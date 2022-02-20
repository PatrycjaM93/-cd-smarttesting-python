import os
import logging
import sys
from dataclasses import dataclass
from typing import List, Literal, cast

import injector
from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from smarttesting.celery_module import CeleryConfig, CeleryModule
from smarttesting.dev_modules import DevModule
from smarttesting.verifier.customer.module import CustomerModule
from smarttesting.verifier.customer.verification.module import VerificationModule
from smarttesting.verifier.customer.verified_person import Base

Env = Literal["PROD", "DEV"]


def assemble(env: Env = "PROD") -> injector.Injector:
    """Zainicjowanie kontenera IoC."""
    configure_logging()
    extra_modules: List[injector.Module] = []

    db_dsn = os.environ.get("DB_URL", "sqlite:///dev_database.db")
    broker_url = os.environ.get("BROKER_URL", "memory://")
    if env == "PROD":
        extra_modules += [ProdConfigModule(broker_url)]
    elif env == "DEV":
        extra_modules += [DevConfigModule(broker_url), DevModule()]

    modules = [
        VerificationModule(),
        CustomerModule(),
        CeleryModule(),
        DbModule(db_dsn),
    ] + extra_modules

    container = injector.Injector(modules=modules, auto_bind=False)

    # Zarejestruj taski w Celery wywołując ich wstrzyknięcie
    container.get(List[Task])

    return container


@dataclass
class ProdConfigModule(injector.Module):
    _broker_url: str

    @injector.singleton
    @injector.provider
    def celery_config(self) -> CeleryConfig:
        CeleryConfigProd.broker_url = self._broker_url
        return cast(CeleryConfig, CeleryConfigProd)


@dataclass
class DevConfigModule(injector.Module):
    _broker_url: str

    @injector.singleton
    @injector.provider
    def celery_config(self) -> CeleryConfig:
        CeleryConfigDev.broker_url = self._broker_url
        return cast(CeleryConfig, CeleryConfigDev)


class CeleryConfigProd:
    accept_content = {"json", "dataclasses_serialization"}
    task_serializer = "dataclasses_serialization"
    result_backend = "rpc://"
    result_persistent = False
    broker_url = ""  # będzie nadpisane


class CeleryConfigDev(CeleryConfigProd):
    worker_concurrency = 1


class DbModule(injector.Module):
    def __init__(self, db_dsn: str) -> None:
        self._db_dsn = db_dsn
        self._engine = create_engine(self._db_dsn)
        self._scoped_session_factory = scoped_session(sessionmaker(bind=self._engine))
        # Stwórz schemat bazy danych. Normalnie odbywa się to przez migracje
        Base.metadata.create_all(self._engine)

    @injector.provider
    def session(self) -> Session:
        return self._scoped_session_factory()


def configure_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    root.addHandler(handler)