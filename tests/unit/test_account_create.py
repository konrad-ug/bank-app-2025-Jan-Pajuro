from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"
    def test_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "0123456789")
        assert account.pesel == "Invalid"
    def test_pesel_too_long(self):
        account = PersonalAccount("Joe", "Dohn", "012345678901")
        assert account.pesel == "Invalid"
    def test_pesel_is_digit(self):
        account = PersonalAccount("John", "Doe", "abc34567890")
        assert account.pesel == "Invalid"
    def test_promo_code_validation(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        assert account.balance == 50
    def test_promo_code_prefix(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PKOM_XYZ")
        assert account.balance == 0
    def test_promo_code_too_long(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_WXYZ")
        assert account.balance == 0
    def test_promo_code_too_short(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XY")
        assert account.balance == 0
    def test_user_age(self):
        account = PersonalAccount("John", "Doe", "61034567890", "PROM_XYZ")
        assert account.balance == 50
    def test_user_age_too_old(self):
        account = PersonalAccount("John", "Doe", "60034567890", "PROM_XYZ")
        assert account.balance == 0
    def test_user_age_1800s(self):
        account = PersonalAccount("John", "Doe", "61834567890", "PROM_XYZ")
        assert account.balance == 0
    def test_user_age_2000s(self):
        account = PersonalAccount("John", "Doe", "60234567890", "PROM_XYZ")
        assert account.balance == 50

class TestTransfer:
    def test_transfer_in(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_in(50)        
        assert account.balance == 100
    def test_transfer_in_negative(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_in(-50)
        assert account.balance == 50
    def test_transfer_in_is_digit(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_in("herofhier")
        assert account.balance == 50
    def test_transfer_out(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_out(50)
        assert account.balance == 0
    def test_transfer_out_negative(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_out(-50)
        assert account.balance == 50
    def test_transfer_out_is_digit(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_out("ouberub")
        assert account.balance == 50
    def test_transfer_out_below_balance(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.transfer_out(100)
        assert account.balance == 50

class TestCompany:
    def test_account_creation(self):
        account = CompanyAccount("company", "0123456789")
        assert account.company_name == "company"
        assert account.nip == "0123456789"
    def test_nip_too_short_(self):
        account = CompanyAccount("company", "012345678")
        assert account.nip == "Invalid"
    def test_nip_too_long(self):
        account = CompanyAccount("company", "01234567890")
        assert account.nip == "Invalid"
    def test_nip_is_digit(self):
        account = CompanyAccount("company", "abcdefghij")
        assert account.nip == "Invalid"

class TestInstantTransfer:
    def test_instant_transfer_personal(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.instant_transfer(30)
        assert account.balance == 19
    def test_instant_transfer_company(self):
        account = CompanyAccount("company", "0123456789")
        account.transfer_in(50)
        account.instant_transfer(30)
        assert account.balance == 15
    def test_instant_transfer_entirety(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.instant_transfer(50)
        assert account.balance == -1
    def test_instant_transfer_negative(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.instant_transfer(-50)
        assert account.balance == 50
    def test_instant_transfer_is_digit(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.instant_transfer("ouberub")
        assert account.balance == 50
    def test_instant_transfer_below_balance(self):
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        account.instant_transfer(51)
        assert account.balance == 50