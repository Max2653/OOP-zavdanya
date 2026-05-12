class FuelStation:
    def __init__(self, max_volume, fuel_balance, fuel_price):
        self.max_volume = max_volume          # максимальний обʼєм
        self.fuel_balance = fuel_balance      # баланс пального
        self.cars_count = 0                   # кількість заправлених авто
        self.fuel_price = fuel_price          # ціна за 1 літр
        self.money = 0                        # зароблені кошти
        self.sold_fuel = 0                    # реалізоване пальне

    # конструктор копіювання
    @classmethod
    def copy(cls, other):
        new_obj = cls(
            other.max_volume,
            other.fuel_balance,
            other.fuel_price
        )
        new_obj.cars_count = other.cars_count
        new_obj.money = other.money
        new_obj.sold_fuel = other.sold_fuel
        return new_obj

    # заправити авто
    def refuel_car(self, liters):
        if liters > self.fuel_balance:
            print("Недостатньо пального в колонці!")
        else:
            self.fuel_balance -= liters
            self.cars_count += 1
            self.sold_fuel += liters
            self.money += liters * self.fuel_price
            print(f"Авто заправлено на {liters} л")

    # поповнити запас пального
    def add_fuel(self, liters):
        if self.fuel_balance + liters > self.max_volume:
            print("Неможливо додати стільки пального!")
        else:
            self.fuel_balance += liters
            print(f"Додано {liters} л пального")

    # інформація
    def show_info(self):
        print("Зароблено коштів:", self.money)
        print("Реалізовано пального:", self.sold_fuel, "л")
        print("Заправлено авто:", self.cars_count)


# -------------------
# Приклад використання

station = FuelStation(1000, 500, 55)

station.refuel_car(50)
station.refuel_car(600)

station.add_fuel(200)

station.show_info()

# копія обʼєкта
station2 = FuelStation.copy(station)

print("\nДані копії:")
station2.show_info()
