from smarttesting.client.customer_verifier import Dao


class InMemoryDao(Dao):
    """Klasa symulująca rozszerzenie oryginalnej klasy łączącej się z bazą danych.

    Udaje, że wykorzystuje bazę danych w pamięci.
    """
