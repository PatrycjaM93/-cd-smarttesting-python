class Test08SpecialTaxCalculator:
    def test_does_not_apply_special_tax_when_amount_not_reaching_threshold(
        self,
    ) -> None:
        initial_amount = 8
        calculator = SpecialTaxCalculator(initial_amount)

        result = calculator.calculate()

        assert result == initial_amount

    def test_applies_special_tax_when_amount_reaches_threshold(self) -> None:
        initial_amount = 25
        calculator = SpecialTaxCalculator(initial_amount)

        result = calculator.calculate()

        assert result == 500


class SpecialTaxCalculator:
    AMOUNT_THRESHOLD = 10
    TAX_MULTIPLIER = 20

    def __init__(self, amount: int) -> None:
        self._amount = amount

    def calculate(self):
        if self._amount <= self.AMOUNT_THRESHOLD:
            return self._amount
        return self._amount * self.TAX_MULTIPLIER
