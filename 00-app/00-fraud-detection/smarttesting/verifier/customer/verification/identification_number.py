import logging


from smarttesting.customer.person import Gender, Person
from smarttesting.verifier.verification import Verification


logger = logging.getLogger(__name__)


class IdentificationNumberVerification(Verification):
    """Weryfikacja poprawności numeru PESEL.

    Algorytm napisany na podstawie:
    https://obywatel.gov.pl/pl/dokumenty-i-dane-osobowe/czym-jest-numer-pesel

    Co oznaczają poszczególne cyfry w numerze PESEL?
    Każda z 11 cyfr w numerze PESEL ma swoje znaczenie. Można je podzielić następująco:

    RRMMDDPPPPK

    RR - to 2 ostanie cyfry roku urodzenia,
    MM - to miesiąc urodzenia.
        Zapoznaj się z sekcją  "Dlaczego osoby urodzone po 1999 roku mają inne
        oznaczenie miesiąca urodzenia", która znajduje się poniżej
    DD - to dzień urodzenia,
    PPPP - to liczba porządkowa oznaczająca płeć.
        U kobiety ostatnia cyfra tej liczby jest parzysta (0, 2, 4, 6, 8),
        a u mężczyzny - nieparzysta (1, 3, 5, 7, 9)
    K - to cyfra kontrolna.

    Przykład: PESEL 810203PPP6K należy do kobiety, która urodziła się 3 lutego 1981,
        a PESEL 761115PPP3K - do mężczyzny, który urodził się 15 listopada 1976 roku.
    """

    def passes(self, person: Person) -> bool:
        passed = (
            self._gender_matches_id_number(person)
            and self._starts_with_date_of_birth(person)
            and self._weight_is_correct(person)
        )
        logger.info("Person %r passed the id number check %s", person, passed)
        return passed

    def _gender_matches_id_number(self, person: Person) -> bool:
        tenth_character = person.national_id_number[9:10]
        if int(tenth_character) % 2 == 0:
            return person.gender == Gender.FEMALE
        else:
            return person.gender == Gender.MALE

    def _starts_with_date_of_birth(self, person: Person) -> bool:
        dob_formatted = person.date_of_birth.strftime("%y%m%d")
        if dob_formatted[0] == "0":
            month = person.date_of_birth.month + 20
            dob_formatted = dob_formatted[:2] + str(month) + dob_formatted[4:]

        return dob_formatted == person.national_id_number[:6]

    def _weight_is_correct(self, person: Person) -> bool:
        """Pomnóż każdą cyfrę z numeru PESEL przez odpowiednią wagę."""
        if len(person.national_id_number) != 11:
            return False

        weights = [1, 2, 7, 8, 1, 3, 7, 9, 1, 3]
        # Dodaj do siebie otrzymane wyniki.
        # Uwaga, jeśli w trakcie mnożenia otrzymasz liczbę dwucyfrową, należy dodać
        # tylko ostatnią cyfrę (na przykład zamiast 63 dodaj 3).
        weight_sum = sum(
            int(person.national_id_number[index]) * weights[index]
            for index in range(10)
        )
        actual_sum = (10 - weight_sum % 10) % 10

        # Odejmij uzyskany wynik od 10. Uwaga: jeśli w trakcie dodawania otrzymasz
        # liczbę dwucyfrową, należy odjąć tylko ostatnią cyfrę
        # (na przykład zamiast 32 odejmij 2).
        # Cyfra, która uzyskasz, to cyfra kontrolna. 10 - 2 = 8
        check_sum = int(person.national_id_number[10])
        return actual_sum == check_sum
