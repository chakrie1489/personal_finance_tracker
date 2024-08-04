import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from data_entry import date_in, amnt_in, cat_in, dcrpt_in

class csv_file :
    filename =  "expenses_data.csv"
    clmns = ["Date","Amount","Category","Description"]
    @classmethod
    def create_csv(cls):
        try:
            pd.read_csv(cls.filename)
        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.clmns)
            df.to_csv(cls.filename,index=False)

    @classmethod
    def data_entry (cls,date,amount,category,description):
        data_entry = {"Date":date,"Amount":amount,"Category": category,"Description":description} 
        with open(cls.filename, mode = "a", newline = "") as csvfile:
            write= csv.DictWriter(csvfile,fieldnames = cls.clmns)
            write.writerow(data_entry)
        print("Data entered successfully")    

    @classmethod
    def get_transactions (cls,start_date,end_date):
        df = pd.read_csv(cls.filename)
        df["Date"] = pd.to_datetime(df["Date"],format = "%d-%m-%Y")
        start_date = datetime.strptime(start_date,"%d-%m-%Y")
        end_date = datetime.strptime(end_date,"%d-%m-%Y")
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        df_filtered = df.loc[mask]

        if df_filtered.empty:
            print("No transactions found in this range")
        else:
            print(f"Transactions from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
            print(df_filtered.to_string(index=False, formatters={"Date": lambda x: x.strftime("%d-%m-%Y")}))

        total_income = df_filtered[df_filtered["Category"] == "Income"]["Amount"].sum()   
        total_expense = df_filtered[df_filtered["Category"] == "Expense"]["Amount"].sum()
        print("\n SUMMARY")
        print(f"Total Income: ₹{total_income:.2f}")
        print(f"Total Expense: ₹{total_expense:.2f}")
        print(f"Net Balance: ₹{(total_income - total_expense):.2f}")


def add_data():
    csv_file.create_csv()
    date = date_in("Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date:",enbl_default = True)
    amount = amnt_in()
    category = cat_in()
    description = dcrpt_in()
    csv_file.data_entry(date,amount,category,description)
    
def plot_data(df):
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")
    df.set_index("Date",inplace = True)
    
    income_df = df[df["Category"] == "Income"].resample("D").sum().reindex(df.index,fill_value = 0)
    expense_df = df[df["Category"] == "Expense"].resample("D").sum().reindex(df.index,fill_value = 0)
    
    plt.figure(figsize=(8,5))
    plt.plot(income_df.index,income_df["Amount"],label = "Income", color = "g")
    plt.plot(expense_df.index,expense_df["Amount"],label = "Expense", color = "r")
    plt.ylabel("Amount")
    plt.xlabel("Date")
    plt.title("Income vs Expense")
    plt.legend()
    plt.grid(True)
    plt.show()

    

def main():
    while True:
        print("\n1. Add a transaction")
        print("2. Get transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice:")
        if choice == "1":
            add_data()
        elif choice == "2":
            start_date = date_in("Enter the start date of the transactions (dd-mm-yyyy):")
            end_date = date_in("Enter the end date of the transactions (dd-mm-yyyy):")
            csv_file.get_transactions(start_date,end_date)
            if input("Do you want to plot the data? (y/n)").lower() == "y":
                df = pd.read_csv(csv_file.filename)
                plot_data(df)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again")

if __name__ == "__main__":
    main()