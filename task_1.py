from collections import UserDict


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""

    def __init__(self, value: str):
        if not value or not value.strip():
            raise ValueError("Ім'я контакту не може бути порожнім.")
        super().__init__(value.strip())


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (рівно 10 цифр)."""

    def __init__(self, value: str):
        if not self._is_valid(value):
            raise ValueError("Номер телефону повинен складатися рівно з 10 цифр.")
        super().__init__(value)

    @staticmethod
    def _is_valid(value: str) -> bool:
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Record:
    """Клас для зберігання інформації про контакт, включно з іменем та списком телефонів."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        """Додає новий номер телефону до запису."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Видаляє номер телефону із запису."""
        phone_obj = self.find_phone(phone_number)
        if phone_obj is None:
            raise ValueError(f"Номер телефону {phone_number} не знайдено.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Редагує існуючий номер телефону, замінюючи його на новий."""
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError(f"Номер телефону {old_phone} не знайдено.")
        # Спочатку валідуємо новий номер через створення об'єкта Phone
        validated_new_phone = Phone(new_phone)
        phone_obj.value = validated_new_phone.value

    def find_phone(self, phone_number: str) -> Phone | None:
        """Шукає об'єкт Phone за значенням номера. Повертає Phone або None."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання записів (Record) та керування ними."""

    def add_record(self, record: Record) -> None:
        """Додає запис до адресної книги (ключ — ім'я контакту)."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Знаходить запис за ім'ям. Повертає Record або None."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за ім'ям, якщо він існує."""
        if name in self.data:
            del self.data[name]


# Перевірка роботи згідно з прикладом із завдання:
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
