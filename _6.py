from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotifier(Notifier):
    def __init__(self, email: str):
        self.email = email

    def send(self, message: str):
        print(f"[EMAIL] {self.email}: {message}")


class SMSNotifier(Notifier):
    def __init__(self, phone: str):
        self.phone = phone

    def send(self, message: str):
        print(f"[SMS] {self.phone}: {message}")


class TelegramNotifier(Notifier):
    def __init__(self, username: str):
        self.username = username

    def send(self, message: str):
        print(f"[TELEGRAM] @{self.username}: {message}")


class NotificationManager:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def set_notifier(self, notifier: Notifier):
        self.notifier = notifier

    def notify(self, message: str):
        self.notifier.send(message)


email = EmailNotifier("user@gmail.com")
sms = SMSNotifier("+380501112233")
telegram = TelegramNotifier("my_user")

manager = NotificationManager(email)
manager.notify("Hello Email")

manager.set_notifier(sms)
manager.notify("Hello SMS")

manager.set_notifier(telegram)
manager.notify("Hello Telegram")