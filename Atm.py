import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="root",  
    database="atm_db"
)

cursor = conn.cursor()

# Function to get or create account
def get_or_create_account(account_number):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Account exists: return balance
    else:
        cursor.execute("INSERT INTO accounts (account_number, balance) VALUES (%s, %s)", (account_number, 0))
        conn.commit()
        return 0  # New account with zero balance

# Function to update balance in DB
def update_balance(account_number, new_balance):
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
    conn.commit()

# Input and validate account number
while True:
    account_number = input("🏦 Enter your account number (11 to 18 digits): ")
    if account_number.isdigit() and 11 <= len(account_number) <= 18:
        balance = get_or_create_account(account_number)
        break
    else:
        print("❌ Invalid account number. Please try again.")

# Account class
class Account:
    def __init__(self, acc, bal):
        self.acc = acc
        self.bal = bal

    def debit(self, amount):
        if amount > self.bal:
            print("❌ Insufficient balance.")
        else:
            self.bal -= amount
            update_balance(self.acc, self.bal)
            print(f"✅ Rs. {amount} debited.")
        print(f"💰 Current balance: Rs. {self.get_balance()}")

    def credit(self, amount):
        self.bal += amount
        update_balance(self.acc, self.bal)
        print(f"✅ Rs. {amount} credited.")
        print(f"💰 Current balance: Rs. {self.get_balance()}")

    def get_balance(self):
        return self.bal

    def display_info(self):
        print("\n🧾 Account Summary:")
        print("Account Number:", self.acc)
        print("Current Balance: Rs.", self.bal)

# Create account object
acc1 = Account(account_number, balance)

# ATM menu loop
while True:
    print("\n🔘 Choose Transaction:")
    print("1. Credit")
    print("2. Debit")
    print("3. View Balance")
    print("4. Exit")

    choice = input("➡️ Enter your choice (1-4): ")

    if choice == '1':
        amount = int(input("💵 Enter amount to credit: "))
        acc1.credit(amount)
    elif choice == '2':
        amount = int(input("💸 Enter amount to debit: "))
        acc1.debit(amount)
    elif choice == '3':
        acc1.display_info()
    elif choice == '4':
        print("👋 Thank you for using our ATM!")
        break
    else:
        print("❌ Invalid choice. Please try again.")

# Close MySQL connection
cursor.close()
conn.close()
