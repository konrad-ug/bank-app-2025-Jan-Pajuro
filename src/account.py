from abc import ABC, abstractmethod

class Account:
    def __init__(self):
        self.balance = 0
        self.history = []
    @abstractmethod
    def instant_fee(self):
        """ Abstract method, doesn't need testing """
    def transfer_in(self, amount):
        if self.ammount_valid(amount):
            self.balance += amount
            self.history.append(amount)
    def transfer_out(self, amount):
        if self.ammount_valid(amount) and self.balance >= amount:
            self.balance -= amount
            self.history.append(-amount)
    def instant_transfer(self, amount):
        if self.ammount_valid(amount) and self.balance >= amount:
            self.balance -= amount + self.instant_fee()
            self.history.extend([-amount, -self.instant_fee()])
    def ammount_valid(self, amount):
        return not isinstance(amount, str) and amount > 0
