from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
import pytest

@pytest.fixture
def account():
        account = PersonalAccount("John", "Doe", "01234567890", "PROM_XYZ")
        return account

@pytest.fixture
def company():
    company = CompanyAccount("company", "0123456789")
    return company

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"

    @pytest.mark.parametrize("pesel, expected", [
        ("0123456789", "Invalid"),
        ("012345678901", "Invalid"),
        ("abc34567890", "Invalid")
    ])
    def test_pesel(self, pesel, expected):
        account = PersonalAccount("John", "Doe", pesel)
        assert account.pesel == expected


class TestPromoCode:

    @pytest.mark.parametrize("promo, expected", [
        ("PROM_XYZ", 50),
        ("PKOM_XYZ", 0),
        ("PROM_WXYZ", 0),
        ("PROM_XY", 0)
    ])
    def test_promo_code(self, promo, expected):
        account = PersonalAccount("John", "Doe", "01234567890", promo)
        assert account.balance == expected

class TestUserAge:

    @pytest.mark.parametrize("pesel, expected", [
        ("61034567890", 50),
        ("60034567890", 0),
        ("61834567890", 0),
        ("60234567890", 50)
    ])
    def test_user_age(self, pesel, expected):
        account = PersonalAccount("John", "Doe", pesel, "PROM_XYZ")
        assert account.balance == expected

class TestTransferIn:

    @pytest.mark.parametrize("amount, expected", [
        (50, 100),
        (-50, 50),
        ("herofhier", 50)
    ])
    def test_transfer_in(self, account, amount, expected):
        account.transfer_in(amount)        
        assert account.balance == expected

class TestTransferOut:

    @pytest.mark.parametrize("amount, expected", [
        (50, 0),
        (-50, 50),
        ("ouberub", 50),
        (100, 50)
    ])
    def test_transfer_out(self, account, amount, expected):
        account.transfer_out(amount)
        assert account.balance == expected

class TestCompany:
    def test_account_creation(self, company):
        account = company
        assert account.company_name == "company"
        assert account.nip == "0123456789"
    
    @pytest.mark.parametrize("nip", [
        ("012345678"),
        ("01234567890"),
        ("abcdefghij")
    ])
    def test_nip(self, nip):
        account = CompanyAccount("company", nip)
        assert account.nip == "Invalid"

class TestInstantTransfer:

    @pytest.mark.parametrize("amount, expected", [
        (30, 19),
        (50, -1),
        (-50, 50),
        ("ouberub", 50),
        (51, 50)
    ])
    def test_instant_transfer_personal(self, account, amount, expected):
        account.instant_transfer(amount)
        assert account.balance == expected
    def test_instant_transfer_company(self, company):
        account = company
        account.transfer_in(50)
        account.instant_transfer(30)
        assert account.balance == 15

class TestOperationHistory:
    def test_history_in(self, account):
        account.transfer_in(50)
        assert account.history == [50]
    def test_history_out(self, account):
        account.transfer_out(50)
        assert account.history == [-50]
    def test_history_out_below_balance(self, account):
        account.transfer_out(100)
        assert account.history == []
    def test_history_instant_personal(self, account):
        account.instant_transfer(30)
        assert account.history == [-30, -1]
    def test_history_instant_company(self, company):
        account = company
        account.transfer_in(50)
        account.instant_transfer(30)
        assert account.history == [50, -30, -5]
    def test_history_instant_below_balance(self, account):
        account.instant_transfer(51)
        assert account.history == []
    def test_history_consecutive_transfers(self, account):
        account.transfer_in(500)
        account.instant_transfer(300)
        assert account.history == [500, -300, -1]

class TestPersonalLoan:
    def test_loan_in(self, account):
        account.transfer_in(40)
        account.transfer_in(300)
        account.transfer_in(70)
        assert account.submit_for_loan(100) == True
        assert account.balance == 560
    def test_loan_greater(self, account):
        account.transfer_in(300)
        account.transfer_out(40)
        account.instant_transfer(70)
        account.transfer_out(80)
        assert account.submit_for_loan(100) == True
        assert account.balance == 259
    def test_loan_not_enough_transactions_3(self, account):
        account.transfer_in(300)
        account.transfer_in(40)
        assert account.submit_for_loan(100) == False
        assert account.balance == 390
    def test_loan_3_not_in(self, account):
        account.transfer_out(40)
        account.transfer_in(300)
        account.transfer_in(70)
        assert account.submit_for_loan(100) == False
        assert account.balance == 380
    def test_loan_not_enough_transactions_5(self, account):
        account.transfer_in(300)
        account.transfer_out(40)
        account.instant_transfer(70)
        assert account.submit_for_loan(100) == False
        assert account.balance == 239
    def test_loan_5_not_greater(self, account):
        account.transfer_in(300)
        account.transfer_out(40)
        account.instant_transfer(70)
        account.transfer_out(80)
        assert account.submit_for_loan(110) == False
        assert account.balance == 159

class TestCompanyLoan:

    @pytest.mark.parametrize("amount_in, amount_out, loan, successful, balance", [
        (3000, 1775, 612, True, 1837),
        (2000, 1775, 150, False, 225),
        (2000, 500, 700, False, 1500)
    ])
    def test_loan(self, company, amount_in, amount_out, loan, successful, balance):
        company.transfer_in(amount_in)
        company.transfer_out(amount_out)
        assert company.take_loan(loan) == successful
        assert company.balance == balance