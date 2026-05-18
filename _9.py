from abc import ABC, abstractmethod
from datetime import datetime
import copy


# ==========================================
# Абстрактний клас
# ==========================================
class FileSystemObject(ABC):

    def __init__(self, name, path, size=0):

        self.__name = name
        self.__path = path
        self.__size = size
        self.__created_at = datetime.now()

    # -------------------------
    # Properties
    # -------------------------
    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def size(self):
        return self.__size

    @property
    def created_at(self):
        return self.__created_at

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @size.setter
    def size(self, value):

        if value < 0:
            raise ValueError("Розмір не може бути від’ємним!")

        self.__size = value

    # -------------------------
    # Методи
    # -------------------------
    def rename(self, new_name):
        self.__name = new_name

    def copy(self):
        return copy.deepcopy(self)

    @abstractmethod
    def get_info(self):
        pass


# ==========================================
# Файл
# ==========================================
class File(FileSystemObject):

    def __init__(self, name, path, size, extension):

        super().__init__(name, path, size)

        self.__extension = extension

    @property
    def extension(self):
        return self.__extension

    def get_info(self):
        return f"{self.name}.{self.extension} ({self.size} байт)"


# ==========================================
# Текстовий файл
# ==========================================
class TextFile(File):

    def __init__(self, name, path, content=""):

        super().__init__(name, path, len(content), "txt")

        self.__content = content

    # -------------------------
    # Читання файлу
    # -------------------------
    def read(self):
        return self.__content

    # -------------------------
    # Запис у файл
    # -------------------------
    def write(self, text):

        self.__content += text

        self.size = len(self.__content)

    def get_info(self):

        return (
            f"Текстовий файл: {self.name}.txt\n"
            f"Розмір: {self.size} байт"
        )


# ==========================================
# Графічний файл
# ==========================================
class ImageFile(File):

    def __init__(self, name, path, size, width, height):

        super().__init__(name, path, size, "png")

        self.__width = width
        self.__height = height

    def get_info(self):

        return (
            f"Зображення: {self.name}.png\n"
            f"Роздільна здатність: "
            f"{self.__width}x{self.__height}"
        )


# ==========================================
# Папка
# ==========================================
class Folder(FileSystemObject):

    def __init__(self, name, path):

        super().__init__(name, path)

        self.__objects = []

    @property
    def objects(self):
        return self.__objects

    # -------------------------
    # Додавання об'єкта
    # -------------------------
    def add_object(self, obj):

        for existing in self.__objects:

            if existing.name == obj.name:
                raise ValueError(
                    f"Об'єкт '{obj.name}' вже існує!"
                )

        self.__objects.append(obj)

    # -------------------------
    # Видалення
    # -------------------------
    def remove_object(self, name):

        for obj in self.__objects:

            if obj.name == name:
                self.__objects.remove(obj)
                return

        raise ValueError(
            f"Об'єкт '{name}' не знайдено!"
        )

    # -------------------------
    # Показ вмісту
    # -------------------------
    def show_contents(self):

        if not self.__objects:
            print("Папка порожня")
            return

        for obj in self.__objects:
            print(obj.get_info())
            print("-" * 30)

    # -------------------------
    # Розмір папки
    # -------------------------
    def calculate_size(self):

        total = 0

        for obj in self.__objects:

            if isinstance(obj, Folder):
                total += obj.calculate_size()
            else:
                total += obj.size

        return total

    def get_info(self):

        return (
            f"Папка: {self.name}\n"
            f"Об'єктів: {len(self.__objects)}\n"
            f"Розмір: {self.calculate_size()} байт"
        )


# ==========================================
# FileManager
# ==========================================
class FileManager:

    def __init__(self):

        self.root = Folder("root", "/")

    # -------------------------
    # Створення папки
    # -------------------------
    def create_folder(self, name):

        folder = Folder(name, "/")

        self.root.add_object(folder)

    # -------------------------
    # Створення текстового файлу
    # -------------------------
    def create_text_file(self, name, content):

        file = TextFile(name, "/", content)

        self.root.add_object(file)

    # -------------------------
    # Пошук об'єкта
    # -------------------------
    def find_object(self, name):

        for obj in self.root.objects:

            if name.lower() in obj.name.lower():
                return obj

        return None

    # -------------------------
    # Видалення
    # -------------------------
    def delete_object(self, name):

        self.root.remove_object(name)

    # -------------------------
    # Перейменування
    # -------------------------
    def rename_object(self, old_name, new_name):

        obj = self.find_object(old_name)

        if obj:
            obj.rename(new_name)
        else:
            raise ValueError(
                "Об'єкт не знайдено!"
            )

    # -------------------------
    # Копіювання
    # -------------------------
    def copy_object(self, name):

        obj = self.find_object(name)

        if not obj:
            raise ValueError(
                "Об'єкт не знайдено!"
            )

        copied = obj.copy()

        copied.rename(obj.name + "_copy")

        self.root.add_object(copied)

    # -------------------------
    # Переміщення
    # -------------------------
    def move_object(self, name, folder_name):

        obj = self.find_object(name)

        target = self.find_object(folder_name)

        if not obj:
            raise ValueError(
                "Об'єкт не знайдено!"
            )

        if not target or not isinstance(target, Folder):
            raise ValueError(
                "Папка призначення не знайдена!"
            )

        self.root.remove_object(name)

        target.add_object(obj)

    # -------------------------
    # Показ файлової системи
    # -------------------------
    def show_file_system(self):

        self.root.show_contents()


# ==========================================
# Консольне меню
# ==========================================
def menu():

    manager = FileManager()

    while True:

        print("\n===== ФАЙЛОВИЙ МЕНЕДЖЕР =====")
        print("1. Створити папку")
        print("2. Створити текстовий файл")
        print("3. Показати вміст")
        print("4. Пошук об'єкта")
        print("5. Перейменувати")
        print("6. Видалити")
        print("7. Копіювати")
        print("8. Перемістити")
        print("9. Читати файл")
        print("10. Записати у файл")
        print("0. Вихід")

        choice = input("Ваш вибір: ")

        try:

            # -------------------------
            # Створення папки
            # -------------------------
            if choice == "1":

                name = input("Назва папки: ")

                manager.create_folder(name)

                print("Папка створена!")

            # -------------------------
            # Створення файлу
            # -------------------------
            elif choice == "2":

                name = input("Назва файлу: ")

                content = input("Вміст файлу: ")

                manager.create_text_file(
                    name,
                    content
                )

                print("Файл створений!")

            # -------------------------
            # Показ вмісту
            # -------------------------
            elif choice == "3":

                manager.show_file_system()

            # -------------------------
            # Пошук
            # -------------------------
            elif choice == "4":

                name = input(
                    "Введіть назву для пошуку: "
                )

                obj = manager.find_object(name)

                if obj:
                    print(obj.get_info())
                else:
                    print("Нічого не знайдено!")

            # -------------------------
            # Перейменування
            # -------------------------
            elif choice == "5":

                old_name = input("Стара назва: ")

                new_name = input("Нова назва: ")

                manager.rename_object(
                    old_name,
                    new_name
                )

                print("Об'єкт перейменовано!")

            # -------------------------
            # Видалення
            # -------------------------
            elif choice == "6":

                name = input(
                    "Назва об'єкта: "
                )

                manager.delete_object(name)

                print("Об'єкт видалено!")

            # -------------------------
            # Копіювання
            # -------------------------
            elif choice == "7":

                name = input(
                    "Назва об'єкта: "
                )

                manager.copy_object(name)

                print("Об'єкт скопійовано!")

            # -------------------------
            # Переміщення
            # -------------------------
            elif choice == "8":

                obj_name = input(
                    "Назва об'єкта: "
                )

                folder_name = input(
                    "Назва папки: "
                )

                manager.move_object(
                    obj_name,
                    folder_name
                )

                print("Об'єкт переміщено!")

            # -------------------------
            # Читання файлу
            # -------------------------
            elif choice == "9":

                name = input("Назва файлу: ")

                obj = manager.find_object(name)

                if isinstance(obj, TextFile):

                    print("\nВміст файлу:")
                    print(obj.read())

                else:
                    print("Файл не знайдено!")

            # -------------------------
            # Запис у файл
            # -------------------------
            elif choice == "10":

                name = input("Назва файлу: ")

                obj = manager.find_object(name)

                if isinstance(obj, TextFile):

                    text = input("Текст: ")

                    obj.write(text)

                    print("Дані записано!")

                else:
                    print("Файл не знайдено!")

            # -------------------------
            # Вихід
            # -------------------------
            elif choice == "0":

                print("Вихід із програми...")
                break

            else:
                print("Невірний вибір!")

        except Exception as error:
            print(f"Помилка: {error}")


# ==========================================
# Запуск програми
# ==========================================
menu()
