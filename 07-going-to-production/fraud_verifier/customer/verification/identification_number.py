from fraud_verifier.customer.person import Gender, Person
from fraud_verifier.verification import Verification


class IdentificationNumberVerification(Verification):
    """Weryfikacja poprawności numeru PESEL.

    Zobacz: https://pl.wikipedia.org/wiki/PESEL#Cyfra_kontrolna_i_sprawdzanie_poprawno.C5.9Bci_numeru
    """

    def passes(self, person: Person) -> bool:
        return (
            self._gender_matches_id_number(person)
            and self._starts_with_date_of_birth(person)
            and self._weight_is_correct(person)
        )

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
        if len(person.national_id_number) != 11:
            return False

        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        weight_sum = sum(
            int(person.national_id_number[index]) * weights[index]
            for index in range(10)
        )
        actual_sum = (10 - weight_sum % 10) % 10

        check_sum = int(person.national_id_number[10])
        return actual_sum == check_sum
