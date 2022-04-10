from dataclasses import dataclass

import injector
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


@dataclass
class DbModule(injector.Module):
    _db_path: str

    @injector.singleton
    @injector.provider
    def engine(self) -> Engine:
        return create_engine("sqlite:///" + self._db_path)

    @injector.provider
    def session(self, engine: Engine) -> Session:
        session_factory = sessionmaker(bind=engine)
        return session_factory()
