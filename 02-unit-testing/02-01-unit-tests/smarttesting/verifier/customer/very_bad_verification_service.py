import logging
import time

logger = logging.getLogger(__name__)


class VeryBadVerificationService:
    @staticmethod
    def run_heavy_queries_to_db():
        """Metoda odpalająca ciężkie zapytania do bazy danych
        i ściągająca pół internetu.
        """
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            logger.exception("Something went wrong")

        return True
