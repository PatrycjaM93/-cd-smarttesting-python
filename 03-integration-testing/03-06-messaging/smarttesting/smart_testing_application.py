from typing import List

import injector
from celery import Task
from smarttesting.celery_module import CeleryModule
from smarttesting.verifier.customer.module import CustomerModule
from smarttesting.verifier.customer.verification.module import VerificationModule
from smarttesting.verifier.customer.verified_person import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


def assemble(broker_url: str, db_dsn: str = "sqlite:///:memory:") -> injector.Injector:
    """Zainicjowanie kontenera IoC."""
    container = injector.Injector(
        modules=[
            VerificationModule(),
            CustomerModule(),
            CeleryModule(broker_url),
            EmbeddedSqliteDb(db_dsn),
        ],
        auto_bind=False,
    )

    # Zarejestruj taski w Celery wywołując ich wstrzyknięcie
    container.get(List[Task])

    return container


class EmbeddedSqliteDb(injector.Module):
    def __init__(self, db_dsn: str) -> None:
        self._db_dsn = db_dsn
        self._engine = create_engine(self._db_dsn)
        self._scoped_session_factory = scoped_session(sessionmaker(bind=self._engine))
        # Stwórz schemat bazy danych. Normalnie odbywa się to przez migracje
        Base.metadata.create_all(self._engine)

    def configure(self, binder: injector.Binder) -> None:
        binder.bind(Session, self._scoped_session_factory)
