from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

    def log_transaction(self, amount):
        print(f"Transaction logged: {amount} UAH")


class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        print(f"Оплата {amount} грн з кредитної картки ****{self.card_number[-4:]}")
        self.log_transaction(amount)

    def refund(self, amount):
        print(f"Повернення {amount} грн на кредитну картку ****{self.card_number[-4:]}")
        self.log_transaction(amount)


class PayPalPayment(PaymentMethod):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        print(f"Оплата {amount} грн через PayPal ({self.email})")
        self.log_transaction(amount)

    def refund(self, amount):
        print(f"Повернення {amount} грн через PayPal ({self.email})")
        self.log_transaction(amount)


class CryptoPayment(PaymentMethod):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def pay(self, amount):
        print(f"Оплата {amount} грн криптовалютою з гаманця {self.wallet_address}")
        self.log_transaction(amount)

    def refund(self, amount):
        print("Повернення неможливе для криптовалюти")


payments = [
    CreditCardPayment("1234"),
    PayPalPayment("user@example.com"),
    CryptoPayment("0xABCDEF123456")
]

for payment in payments:
    payment.pay(100)
