from typing import Any

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()


class VerifiedPerson(Base):
    """
    Model bazodanowy. Wykorzystujemy ORM (mapowanie obiektowo relacyjne)
    i obiekt tej klasy mapuje się na tabelę "verified". Każde pole klasy to osobna
    kolumna w bazie danych.
    """

    __tablename__ = "verified"

    id = Column(Integer(), primary_key=True)
    uuid: str = Column(String(36))
    national_identification_number: str = Column(String(255))
    status: str = Column(String(255))
