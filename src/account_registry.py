from src.personal_account import PersonalAccount

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        if isinstance(account, PersonalAccount):
            self.accounts.append(account)
    
    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11 and pesel.isdigit()

    def search(self, pesel):
        if self.is_pesel_valid(pesel):
            for account in self.accounts:
                if account.pesel == pesel:
                    return account
        return None

    def return_all(self):
        return self.accounts

    def count(self):
        return len(self.accounts)