from collections import UserDict
from datetime import datetime, date

class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Поле імені не може бути порожнім.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.validate_phone(new_value):
            raise ValueError("Неправильний формат номеру телефону.")
        self._value = new_value

    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value:
            try:
                datetime.strptime(new_value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Неправильний формат дня народження.")
        self._value = new_value

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Номер телефону {old_phone} не існує в записі.")

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

    def days_to_birthday(self):
        if self.birthday.value:
            today = date.today()
            birthday_date = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
            next_birthday = date(today.year, birthday_date.month, birthday_date.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, birthday_date.month, birthday_date.day)
            days_remaining = (next_birthday - today).days
            return days_remaining

    def __str__(self):
        return f"Контакт: {self.name.value}, телефони: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, batch_size=10):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i + batch_size]

book = AddressBook()
john_record = Record("Джон", "1234567890", birthday="1990-04-15")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Джейн", "9876543210")
book.add_record(jane_record)

john = book.find("Джон")
print(f"Днів до наступного дня народження Джона: {john.days_to_birthday()} днів")

for batch in book.iterator(batch_size=1):
    for record in batch:
        print(record)
