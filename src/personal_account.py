from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        if len(pesel) == 11 and pesel.isdigit():
            self.pesel = pesel
        else:
            self.pesel = "Invalid"
        if self.is_promo_valid(promo):
            self.balance += 50
    def is_promo_valid(self, promo):
        return promo and len(promo) == 8 and promo[:5] == "PROM_" and self.is_user_not_too_old()
    def is_user_not_too_old(self):
        return (int(self.pesel[:2]) > 60 and self.pesel[2] == "0") or self.pesel[2] in ["2", "4", "6"]
    def instant_fee(self):
        return 1
    def last_3_were_in(self):
        if len(self.history) >= 3:
            for i in range(-3, 0):
                if self.history[i] < 0:
                    return False
            return True
        return False
    def last_5_bigger_than_loan(self, amount):
        return len(self.history) >= 5 and sum(self.history[-5:]) > amount
    def can_submit_for_loan(self, amount):
        return self.last_3_were_in() or self.last_5_bigger_than_loan(amount)
    def submit_for_loan(self, amount):
        if self.can_submit_for_loan(amount):
            self.balance += amount
            return True
        return False