# Changes

## 0.7.1 (23/02/2024)
* Initial relase of fork for Tasmania.

## 0.7 (26/01/2024)
* Bumped version of upstream aio_geojson_client library to 0.20.
* Improved JSON parsing error handling, especially when not using Python's built-in JSON parsing library.
* Code quality improvements.
* Added Python 3.12 support.
* Removed Python 3.7 support.
* Bumped library versions: black, flake8, isort.
* Migrated to pytest.

## 0.6 (24/01/2023)
* Added Python 3.11 support.
* Removed deprecated asynctest dependency.
* Bumped version of upstream aio_geojson_client library to 0.18.
* Bumped library versions: black.

## 0.5 (18/02/2022)
* No functional changes.
* Added Python 3.10 support.
* Removed Python 3.6 support.
* Bumped version of upstream aio_geojson_client library to 0.16.
* Bumped library versions: black, flake8, isort.
* Migrated to github actions.

## 0.4 (12/06/2021)
* Set aiohttp to a release 3.7.4 or later (thanks @fabaff).
* Add license tag (thanks @fabaff).
* Added Python 3.9 support.
* Bump aio_geojson_client to v0.14.
* General code improvements.

## 0.3 (18/02/2020)
* Bumped version of upstream GeoJSON library.
* Fixes extraction of polygons from a feed (polygon without hole only).

## 0.2 (17/02/2020)
* Bumped version of upstream GeoJSON library.
* Added status callback.
* Internal code improvements.

## 0.1 (14/11/2019)
* Initial release.
* Supporting all the features available in non-async library 
  ([python-aio-geojson-client](https://github.com/exxamalte/python-aio-geojson-client)).
