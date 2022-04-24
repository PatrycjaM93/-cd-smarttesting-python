from datetime import date
from unittest.mock import Mock, patch

import pytest
from smarttesting.customer.person import Person
from smarttesting.verifier.customer.verification.business_rules_verification import (
    BusinessRulesVerification,
)
from smarttesting.verifier.customer.verification.verifier_manager import VerifierManager
from smarttesting.verifier.event_emitter import EventEmitter


@pytest.mark.homework(
    reason=(
        "Czy ten test na pewno jest czytelny? Co on w ogóle testuje? "
        "Czyżby wszystkie przypadki błędnych weryfikacji?"
    )
)
class TestBusinessRulesVerification:
    def test(self) -> None:
        emitter = Mock(spec_set=EventEmitter)
        manager = Mock(spec_set=VerifierManager)
        # Jan should fail
        verify_name_patcher = patch.object(
            manager, "verify_name", side_effect=lambda person: person.name != "Jan"
        )
        verify_name_patcher.start()
        business_rules_verification = BusinessRulesVerification(emitter, manager)
        verify_address_patcher = patch.object(
            manager, "verify_address", return_value=True
        )
        verify_address_patcher.start()
        verify_phone_patcher = patch.object(manager, "verify_phone", return_value=True)
        verify_phone_patcher.start()
        verify_tax_info_patcher = patch.object(
            manager, "verify_tax_information", return_value=True
        )
        verify_tax_info_patcher.start()
        person = Person("Jan", "Kowalski", date.today(), None, "12309279124123")  # type: ignore
        verify_surname_patcher = patch.object(
            manager, "verify_surname", return_value=True
        )
        verify_surname_patcher.start()
        passes = business_rules_verification.passes(person)
        assert not passes
        manager.verify_name.assert_called_once()
        assert manager.verify_name.mock_calls[0][1][0].name == "Jan"
        patch.stopall()
        verify_name_patcher = patch.object(manager, "verify_name", return_value=True)
        verify_name_patcher.start()
        verify_address_patcher = patch.object(
            manager, "verify_address", return_value=False
        )
        verify_address_patcher.start()
        passes = business_rules_verification.passes(person)
        assert not passes
        patch.stopall()
        verify_address_patcher = patch.object(
            manager, "verify_address", return_value=True
        )
        verify_address_patcher.start()
        verify_phone_patcher = patch.object(manager, "verify_phone", return_value=False)
        verify_phone_patcher.start()
        passes = business_rules_verification.passes(person)
        assert not passes
        patch.stopall()
        verify_phone_patcher = patch.object(manager, "verify_phone", return_value=True)
        verify_phone_patcher.start()
        verify_tax_info_patcher = patch.object(
            manager, "verify_tax_information", return_value=False
        )
        verify_tax_info_patcher.start()
        passes = business_rules_verification.passes(person)
        assert not passes
