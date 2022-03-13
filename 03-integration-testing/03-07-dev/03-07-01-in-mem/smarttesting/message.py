from typing import ClassVar, Dict, Type


class Message:
    """Klasa bazowa dla wszystkich wiadomości.

    Potrzebna jest nam 'jedynie' do implementacji własnego kodeka do tasków Celery
    by można było przekazywać instancje dataclass jako argumenty wywołania tasków."""

    __messages_by_name: ClassVar[Dict[str, Type]] = {}

    def __init_subclass__(cls) -> None:
        cls.__messages_by_name[cls.__name__] = cls

    @classmethod
    def subclass_for_name(cls, name: str) -> Type:
        return cls.__messages_by_name[name]
