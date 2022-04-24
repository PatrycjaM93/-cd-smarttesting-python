# pylint: disable=pointless-statement
"""Wyłączamy pylinta, który wyłapuje naszą demonstracyjną pomyłkę :)"""


class Test01NoAssertions:
    def test_returns_sum_when_adding_two_numbers(self) -> None:
        first_number = 1
        second_number = 2

        # brakuje `assert`!
        first_number + second_number == 3

    def test_returns_sum_when_adding_two_numbers_fixed(self) -> None:
        """Poprawiony test składający się z samej asercji."""
        assert 1 + 2 == 3
