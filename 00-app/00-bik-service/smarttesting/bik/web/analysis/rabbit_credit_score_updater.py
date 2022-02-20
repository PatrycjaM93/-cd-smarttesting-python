from kombu import Connection, Producer
from smarttesting.bik.score.analysis.score_updater import ScoreUpdater
from smarttesting.bik.score.domain.score_calculated_event import ScoreCalculatedEvent


class RabbitCreditScoreUpdater(ScoreUpdater):
    def __init__(self, connection: Connection) -> None:
        self._producer = Producer(connection)

    def score_calculated(self, score_calculated_event: ScoreCalculatedEvent) -> None:
        self._producer.publish(
            exchange="scoreExchange",
            routing_key="#",
            body={
                "pesel": score_calculated_event.pesel.pesel,
                "score": score_calculated_event.score.points,
            },
        )
