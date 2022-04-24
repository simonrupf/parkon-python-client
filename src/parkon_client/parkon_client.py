#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime, timedelta
from json import dumps, loads
from json.decoder import JSONDecodeError
from urllib import request
from urllib.error import URLError

__version__ = "0.0.1"
SERVICE_URL = "https://app.parkon.ch/api/"
HEADERS = {"User-Agent": f"parkon_client/{__version__} (+https://github.com/SimonRupf/parkon-python-client)",
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8"}
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
JSON_FORMAT = f"{DATE_FORMAT}T{TIME_FORMAT}:%SZ"

def validate_email(as_string):
    from email.utils import parseaddr
    email = parseaddr(as_string)[1]
    if "@" not in email:
        raise ValueError
    return email

def validate_date(as_string):
    return datetime.strptime(as_string, DATE_FORMAT)

def validate_time(as_string):
    return datetime.strptime(as_string, TIME_FORMAT)

def request_parking_spot(short_id, vehicle_number, email, start_date_time, hours):
    # resolve the short ID
    unix_timestamp = int(datetime.timestamp(datetime.now()))
    id_request = request.Request(f"{SERVICE_URL}EstatePortal/GetByShortId?shortId={short_id}&_={unix_timestamp}",
        headers=HEADERS, method="GET")
    with request.urlopen(id_request) as response:
        estate = loads(response.read().decode())

    # request a parking spot
    end_date_time = start_date_time + timedelta(hours=hours)
    payload = {"$type": "Parkon.Shared.Dto.VehicleListingDto, Parkon.Bridge",
        "EmailToSendConfirmation": email,
        "EstateId": estate["EstateId"],
        "Notes": "",
        "Source": None,
        "SourcePortalId": estate["Id"],
        "SourcePortalPublicTitle": None,
        "Type": 0,
        "ValidFrom": start_date_time.strftime(JSON_FORMAT),
        "ValidUntil": end_date_time.strftime(JSON_FORMAT),
        "VehicleCanton": None,
        "VehicleFullPlate": vehicle_number,
        "VehicleId": None,
        "VehicleNumber": None,
        "VehicleOwnerAddressCity": None,
        "VehicleOwnerAddressStreet": None,
        "VehicleOwnerAddressZip": None,
        "VehicleOwnerName": None,
        "Id": "00000000-0000-0000-0000-000000000000"}
    parking_request = request.Request(f"{SERVICE_URL}VehicleListing/CreateOrUpdateVehicleListing",
        data=dumps(payload).encode(), headers=HEADERS, method="POST")
    with request.urlopen(parking_request) as response:
        return loads(response.read().decode())

def main():
    # handle command line arguments, offers help via -h/--help
    argument_parser = ArgumentParser(
        description="Requests a parking spot in parkon.")
    argument_parser.add_argument("short_id",
        help="short ID as displayed in the parkon URL, i.e. https://app.parkon.ch/Portal/<ShortId>")
    argument_parser.add_argument("vehicle_number",
        help="full vehicle plate number with cantonal acronym, separated by dash and no spaces between digits, i.e. AG-123456")
    argument_parser.add_argument("email", type=validate_email,
        help="email address to send confirmation, i.e. name@example.com")
    argument_parser.add_argument("date", type=validate_date,
        help="start date for reserving the parking spot, in ISO date format, i.e. 2022-12-31")
    argument_parser.add_argument("time", type=validate_time,
        help="start time for reserving the parking spot, in 24 hours / colon / minute format, i.e. 14:30")
    argument_parser.add_argument("hours", type=int, choices=[2, 4, 8, 12, 24, 72], default=2, nargs="?",
        help="(optional) hours to reserve the parking spot for, 2 by default")
    arguments = argument_parser.parse_args()

    try:
        print(request_parking_spot(arguments.short_id, arguments.vehicle_number,
            arguments.email, datetime.combine(arguments.date, arguments.time.time()),
            arguments.hours))
    except JSONDecodeError as e:
        print(f"Error decoding the JSON response of the parking spot request: {e.msg}")
    except URLError as e:
        print(f"Error during parking spot request: {e.reason}")

if __name__ == "__main__":
    main()
