import logging
from urllib.parse import urljoin

import requests
from marshmallow_dataclass import class_schema
from smarttesting.bik.score.domain.pesel import Pesel
from smarttesting.bik.score.personal.personal_information import PersonalInformation

logger = logging.getLogger(__name__)


class PersonalInformationClient:
    def __init__(self, personal_information_service_url: str) -> None:
        self._personal_information_service_url = personal_information_service_url

    def get_personal_information(self, pesel: Pesel) -> PersonalInformation | None:
        url = urljoin(self._personal_information_service_url, pesel.pesel)
        personal_info_raw = requests.get(url).json()
        personal_info = self._deserialize(personal_info_raw)
        logger.info("Personal information for id %s is %r", pesel, personal_info_raw)
        return personal_info

    def _deserialize(self, data: dict) -> PersonalInformation:
        schema_cls = class_schema(PersonalInformation)
        return schema_cls().load(data)
