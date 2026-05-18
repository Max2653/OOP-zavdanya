from abc import ABC, abstractmethod
from datetime import datetime
import copy


# =========================
# Абстрактний клас
# =========================
class FileSystemObject(ABC):
    def __init__(self, name, path, size=0):
        self.__name = name
        self.__path = path
        self.__created_at = datetime.now()
        self.__size = size
        self.__deleted = False

    # -----------------
    # Properties
    # -----------------
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

    @property
    def deleted(self):
        return self.__deleted

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @path.setter
    def path(self, new_path):
        self.__path = new_path

    # -----------------
    # Методи
    # -----------------
    def rename(self, new_name):
        self.__name = new_name

    def delete(self):
        self.__deleted = True

    def copy(self):
        return copy.deepcopy(self)

    @abstractmethod
    def get_info(self):
        pass


# =========================
# Клас File
# =========================
class File(FileSystemObject):
    def __init__(self, name, path, size, extension):
        super().__init__(name, path, size)
        self.__extension = extension

    @property
    def extension(self):
        return self.__extension

    def get_info(self):
        return f"Файл: {self.name}.{self.extension}"


# =========================
# Текстовий файл
# =========================
class TextFile(File):
    def __init__(self, name, path, content):
        size = len(content)
        super().__init__(name, path, size, "txt")
        self.__content = content

    @property
    def content(self):
        return self.__content

    def get_info(self):
        return (
            f"Текстовий файл: {self.name}.txt\n"
            f"Розмір: {self.size} байт\n"
            f"Вміст: {self.content}"
        )


# =========================
# Графічний файл
# =========================
class ImageFile(File):
    def __init__(self, name, path, size, width, height):
        super().__init__(name, path, size, "png")
        self.__width = width
        self.__height = height

    def get_info(self):
        return (
            f"Зображення: {self.name}.png\n"
            f"Роздільна здатність: {self.__width}x{self.__height}"
        )


# =========================
# Папка
# =========================
class Folder(FileSystemObject):
    def __init__(self, name, path):
        super().__init__(name, path)
        self.__objects = []

    @property
    def objects(self):
        return self.__objects

    # -----------------
    # Додавання об'єкта
    # -----------------
    def add_object(self, obj):

        # Перевірка однакових назв
        for existing in self.__objects:
            if existing.name == obj.name:
                raise ValueError(
                    f"Об'єкт з назвою '{obj.name}' вже існує!"
                )

        self.__objects.append(obj)

    # -----------------
    # Видалення об'єкта
    # -----------------
    def remove_object(self, name):
        for obj in self.__objects:
            if obj.name == name:
                self.__objects.remove(obj)
                obj.delete()
                return

        raise ValueError(f"Об'єкт '{name}' не знайдено!")

    # -----------------
    # Показати вміст
    # -----------------
    def show_contents(self):
        if not self.__objects:
            print("Папка порожня")
            return

        for obj in self.__objects:
            print(obj.get_info())

    def get_info(self):
        return (
            f"Папка: {self.name}\n"
            f"Кількість об'єктів: {len(self.__objects)}"
        )


# =========================
# FileManager
# =========================
class FileManager:
    def __init__(self):
        self.root = Folder("root", "/")

    # -----------------
    # Створення папки
    # -----------------
    def create_folder(self, folder_name, parent_folder=None):

        if parent_folder is None:
            parent_folder = self.root

        folder = Folder(folder_name, parent_folder.path)
        parent_folder.add_object(folder)

        return folder

    # -----------------
    # Створення текстового файлу
    # -----------------
    def create_text_file(self, name, content, parent_folder=None):

        if parent_folder is None:
            parent_folder = self.root

        file = TextFile(name, parent_folder.path, content)
        parent_folder.add_object(file)

        return file

    # -----------------
    # Пошук об'єкта
    # -----------------
    def find_object(self, name, folder=None):

        if folder is None:
            folder = self.root

        for obj in folder.objects:

            if obj.name == name:
                return obj

            if isinstance(obj, Folder):
                found = self.find_object(name, obj)

                if found:
                    return found

        return None

    # -----------------
    # Видалення
    # -----------------
    def delete_object(self, name):

        obj = self.find_object(name)

        if not obj:
            raise ValueError("Об'єкт не існує!")

        self._delete_from_folder(self.root, name)

    def _delete_from_folder(self, folder, name):

        for obj in folder.objects:

            if obj.name == name:
                folder.remove_object(name)
                return True

            if isinstance(obj, Folder):

                if self._delete_from_folder(obj, name):
                    return True

        return False

    # -----------------
    # Перейменування
    # -----------------
    def rename_object(self, old_name, new_name):

        obj = self.find_object(old_name)

        if not obj:
            raise ValueError("Об'єкт не знайдено!")

        obj.rename(new_name)

    # -----------------
    # Копіювання
    # -----------------
    def copy_object(self, object_name, target_folder):

        obj = self.find_object(object_name)

        if not obj:
            raise ValueError("Об'єкт не знайдено!")

        copied = obj.copy()

        # Перевірка дублювання
        copied.rename(copied.name + "_copy")

        target_folder.add_object(copied)

    # -----------------
    # Переміщення
    # -----------------
    def move_object(self, object_name, target_folder):

        obj = self.find_object(object_name)

        if not obj:
            raise ValueError("Об'єкт не знайдено!")

        # Заборона переміщення папки в саму себе
        if isinstance(obj, Folder):

            if obj == target_folder:
                raise ValueError(
                    "Неможливо перемістити папку в саму себе!"
                )

        # Видаляємо зі старої папки
        self._delete_from_folder(self.root, object_name)

        # Додаємо в нову
        target_folder.add_object(obj)


# =====================================
# Демонстрація роботи програми
# =====================================

manager = FileManager()

# Створення папок
docs = manager.create_folder("Documents")
images = manager.create_folder("Images")

# Створення файлів
file1 = manager.create_text_file(
    "notes",
    "Привіт, це текстовий файл!",
    docs
)

image1 = ImageFile(
    "photo",
    "/Images",
    2048,
    1920,
    1080
)

images.add_object(image1)

# Показ вмісту
print("=== Documents ===")
docs.show_contents()

print("\n=== Images ===")
images.show_contents()

# Копіювання
manager.copy_object("notes", images)

print("\n=== Images після копіювання ===")
images.show_contents()

# Перейменування
manager.rename_object("notes", "new_notes")

print("\n=== Documents після перейменування ===")
docs.show_contents()

# Переміщення
manager.move_object("new_notes", images)

print("\n=== Images після переміщення ===")
images.show_contents()

# Видалення
manager.delete_object("photo")

print("\n=== Images після видалення ===")
images.show_contents()
