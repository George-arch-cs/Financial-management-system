import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ModernBank:
    def __init__(self, root):
        self.root = root
        self.root.title("Sonova Bank – Digital Wallet")
        self.root.geometry("1000x700")
        self.root.configure(bg="#faf9f6")

        self.users = {}
        self.current_user = None
        # For demo, create some categories for expenses
        self.expense_categories = ['Food', 'Rent', 'Transport', 'Personal']

        # balance history for line chart: {user: [(datetime, balance), ...]}
        self.balance_history = {}

        self.setup_styles()
        self.login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#faf9f6")
        style.configure("TLabel", background="#faf9f6", font=("Times New Roman", 12))
        style.configure("TButton", font=("Times New Roman", 12, "bold"), background="#0070f3", foreground="white")
        style.map("TButton", background=[("active", "#005bb5")])
        style.configure("TNotebook", background="#faf9f6")
        style.configure("TNotebook.Tab", font=("Times New Roman", 12, "bold"), padding=[10, 5])

    def login_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        ttk.Label(self.root, text="Welcome to Sonova Bank 🌺", font=("Times New Roman", 24, "bold"), foreground="#0070f3", background="#faf9f6").pack(pady=60)

        frame = ttk.Frame(self.root)
        frame.pack()

        ttk.Label(frame, text="Enter Username:", font=("Times New Roman", 14)).grid(row=0, column=0, padx=10, pady=15)
        self.user_entry = ttk.Entry(frame, width=30, font=("Times New Roman", 14))
        self.user_entry.grid(row=0, column=1, padx=10, pady=15)

        ttk.Label(frame, text="Enter PIN:", font=("Times New Roman", 14)).grid(row=1, column=0, padx=10, pady=15)
        self.pin_entry = ttk.Entry(frame, width=30, show="*", font=("Times New Roman", 14))
        self.pin_entry.grid(row=1, column=1, padx=10, pady=15)

        ttk.Button(frame, text="Login / Register", command=self.authenticate).grid(row=2, column=0, columnspan=2, pady=30, ipadx=20, ipady=5)

    def authenticate(self):
        user = self.user_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not user or not pin:
            messagebox.showerror("Login Failed", "Please fill in both fields.")
            return

        if user not in self.users:
            # New user registration
            self.users[user] = {
                "pin": pin,
                "balance": 0.0,
                "transactions": [],
                "expense_summary": {cat: 0.0 for cat in self.expense_categories}
            }
            self.balance_history[user] = []
        elif self.users[user]["pin"] != pin:
            messagebox.showerror("Login Failed", "Incorrect PIN.")
            return

        self.current_user = user
        # Initialize balance history if not existing
        if user not in self.balance_history:
            self.balance_history[user] = []
        # Log initial balance time for graph
        if not self.balance_history[user]:
            self.balance_history[user].append((datetime.now(), self.users[user]["balance"]))
        self.show_dashboard()

    def show_dashboard(self):
        for w in self.root.winfo_children():
            w.destroy()

        # Top welcome + balance
        ttk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Times New Roman", 24, "bold"), background="#faf9f6").pack(pady=15)
        balance = self.users[self.current_user]["balance"]
        ttk.Label(self.root, text=f"💰 Current Balance: ${balance:.2f}", font=("Times New Roman", 20, "bold"), foreground="#16a34a", background="#faf9f6").pack(pady=5)

        # Tabs setup
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Banking tab
        banking_tab = ttk.Frame(notebook)
        notebook.add(banking_tab, text="Banking")

        self.add_funds_ui(banking_tab)
        self.send_payment_ui(banking_tab)
        self.add_expense_ui(banking_tab)

        # Transactions tab
        transactions_tab = ttk.Frame(notebook)
        notebook.add(transactions_tab, text="Transactions")
        self.transactions_ui(transactions_tab)

        # Summary tab
        summary_tab = ttk.Frame(notebook)
        notebook.add(summary_tab, text="Summary & Analysis")
        self.summary_ui(summary_tab)

    def add_funds_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="Add Funds", padding=10)
        frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(frame, text="Amount ($):", font=("Times New Roman", 14)).grid(row=0, column=0, sticky="w")
        self.add_funds_amt = ttk.Entry(frame, font=("Times New Roman", 14))
        self.add_funds_amt.grid(row=0, column=1, padx=10, pady=5)

        def add():
            try:
                amt = float(self.add_funds_amt.get())
                if amt <= 0:
                    raise ValueError("Amount must be positive")
                self.users[self.current_user]["balance"] += amt
                self.log_transaction(f"Added funds: ${amt:.2f}")
                self.balance_history[self.current_user].append((datetime.now(), self.users[self.current_user]["balance"]))
                messagebox.showinfo("Success", f"${amt:.2f} added to your wallet.")
                self.add_funds_amt.delete(0, tk.END)
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid amount: {e}")

        ttk.Button(frame, text="Add Funds", command=add).grid(row=0, column=2, padx=10, pady=5)

    def send_payment_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="Send Payment", padding=10)
        frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(frame, text="Recipient Username:", font=("Times New Roman", 14)).grid(row=0, column=0, sticky="w")
        self.recipient_entry = ttk.Entry(frame, font=("Times New Roman", 14))
        self.recipient_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Amount ($):", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w")
        self.send_amt_entry = ttk.Entry(frame, font=("Times New Roman", 14))
        self.send_amt_entry.grid(row=1, column=1, padx=10, pady=5)

        def send():
            recipient = self.recipient_entry.get().strip()
            try:
                amount = float(self.send_amt_entry.get())
                if recipient not in self.users:
                    messagebox.showerror("Error", "Recipient not found.")
                    return
                if amount <= 0:
                    raise ValueError("Amount must be positive")
                if self.users[self.current_user]['balance'] < amount:
                    messagebox.showwarning("Insufficient Funds", "Not enough balance.")
                    return
                self.users[self.current_user]['balance'] -= amount
                self.users[recipient]['balance'] += amount
                self.log_transaction(f"Sent ${amount:.2f} to {recipient}")
                self.users[recipient]['transactions'].append(f"Received ${amount:.2f} from {self.current_user}")
                self.balance_history[self.current_user].append((datetime.now(), self.users[self.current_user]['balance']))
                messagebox.showinfo("Payment Sent", f"${amount:.2f} sent to {recipient}.")
                self.recipient_entry.delete(0, tk.END)
                self.send_amt_entry.delete(0, tk.END)
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        ttk.Button(frame, text="Send Payment", command=send).grid(row=2, column=0, columnspan=2, pady=10)

    def add_expense_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="Add Expense", padding=10)
        frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(frame, text="Amount ($):", font=("Times New Roman", 14)).grid(row=0, column=0, sticky="w")
        self.expense_amt_entry = ttk.Entry(frame, font=("Times New Roman", 14))
        self.expense_amt_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame, text="Category:", font=("Times New Roman", 14)).grid(row=1, column=0, sticky="w")
        self.expense_category_var = tk.StringVar()
        categories = self.expense_categories
        category_menu = ttk.Combobox(frame, textvariable=self.expense_category_var, values=categories, state="readonly", font=("Times New Roman", 14))
        category_menu.grid(row=1, column=1, padx=10, pady=5)
        category_menu.current(0)

        def add_expense():
            try:
                amt = float(self.expense_amt_entry.get())
                if amt <= 0:
                    raise ValueError("Amount must be positive")
                if self.users[self.current_user]['balance'] < amt:
                    messagebox.showwarning("Insufficient Funds", "Not enough balance.")
                    return
                category = self.expense_category_var.get()
                self.users[self.current_user]['balance'] -= amt
                self.users[self.current_user]["expense_summary"][category] += amt
                self.log_transaction(f"Expense: ${amt:.2f} for {category}")
                self.balance_history[self.current_user].append((datetime.now(), self.users[self.current_user]["balance"]))
                messagebox.showinfo("Success", f"Expense of ${amt:.2f} recorded under {category}.")
                self.expense_amt_entry.delete(0, tk.END)
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        ttk.Button(frame, text="Add Expense", command=add_expense).grid(row=2, column=0, columnspan=2, pady=10)

    def transactions_ui(self, parent):
        ttk.Label(parent, text="Transaction History", font=("Times New Roman", 16, "bold")).pack(pady=15)
        txt = tk.Text(parent, font=("Times New Roman", 12), wrap="word")
        txt.pack(expand=True, fill="both", padx=20, pady=10)
        history = self.users[self.current_user]['transactions']
        if not history:
            txt.insert("1.0", "No transactions yet.")
        else:
            txt.insert("1.0", "\n".join(history))
        txt.config(state="disabled")

    def summary_ui(self, parent):
        ttk.Label(parent, text="Summary & Analysis", font=("Times New Roman", 16, "bold")).pack(pady=15)

        notebook = ttk.Notebook(parent)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Pie chart tab
        pie_tab = ttk.Frame(notebook)
        notebook.add(pie_tab, text="Expenses Pie Chart")

        exp_summary = self.users[self.current_user]["expense_summary"]
        labels = list(exp_summary.keys())
        sizes = [exp_summary[k] for k in labels]

        fig1, ax1 = plt.subplots(figsize=(5, 5))
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        if sum(sizes) == 0:
            ax1.text(0.5, 0.5, "No expenses to display", ha='center', va='center', fontsize=14)
        else:
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        ax1.axis('equal')
        ax1.set_title('Expenses by Category', fontsize=16)

        canvas1 = FigureCanvasTkAgg(fig1, master=pie_tab)
        canvas1.draw()
        canvas1.get_tk_widget().pack(padx=20, pady=20)

        # Line chart tab
        line_tab = ttk.Frame(notebook)
        notebook.add(line_tab, text="Balance History")

        hist = self.balance_history.get(self.current_user, [])
        if hist:
            dates, balances = zip(*hist)
        else:
            dates, balances = [], []

        fig2, ax2 = plt.subplots(figsize=(7, 4))
        if dates and balances:
            ax2.plot(dates, balances, marker='o', linestyle='-', color='blue')
            ax2.set_title('Balance Over Time', fontsize=16)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Balance ($)')
            fig2.autofmt_xdate()
        else:
            ax2.text(0.5, 0.5, "No balance history available", ha='center', va='center', fontsize=14)

        canvas2 = FigureCanvasTkAgg(fig2, master=line_tab)
        canvas2.draw()
        canvas2.get_tk_widget().pack(padx=20, pady=20)

    def log_transaction(self, text):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{time}] {text}"
        self.users[self.current_user]['transactions'].append(entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBank(root)
    root.mainloop()
