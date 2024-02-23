"""TAS Fire Service Incidents feed."""
from __future__ import annotations

import logging
from datetime import datetime

from aio_geojson_client.feed import GeoJsonFeed
from aiohttp import ClientSession
from geojson import FeatureCollection

from .consts import URL
from .feed_entry import TasFireServiceIncidentsFeedEntry

_LOGGER = logging.getLogger(__name__)


class TasFireServiceIncidentsFeed(
    GeoJsonFeed[TasFireServiceIncidentsFeedEntry]
):
    """TAS Fire Services Incidents feed."""

    def __init__(
        self,
        websession: ClientSession,
        home_coordinates: tuple[float, float],
        filter_radius: float = None,
        filter_alertlevels: list[str] = None,
        filter_feedtypes: list[str] = None,
    ):
        """Initialise this service."""
        super().__init__(websession, home_coordinates, URL, filter_radius=filter_radius)
        self._filter_alertlevels = filter_alertlevels
        self._filter_feedtypes = filter_feedtypes

    def __repr__(self):
        """Return string representation of this feed."""
        return "<{}(home={}, url={}, radius={}, categories={})>".format(
            self.__class__.__name__,
            self._home_coordinates,
            self._url,
            self._filter_radius,
            self._filter_alertlevels,
            self._filter_feedtypes,
        )

    def _new_entry(
        self, home_coordinates: tuple[float, float], feature, global_data: dict
    ) -> TasFireServiceIncidentsFeedEntry:
        """Generate a new entry."""
        return TasFireServiceIncidentsFeedEntry(home_coordinates, feature)

    def _filter_entries(
        self, entries: list[TasFireServiceIncidentsFeedEntry]
    ) -> list[TasFireServiceIncidentsFeedEntry]:
        """Filter the provided entries."""
        filtered_entries = super()._filter_entries(entries)
        if self._filter_feedtypes:
            filtered_entries = list(
                filter(
                    lambda entry: entry.feedType in self._filter_feedtypes,
                    filtered_entries,
                )
            )
        if self._filter_alertlevels:
            filtered_entries = list(
                filter(
                    lambda entry: entry.alertLevel in self._filter_alertlevels,
                    filtered_entries,
                )
            )
        return filtered_entries

    def _extract_last_timestamp(
        self, feed_entries: list[TasFireServiceIncidentsFeedEntry]
    ) -> datetime | None:
        """Determine latest (newest) entry from the filtered feed."""
        if feed_entries:
            dates = sorted(
                filter(None, [entry.changed for entry in feed_entries]),
                reverse=True,
            )
            return dates[0]
        return None

    def _extract_from_feed(self, feed: FeatureCollection) -> dict | None:
        """Extract global metadata from feed."""
        return None
