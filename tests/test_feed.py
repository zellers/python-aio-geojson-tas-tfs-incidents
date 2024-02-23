"""Test for the TAS Fire Service Incidents GeoJSON feed."""
import asyncio
import datetime
from http import HTTPStatus

import aiohttp
import pytest
from aio_geojson_client.consts import UPDATE_OK

from aio_geojson_tas_tfs_incidents.consts import ATTRIBUTION
from aio_geojson_tas_tfs_incidents.feed import TasFireServiceIncidentsFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(mock_aioresponse):
    """Test updating feed is ok."""
    home_coordinates = (-42, 147.0)
    mock_aioresponse.get(
        "https://alert.tas.gov.au/data/data.geojson",
        status=HTTPStatus.OK,
        body=load_fixture("incidents-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = TasFireServiceIncidentsFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<TasFireServiceIncidentsFeed("
            "home=(-42, 147.0), "
            "url=https://alert.tas.gov.au"
            "/data/data.geojson, "
            "radius=None, categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 3

        feed_entry = entries[0]
        assert feed_entry.title == "Title 1"
        assert feed_entry.feedType == "Type 1"
        assert feed_entry.external_id == "1234"
        assert feed_entry.coordinates == (-42.292141, 146.506805)
        assert round(abs(feed_entry.distance_to_home - 52.0), 1) == 0
        assert repr(feed_entry) == "<TasFireServiceIncidents" "FeedEntry(id=1234)>"
        assert feed_entry.created == datetime.datetime(
            2024, 2, 21, 5, 29, tzinfo=datetime.timezone.utc
        )
        assert feed_entry.location == "Location 1"
        assert feed_entry.status == "Status 1"
        assert feed_entry.type == "Type 1"
        assert feed_entry.burntArea == "1.234"
        assert feed_entry.attribution == ATTRIBUTION

        feed_entry = entries[1]
        assert feed_entry is not None
        assert feed_entry.title == "Title 2"
        assert feed_entry.type == "Type 2"
        assert feed_entry.alertLevel is None

        feed_entry = entries[2]
        assert feed_entry.title == "Title 3"
        assert feed_entry.alertLevel == "alertLevel 3"

@pytest.mark.asyncio
async def test_update_ok_with_feedTypes(mock_aioresponse):
    """Test updating feed is ok, filtered by feedType."""
    home_coordinates = (-42, 147.0)
    mock_aioresponse.get(
        "https://alert.tas.gov.au/data/data.geojson",
        status=HTTPStatus.OK,
        body=load_fixture("incidents-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = TasFireServiceIncidentsFeed(
            websession, home_coordinates, filter_feedtypes=["Type 1"]
        )
        assert (
            repr(feed) == "<TasFireServiceIncidentsFeed("
            "home=(-42, 147.0), "
            "url=https://alert.tas.gov.au"
            "/data/data.geojson, "
            "radius=None, categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 2

        feed_entry = entries[0]
        assert feed_entry is not None
        assert feed_entry.title == "Title 1"
        assert feed_entry.feedType == "Type 1"
        assert repr(feed_entry) == "<TasFireServiceIncidents" "FeedEntry(id=1234)>"


@pytest.mark.asyncio
async def test_empty_feed(mock_aioresponse):
    """Test updating feed is ok when feed does not contain any entries."""
    home_coordinates = (-42, 147.0)
    mock_aioresponse.get(
        "https://alert.tas.gov.au/data/data.geojson",
        status=HTTPStatus.OK,
        body=load_fixture("incidents-2.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        feed = TasFireServiceIncidentsFeed(websession, home_coordinates)
        assert (
            repr(feed) == "<TasFireServiceIncidentsFeed("
            "home=(-42, 147.0), "
            "url=https://alert.tas.gov.au"
            "/data/data.geojson, "
            "radius=None, categories=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 0
        assert feed.last_timestamp is None
