from dataclasses import dataclass

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from fraud_verifier.feature_toggles.features import Feature
from fraud_verifier.feature_toggles.model import FeatureModel


@dataclass
class FeatureManager:
    _session: Session

    def is_enabled(self, feature: Feature) -> bool:
        try:
            entry: FeatureModel = (
                self._session.query(FeatureModel)
                .filter(FeatureModel.name == feature.name)
                .one()
            )
        except NoResultFound:
            return False

        return entry.enabled
