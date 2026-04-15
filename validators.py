from datetime import datetime

def validate_id(prompt):
    try:
        value = int(input(prompt))
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print("ID must be a positive number!")
        return None


def validate_price(prompt):
    try:
        value = float(input(prompt))
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print("Price must be a positive number!")
        return None


def validate_quantity(prompt):
    try:
        value = int(input(prompt))
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print("Quantity must be a positive integer!")
        return None


def validate_expiry_date(prompt):
    value = input(prompt)
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return value   # keep as string
    except ValueError:
        print("Invalid date format! Use DD.MM.YYYY")
        return None
