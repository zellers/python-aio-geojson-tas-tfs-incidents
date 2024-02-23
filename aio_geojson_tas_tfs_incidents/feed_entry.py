"""TAS Fire Service Incidents feed entry."""
from __future__ import annotations

import calendar
import logging
import re
from datetime import datetime
from time import strptime

import pytz
from aio_geojson_client.feed_entry import FeedEntry
from geojson import Feature

from .consts import (
    ATTR_FEEDTYPE,
    ATTR_ALERTLEVEL,
    ATTR_BODYHTML,
    ATTR_ID,
    ATTR_PUB_DATE,
    ATTR_TITLE,
    ATTR_AREA,
    ATTR_CREATED,
    ATTR_CHANGED,
    ATTR_TYPE,
    ATTR_ADDRESS,
    ATTR_STATUS,
    ATTR_BURNTAREA,
    ATTRIBUTION,
)

_LOGGER = logging.getLogger(__name__)


class TasFireServiceIncidentsFeedEntry(FeedEntry):
    """TAS Fire Service Incidents feed entry."""

    def __init__(self, home_coordinates: tuple[float, float], feature: Feature):
        """Initialise this service."""
        super().__init__(home_coordinates, feature)

    @property
    def attribution(self) -> str | None:
        """Return the attribution of this entry."""
        return ATTRIBUTION

    @property
    def title(self) -> str:
        """Return the title of this entry."""
        return self._search_in_properties(ATTR_TITLE)

    @property
    def alertLevel(self) -> str:
        """Return the alertLevel of this entry."""
        return self._search_in_properties(ATTR_ALERTLEVEL)

    @property
    def feedType(self) -> str:
        """Return the feedType of this entry."""
        return self._search_in_properties(ATTR_FEEDTYPE)

    @property
    def external_id(self) -> str:
        """Return the external id of this entry."""
        return self._search_in_properties(ATTR_ID)

    @property
    def created(self) -> datetime:
        """Return the creation timestamp date of this entry."""
        created = datetime.fromisoformat(self._search_in_properties(ATTR_CREATED))
        return created


    @property
    def changed(self) -> datetime:
        """Return the creation timestamp date of this entry."""
        changed = datetime.fromisoformat(self._search_in_properties(ATTR_CHANGED))
        return changed

    @property
    def bodyHtml(self) -> str:
        """Return the description of this entry."""
        return self._search_in_properties(ATTR_BODYHTML)

    @property
    def description(self) -> str:
        """Return the description of this entry."""
        description = self._search_in_properties(ATTR_BODYHTML)
        if description:
            clean = re.compile('<.*?>')
            description =  re.sub(clean, '', self._search_in_properties(ATTR_BODYHTML))
        return description

    # def _search_in_description(self, regexp):
    #     """Find a sub-string in the entry's description."""
    #     if self.description:
    #         match = re.search(regexp, self.description)
    #         if match:
    #             return match.group(CUSTOM_ATTRIBUTE)
    #     return None

    @property
    def location(self) -> str:
        """Return the location of this entry."""
        return self._search_in_properties(ATTR_ADDRESS)

    @property
    def status(self) -> str:
        """Return the status of this entry."""
        return self._search_in_properties(ATTR_STATUS)

    @property
    def type(self) -> str:
        """Return the type of this entry."""
        entrytype =  self._search_in_properties(ATTR_TYPE)
        return entrytype["name"]

    @property
    def burntArea(self) -> str:
        """Return the size of this entry."""
        return self._search_in_properties(ATTR_BURNTAREA)
