import time
from datetime import datetime
from typing import Any
from urllib.parse import urljoin

import pandas as pd
import requests
from pytz import UTC
from requests.auth import HTTPBasicAuth

from ..logging import success_parsing_log
from ..structure.subject import SCHEMA, Column, Metadata, Sensor, Subject, Vendor
from ..utils import (
    align_datetimes,
    get_sampling_frequency,
)
from .utils import change_crs, change_timezone, get_crs, get_timezone


def _knots_to_kmh(knots):
    return knots * 1.852


def _get_device(
    url: str,
    username: str,
    password: str,
    subject_id: str,
) -> dict[str, Any]:
    url = urljoin(url, "api/devices")

    params = {"uniqueId": subject_id}

    headers = {
        "Accept": "application/json",
    }

    response = requests.get(
        url,
        params,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
    )

    response_json = response.json()

    if not response_json:
        raise ValueError(f"Device with subject_id {subject_id} not found")

    device = response_json[0]
    phone = device["phone"]
    model = device["model"]

    if phone and model:
        model = f"{phone} ({model})"
    elif phone:
        model = phone
    elif model:
        model = model

    return {
        "id": device["id"],
        "model": model,
    }


def _get_records(
    url: str,
    username: str,
    password: str,
    id: int,
    start: datetime | None = None,
    end: datetime | None = None,
) -> dict[str, Any]:
    url = urljoin(url, "api/reports/route")

    params = {
        "deviceId": id,
        "from": start,
        "to": end,
    }

    headers = {
        "Accept": "application/json",
    }

    response = requests.get(
        url,
        params,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
    )

    response_json = response.json()

    if not response_json:
        raise ValueError(f"No records found for device with id {id}")

    return response_json


def _parse_records(response_json: dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame(response_json)
    attributes = pd.json_normalize(df["attributes"]).add_prefix("attributes_")  # type: ignore
    df = pd.concat([df, attributes], axis=1).drop(columns=["attributes"])

    df = df[df["valid"] == True]
    df.rename(
        columns={
            "fixTime": Column.DATETIME,
            "altitude": Column.ELEVATION,
            "attributes_distance": Column.DISTANCE,
            "accuracy": Column.GNSS_ACCURACY,
            "attributes_motion": Column.MOTION,
        },
        inplace=True,
    )

    df = df[
        [
            Column.DATETIME,
            Column.LATITUDE,
            Column.LONGITUDE,
            Column.ELEVATION,  # Unit defaults to: meters
            Column.SPEED,  # Unit defaults to: knots
            Column.DISTANCE,  # Unit defaults to: meters
            Column.GNSS_ACCURACY,  # Unit defaults to meters
            Column.MOTION,
        ]
    ]

    df[Column.SPEED] = df[Column.SPEED].apply(_knots_to_kmh)

    df[Column.DATETIME] = pd.to_datetime(df[Column.DATETIME]).dt.tz_localize(None)
    df.set_index(Column.DATETIME, inplace=True)

    return df


def from_server(
    url: str,
    username: str,
    password: str,
    subject_id: str,
    *,
    start: datetime | None = None,
    end: datetime | None = None,
    sampling_frequency: float | None = None,
    crs: str | None = "infer",
    timezone: str | None = "infer",
    sensor_id: str | None = None,
    vendor: Vendor = Vendor.TRACCAR,
    model: str | None = None,
    serial_number: str | None = None,
    firmware_version: str | None = None,
) -> Subject:
    """
    The Traccar API allows you to download data from a specific server (URL) using your login credentials (username and password). To obtain data for a particular device, you must specify a subject ID (which corresponds to the device identifier). Optionally, you can define a date and time range to download data for a specific timeframe. If no date range is provided (from/to), all data for the chosen device will be downloaded.

    The downloaded data will be parsed and validated according to the schema defined in the structure module.

    Args:
        url (str): The URL of the Traccar server.
        username (str): The username to authenticate with the server.
        password (str): The password to authenticate with the server.
        subject_id (str): The ID of the subject to fetch data for (corresponds to the device identifier).
        start (datetime, optional): The start time of the data to fetch. If not provided, it will fetch all available data.
        end (datetime, optional): The end time of the data to fetch. If not provided, it will fetch all available data.
        sampling_frequency (float, optional): The sampling frequency of the data. If not provided, it will be infered from data.
        timezone (str, optional): The timezone of the data. If set to "infer" it will be inferred from the data. If None it will be set to the local timezone. Otherwise, it will be set to the provided timezone.
        crs (str, optional): The coordinate reference system (CRS) of the data. If set to "infer" it will be inferred from the data. If None it will be set to "EPSG:4326". Otherwise, it will be set to the provided CRS.
        sensor_id (str, optional): The ID of the sensor to fetch data for. If not provided, unique device ID from Traccar server will be used (if available).
        vendor (Vendor, optional): The vendor of the device. Defaults to "Traccar".
        model (str, optional): The model of the device. If not provided, it will be fetched from the Traccar server (device - extra, phone + model) if available.
        serial_number (str, optional): The serial number of the device.
        firmware_version (str, optional): The firmware version of the device.

    Returns:
        Subject: A Subject object containing the fetched and processed dataframe containing information: datetime, latitude, longitude, gps_accuracy, distance, elevation, and speed.

    Examples:
        Here's how to call the function with just the minimum required parameters.

        ```python
        from labda.parsers import Traccar

        subject = Traccar.from_server(
            url="http://gps.example.com",
            username="admin",
            password="pwd9000",
            subject_id="john_doe",
        )
        ```
    """
    origin_tz = "UTC"
    origin_crs = "EPSG:4326"

    if not start:
        start = datetime.fromtimestamp(0)

    if not end:
        end = datetime.now()

    start = start.astimezone(UTC).isoformat()  # type: ignore
    end = end.astimezone(UTC).isoformat()  # type: ignore

    device = _get_device(url, username, password, subject_id)
    records = _get_records(url, username, password, device["id"], start, end)
    df = _parse_records(records)

    if not timezone:
        timezone = time.tzname[0]
    if timezone == "infer":
        timezone = get_timezone(df)
        df = change_timezone(df, origin_tz, timezone)
    else:
        df = change_timezone(df, origin_tz, timezone)

    if not crs:
        crs = origin_crs
    if crs == "infer":
        crs = get_crs(df)
        df = change_crs(df, origin_crs, crs)
    else:
        df = change_crs(df, origin_crs, crs)

    if not sampling_frequency:
        sampling_frequency = get_sampling_frequency(df)

    df = align_datetimes(df, sampling_frequency)

    # Order columns as defined in Column, remove extra columns
    records_columns = [col.value for col in Column]
    ordered_columns = [col for col in records_columns if col in df.columns]
    df = df[ordered_columns]

    df = SCHEMA.validate(df)

    sensor_id = sensor_id or device["id"]
    model = model or device["model"]

    sensor = Sensor(
        id=sensor_id,  # type: ignore
        serial_number=serial_number,
        model=model,
        vendor=vendor,
        firmware_version=firmware_version,
    )

    metadata = Metadata(
        id=subject_id,
        sensor=[sensor],
        sampling_frequency=sampling_frequency,
        crs=crs,
        timezone=timezone,
    )

    subject = Subject(metadata=metadata, df=df)

    func = f"{__name__}:from_server"
    success_parsing_log(subject, url, func)

    return subject
