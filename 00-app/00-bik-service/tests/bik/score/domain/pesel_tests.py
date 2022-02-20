import pytest
from smarttesting.bik.score.domain.pesel import Pesel


class TestPesel:
    def test_creates_new_pesel(self) -> None:
        raw_pesel_string = "91121345678"

        pesel = Pesel(raw_pesel_string)

        assert pesel.pesel == raw_pesel_string

    @pytest.mark.parametrize(
        "raw_pesel",
        [
            ("9112134567",),
            ("911213456789",),
        ],
    )
    def test_raises_exception_for_pesel_of_length_other_than_11(
        self, raw_pesel: str
    ) -> None:
        with pytest.raises(ValueError):
            Pesel(raw_pesel)
