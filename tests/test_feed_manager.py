"""Test for the TAS Fire Service Incidents GeoJSON feed manager."""
import asyncio
import datetime
from http import HTTPStatus

import aiohttp
import pytest

from aio_geojson_tas_tfs_incidents.feed_manager import (
    TasFireServiceIncidentsFeedManager,
)
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_feed_manager(mock_aioresponse):
    """Test the feed manager."""
    home_coordinates = (-42, 147.0)
    mock_aioresponse.get(
        "https://alert.tas.gov.au/data/data.geojson",
        status=HTTPStatus.OK,
        body=load_fixture("incidents-1.json"),
    )

    async with aiohttp.ClientSession(loop=asyncio.get_running_loop()) as websession:
        # This will just record calls and keep track of external ids.
        generated_entity_external_ids = []
        updated_entity_external_ids = []
        removed_entity_external_ids = []

        async def _generate_entity(external_id):
            """Generate new entity."""
            generated_entity_external_ids.append(external_id)

        async def _update_entity(external_id):
            """Update entity."""
            updated_entity_external_ids.append(external_id)

        async def _remove_entity(external_id):
            """Remove entity."""
            removed_entity_external_ids.append(external_id)

        feed_manager = TasFireServiceIncidentsFeedManager(
            websession,
            _generate_entity,
            _update_entity,
            _remove_entity,
            home_coordinates,
            None,
        )
        assert (
            repr(feed_manager) == "<TasFireServiceIncidents"
            "FeedManager("
            "feed=<TasFireService"
            "IncidentsFeed("
            "home=(-42, 147.0), url=https://"
            "alert.tas.gov.au"
            "/data/data.geojson, "
            "radius=None, categories=None)>)>"
        )
        await feed_manager.update()
        entries = feed_manager.feed_entries
        assert entries is not None
        assert len(entries) == 3
        assert feed_manager.last_timestamp == datetime.datetime(
            2024, 2, 23, 5, 3, tzinfo=datetime.timezone.utc
        )
        assert len(generated_entity_external_ids) == 3
        assert len(updated_entity_external_ids) == 0
        assert len(removed_entity_external_ids) == 0
