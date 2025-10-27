class Account:
    def __init__(self):
        self.balance = 0
    def transfer_in(self, ammount):
        if not isinstance(ammount, str) and ammount > 0:
            self.balance += ammount
    def transfer_out(self, ammount):
        if not isinstance(ammount, str) and ammount > 0 and self.balance >= ammount:
            self.balance -= ammount
