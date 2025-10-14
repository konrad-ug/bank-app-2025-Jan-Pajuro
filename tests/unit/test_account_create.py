from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"
    def test_pesel_validation(self):
        account_short = Account("John", "Doe", "0123456789")
        assert account_short.pesel == "Invalid"
        account_long = Account("Joe", "Dohn", "012345678901")
        assert account_long.pesel == "Invalid"
        account_not_digit = Account("John", "Doe", "abc34567890")
