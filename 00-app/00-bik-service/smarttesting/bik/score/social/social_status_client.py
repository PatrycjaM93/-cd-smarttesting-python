import logging
from urllib.parse import urljoin

import requests
from marshmallow_dataclass import class_schema
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.social.social_status import SocialStatus

logger = logging.getLogger(__name__)


class SocialStatusClient:
    def __init__(self, social_status_service_url: str) -> None:
        self._social_status_service_url = social_status_service_url

    def get_social_status(self, pesel: Pesel) -> SocialStatus | None:
        url = urljoin(self._social_status_service_url, pesel.pesel)
        social_status_raw = requests.get(url).json()
        social_status = self._deserialize(social_status_raw)
        logger.info("Social status for id %s is %r", pesel, social_status_raw)
        return social_status

    def _deserialize(self, data: dict) -> SocialStatus:
        schema_cls = class_schema(SocialStatus)
        return schema_cls().load(data)
