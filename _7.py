from abc import ABC, abstractmethod
from datetime import datetime


# Абстрактний клас
class FileSystemObject(ABC):
    def __init__(self, name, path, size):
        self.__name = name
        self.__path = path
        self.__created_at = datetime.now()
        self.__size = size

    # Інкапсуляція через property
    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__path

    @property
    def created_at(self):
        return self.__created_at

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        if value >= 0:
            self.__size = value
        else:
            print("Розмір не може бути від’ємним!")

    # Абстрактний метод
    @abstractmethod
    def get_info(self):
        pass


# Загальний файл
class File(FileSystemObject):
    def __init__(self, name, path, size, extension):
        super().__init__(name, path, size)
        self.__extension = extension

    @property
    def extension(self):
        return self.__extension

    def get_info(self):
        return (f"Файл: {self.name}.{self.extension}\n"
                f"Шлях: {self.path}\n"
                f"Розмір: {self.size} байт")


# Текстовий файл
class TextFile(File):
    def __init__(self, name, path, size, content):
        super().__init__(name, path, size, "txt")
        self.__content = content

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    def get_info(self):
        return (f"Текстовий файл: {self.name}.txt\n"
                f"Шлях: {self.path}\n"
                f"Розмір: {self.size} байт\n"
                f"Вміст: {self.content}")


# Графічний файл
class ImageFile(File):
    def __init__(self, name, path, size, width, height):
        super().__init__(name, path, size, "png")
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def get_info(self):
        return (f"Графічний файл: {self.name}.png\n"
                f"Шлях: {self.path}\n"
                f"Розмір: {self.size} байт\n"
                f"Роздільна здатність: {self.width}x{self.height}")


# Папка
class Folder(FileSystemObject):
    def __init__(self, name, path):
        super().__init__(name, path, 0)
        self.__objects = []

    @property
    def objects(self):
        return self.__objects

    # Додавання об'єкта в папку
    def add_object(self, obj):
        self.__objects.append(obj)

    def get_info(self):
        info = (f"Папка: {self.name}\n"
                f"Шлях: {self.path}\n"
                f"Кількість об'єктів: {len(self.objects)}\n")

        for obj in self.objects:
            info += "\n---\n" + obj.get_info()

        return info


# ======================
# Приклад використання
# ======================

# Створення файлів
text_file = TextFile(
    "notes",
    "/documents",
    120,
    "Це текстовий файл"
)

image_file = ImageFile(
    "photo",
    "/images",
    2048,
    1920,
    1080
)

# Створення папки
folder = Folder("MyFolder", "/home/user")

# Додавання об'єктів
folder.add_object(text_file)
folder.add_object(image_file)

# Вивід інформації
print(text_file.get_info())
print("\n====================\n")
print(image_file.get_info())
print("\n====================\n")
print(folder.get_info())
