from abc import ABC, abstractmethod

class Account:
    def __init__(self):
        self.balance = 0
    @abstractmethod
    def instant_fee(self):
        pass
    def transfer_in(self, ammount):
        if self.ammount_valid(ammount):
            self.balance += ammount
        #""" Abstract method, doesn't need testing """
    def transfer_out(self, ammount):
        if self.ammount_valid(ammount) and self.balance >= ammount:
            self.balance -= ammount
    def instant_transfer(self, ammount):
        if self.ammount_valid(ammount) and self.balance >= ammount:
            self.balance -= ammount + self.instant_fee()
    def ammount_valid(self, ammount):
        return not isinstance(ammount, str) and ammount > 0
