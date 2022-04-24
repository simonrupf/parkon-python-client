# parkon API python library and CLI client

This is a python 3 library and CLI client, to request parking spots in the
parkon API of [parkon GmbH](https://parkon.ch/).

## Usage

### As a Python 3 Library

```python
from datetime import datetime
from parkon_client.parkon_client import request_parking_spot
request_parking_spot(short_id="short ID as displayed in the parkon URL",
    vehicle_number="AG-123456",
    email="name@example.com",
    start_date_time=datetime.now(),
    hours=2)
```

### As a Command Line Interface Client

```shell
$ parkon_client -h
usage: parkon_client.py [-h] short_id vehicle_number email date time [{2,4,8,12,24,72}]

Requests a parking spot in parkon.

positional arguments:
  short_id          short ID as displayed in the parkon URL, i.e. https://app.parkon.ch/Portal/<ShortId>
  vehicle_number    full vehicle plate number with cantonal acronym, separated by dash and no spaces between digits, i.e. AG-123456
  email             email address to send confirmation, i.e. name@example.com
  date              start date for reserving the parking spot, in ISO date format, i.e. 2022-12-31
  time              start time for reserving the parking spot, in 24 hours / colon / minute format, i.e. 14:30
  {2,4,8,12,24,72}  (optional) hours to reserve the parking spot for, 2 by default

optional arguments:
  -h, --help        show this help message and exit
```

