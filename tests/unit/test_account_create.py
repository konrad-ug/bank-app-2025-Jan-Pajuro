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
    def test_promo_code_validation(self):
        account = Account("John", "Doe", "01234567890", "PROM_XYZ")
        assert account.balance == 50
        account = Account("John", "Doe", "01234567890", "PKOM_XYZ")
        assert account.balance == 0
        account = Account("John", "Doe", "01234567890", "PROM_WXYZ")
        assert account.balance == 0
        account = Account("John", "Doe", "01234567890", "PROM_XY")
        assert account.balance == 0
    def test_user_age(self):
        account = Account("John", "Doe", "61034567890", "PROM_XYZ")
        assert account.balance == 50
        account = Account("John", "Doe", "60034567890", "PROM_XYZ")
        assert account.balance == 0
        account = Account("John", "Doe", "61834567890", "PROM_XYZ")
        assert account.balance == 0
        account = Account("John", "Doe", "60234567890", "PROM_XYZ")
        assert account.balance == 50

class TestAccount1:
    def test_transfer(self):
        account = Account("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_in(50)
        assert account.balance == 100
        account.transfer_in(-50)
        assert account.balance == 100
        account.transfer_in("herofhier")
        assert account.balance == 100
        account.transfer_out(50)
        assert account.balance == 50
        account.transfer_out(-50)
        assert account.balance == 50
        account.transfer_out("ouberub")
        assert account.balance == 50
        account.transfer_out(100)
        assert account.balance == 50




