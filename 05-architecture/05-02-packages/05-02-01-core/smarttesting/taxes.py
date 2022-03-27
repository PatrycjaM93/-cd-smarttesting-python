import random


class TaxService:
    def calculate(self) -> int:
        if random.random() > 0.5:
            raise NotImplementedError

        return 42
