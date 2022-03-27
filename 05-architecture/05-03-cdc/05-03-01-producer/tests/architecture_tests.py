from pathlib import Path

import pytest
from pylint import epylint


class TestArchitecture:
    @pytest.fixture(autouse=True)
    def setup(self):
        root_dir = Path(__file__).parents[1]
        self.paths_to_check = [
            str(root_dir / module_name)
            for module_name in (
                "smarttesting",
                "smarttesting_api",
                "smarttesting_main",
                "tests",
            )
        ]

    def test_run_pylint_checks_on_modules(self) -> None:
        """Uruchomienie pylinta programatycznie.

        Po więcej szczegółów zajrzyj do 05-02-packages.
        """
        pylint_arg = " ".join(self.paths_to_check)
        std_out, _std_err = epylint.py_run(pylint_arg, return_std=True)

        std_out.seek(0)
        output = std_out.read()
        assert "Your code has been rated at 10.00/10" in output, output
