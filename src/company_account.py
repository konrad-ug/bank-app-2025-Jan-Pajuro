from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        if len(nip) == 10 and nip.isdigit():
            self.nip = nip
        else:
            self.nip = "Invalid"
    def instant_fee(self):
        return 5
    def take_loan(self, amount):
        if -1775 in self.history and self.balance >= 2 * amount:
            self.balance += amount
            return True
        return False