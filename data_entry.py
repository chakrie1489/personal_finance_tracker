from datetime import datetime

Categories = {"I": "Income", "E": "Expense"}

def date_in(msg_inpt,enbl_default=False):
    date_str = input(msg_inpt)
    if enbl_default and not date_str:
        return datetime.now().strftime("%d-%m-%Y")
    try:
        date_validation = datetime.strptime(date_str, "%d-%m-%Y")
        return date_validation.strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please enter date in dd-mm-yyyy format")
        return date_in(msg_inpt,enbl_default)


def amnt_in():
    try:
        amnt_str = float(input("Enter the amount:"))
        if amnt_str <= 0:
           raise ValueError("Amount cannot be negative, Plase try again")
        return amnt_str
    except ValueError as e:
        print(e)
        return amnt_in()

def cat_in():
    cat_str = input("Enter the Category ('I' for income and 'E' for expense):").upper()
    if cat_str in Categories:
        return Categories[cat_str]
    else:
        print("Invalid category. Please try again using 'I' for income and 'E' for expense")
        return cat_in()

def dcrpt_in():
    dcrpt_str = input("Enter the description(Optional):")
    return dcrpt_str