class Account:
    def __init__(self, first_name, last_name, pesel, promo=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        if len(pesel) == 11 and pesel.isdigit():
            self.pesel = pesel
        else:
            self.pesel = "Invalid"
        if promo and len(promo) == 8 and promo[:5] == "PROM_":
            self.balance += 50
