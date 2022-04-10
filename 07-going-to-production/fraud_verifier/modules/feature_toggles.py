import injector
from sqlalchemy.orm import Session

from fraud_verifier.feature_toggles.manager import FeatureManager


class FeatureTogglesModule(injector.Module):
    @injector.provider
    def manager(self, session: Session) -> FeatureManager:
        return FeatureManager(session)
