# python-aio-geojson-tas-tfs-incidents

[![Build Status](https://github.com/zellers/python-aio-geojson-tas-tfs-incidents/workflows/CI/badge.svg)](https://github.com/zellers/python-aio-geojson-tas-tfs-incidents/actions?workflow=CI)
[![PyPi](https://img.shields.io/pypi/v/aio-geojson-tas-tfs-incidents.svg)](https://test.pypi.org/project/aio-geojson-tas-tfs-incidents)
[![Version](https://img.shields.io/pypi/pyversions/aio-geojson-tas-tfs-incidents.svg)](https://test.pypi.org/project/aio-geojson-tas-tfs-incidents)

This library is a fork of [python-aio-geojson-nsw-rfs-incidents](https://github.com/exxamalte/python-aio-geojson-nsw-rfs-incidents) for convenient async access to the [Tas Alert Feed](https://alert.tas.gov.au/).
 
## Installation
`pip install aio-geojson-tas-tfs-incidents`

## Usage
See below for examples of how this library can be used. After instantiating a 
particular class - feed or feed manager - and supply the required parameters, 
you can call `update` to retrieve the feed data. The return value 
will be a tuple of a status code and the actual data in the form of a list of 
feed entries specific to the selected feed.

Status Codes
* _OK_: Update went fine and data was retrieved. The library may still 
  return empty data, for example because no entries fulfilled the filter 
  criteria.
* _OK_NO_DATA_: Update went fine but no data was retrieved, for example 
  because the server indicated that there was not update since the last request.
* _ERROR_: Something went wrong during the update

**Parameters**

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| `home_coordinates` | Coordinates (tuple of latitude/longitude) |

**Supported Filters**

| Filter     |                     | Description |
|------------|---------------------|-------------|
| Radius     | `filter_radius`     | Radius in kilometers around the home coordinates in which events from feed are included. |
| Categories | `filter_categories` | Array of category names. Only events with a category matching any of these is included. |

**Example**
```python
import asyncio
from aiohttp import ClientSession
from aio_geojson_tas_tfs_incidents import TasFireServiceIncidentsFeed
async def main() -> None:
    async with ClientSession() as websession:    
        # Home Coordinates: Latitude: -42.0, Longitude: 147.0
        # Filter radius: 50 km
        # Filter categories: 'Advice'
        feed = TasFireServiceIncidentsFeed(websession, 
                                                (-42, 147.0), 
                                                filter_radius=50, 
                                                filter_feedtypes=['warning'],
                                                filter_alertlevels=['watch_and_act', 'advice'])
        status, entries = await feed.update()
        print(status)
        print(entries)
asyncio.get_event_loop().run_until_complete(main())
```

## Feed entry properties
Each feed entry is populated with the following properties:

| Name               | Description                                                                                         | Feed attribute |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| geometries         | All geometry details of this entry.                                                                                                        | `geometries`   |
| coordinates        | Best coordinates (latitude, longitude) of this entry.                                                                                      | `geometries`   |
| external_id        | The unique public identifier for this incident.                                                                                            | `id`           |
| title              | Title of this entry.                                                                                                                       | `title`        |
| attribution        | Attribution of the feed.                                                                                                                   | n/a            |
| distance_to_home   | Distance in km of this entry to the home coordinates.                                                                                      | n/a            |
| feedType           | The type of messages ('incident', 'warning').                                                                                              | `feedType`     |
| alertLevel         | The alert level of the incident ("emergency_warning", "watch_and_act", "advice", "not_applicable"). Only available for feedType 'warning'. | `category`     |
| created            | The creation date of the incident.                                                                                                         | `created`      |
| changed            | The last changed date of the incident.                                                                                                     | `changed`      |
| bodyHtml           | The description of the incident including HTML tags.                                                                                       | `bodyHtml`     |
| description        | The description of the incident without HTML tags.                                                                                         | n/a            |
| location           | Location description of the incident.                                                                                                      | `location`     |
| status             | Status of the incident.                                                                                                                    | `status`       |
| type               | Type of the incident (e.g. Bush Fire, Grass Fire, Hazard Reduction).                                                                       | `type`['name'] |
| burntArea          | Burnt area in ha.                                                                                                                          | `burntArea`    |


## Feed Manager

The Feed Manager helps managing feed updates over time, by notifying the 
consumer of the feed about new feed entries, updates and removed entries 
compared to the last feed update.

* If the current feed update is the first one, then all feed entries will be 
  reported as new. The feed manager will keep track of all feed entries' 
  external IDs that it has successfully processed.
* If the current feed update is not the first one, then the feed manager will 
  produce three sets:
  * Feed entries that were not in the previous feed update but are in the 
    current feed update will be reported as new.
  * Feed entries that were in the previous feed update and are still in the 
    current feed update will be reported as to be updated.
  * Feed entries that were in the previous feed update but are not in the 
    current feed update will be reported to be removed.
* If the current update fails, then all feed entries processed in the previous
  feed update will be reported to be removed.

After a successful update from the feed, the feed manager provides two
different dates:

* `last_update` will be the timestamp of the last update from the feed 
  irrespective of whether it was successful or not.
* `last_update_successful` will be the timestamp of the last successful update 
  from the feed. This date may be useful if the consumer of this library wants 
  to treat intermittent errors from feed updates differently.
* `last_timestamp` (optional, depends on the feed data) will be the latest 
  timestamp extracted from the feed data. 
  This requires that the underlying feed data actually contains a suitable 
  date. This date may be useful if the consumer of this library wants to 
  process feed entries differently if they haven't actually been updated.
