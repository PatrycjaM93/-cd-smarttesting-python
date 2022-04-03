import unittest
from unittest.mock import Mock

from smarttesting.hello_world import hello_world


class TestHelloWorld(unittest.TestCase):
    def test_writes_hello_world(self) -> None:
        out = Mock()

        hello_world(out)

        assert out.write.called_once_with("Hello, world!\n")
