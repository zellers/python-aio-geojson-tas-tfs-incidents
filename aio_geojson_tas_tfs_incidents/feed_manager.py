"""Feed Manager for TAS Fire Service Incidents feed."""
from __future__ import annotations

from collections.abc import Awaitable, Callable

from aio_geojson_client.feed_manager import FeedManagerBase
from aio_geojson_client.status_update import StatusUpdate
from aiohttp import ClientSession

from .feed import TasFireServiceIncidentsFeed


class TasFireServiceIncidentsFeedManager(FeedManagerBase):
    """Feed Manager for TAS Fire Services Incidents feed."""

    def __init__(
        self,
        websession: ClientSession,
        generate_callback: Callable[[str], Awaitable[None]],
        update_callback: Callable[[str], Awaitable[None]],
        remove_callback: Callable[[str], Awaitable[None]],
        coordinates: tuple[float, float],
        filter_radius: float = None,
        filter_feedtypes: list[str] = None,
        filter_alertlevels: list[str] = None,
        status_callback: Callable[[StatusUpdate], Awaitable[None]] = None,
    ):
        """Initialize the TAS Fire Services Feed Manager."""
        feed = TasFireServiceIncidentsFeed(
            websession,
            coordinates,
            filter_radius=filter_radius,
            filter_feedtypes=filter_feedtypes,
            filter_alertlevels=filter_alertlevels,
        )
        super().__init__(
            feed,
            generate_callback,
            update_callback,
            remove_callback,
            status_async_callback=status_callback,
        )
