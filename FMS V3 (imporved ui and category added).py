import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("💸 Personal Finance Tracker")
        self.root.geometry("450x500")
        self.root.configure(bg="#f9f9f9")

        self.income = 0
        self.expense_categories = {
            'Food': 0,
            'Rent': 0,
            'Transport': 0,
            'Personal': 0
        }
        self.limit = 0

        # Theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6, background="#4CAF50", foreground="white")
        style.configure("TLabel", font=("Helvetica", 11), background="#f9f9f9")
        style.configure("TEntry", padding=4)

        # Header
        ttk.Label(root, text="💰 Personal Finance Manager", font=("Helvetica", 16, "bold"), foreground="#0066cc").pack(pady=10)

        # Input Frame
        frame = ttk.Frame(root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Income", command=self.add_income).grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="Expense Category:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(frame, textvariable=self.category_var, values=list(self.expense_categories.keys()), state='readonly', width=18)
        self.category_menu.grid(row=2, column=1, padx=5, pady=5)
        self.category_menu.current(0)

        ttk.Button(frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="Set Monthly Limit:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.limit_entry = ttk.Entry(frame, width=20)
        self.limit_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Set Limit", command=self.set_limit).grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(root, text="📊 Show Summary", command=self.show_summary).pack(pady=10)

        self.status_label = ttk.Label(root, text="", foreground="#333333", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

        self.summary_text = tk.Text(root, height=8, width=50, bg="#ffffff", fg="#333333", font=("Helvetica", 10))
        self.summary_text.pack(pady=10)
        self.summary_text.config(state='disabled')

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            self.income += amount
            self.amount_entry.delete(0, tk.END)
            self.update_status(f"✅ Income added: ${amount:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            self.expense_categories[category] += amount
            self.amount_entry.delete(0, tk.END)

            total_expenses = sum(self.expense_categories.values())
            if total_expenses > self.limit > 0:
                messagebox.showwarning("⚠️ Limit Exceeded", "You've exceeded your spending limit!")
            self.update_status(f"❌ Expense added to {category}: ${amount:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def set_limit(self):
        try:
            self.limit = float(self.limit_entry.get())
            self.limit_entry.delete(0, tk.END)
            self.update_status(f"🔒 Limit set to ${self.limit:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def show_summary(self):
        total_expenses = sum(self.expense_categories.values())
        remaining = self.income - total_expenses

        self.summary_text.config(state='normal')
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert(tk.END, f"Total Income: ${self.income:.2f}\n")
        self.summary_text.insert(tk.END, f"Total Expenses: ${total_expenses:.2f}\n")
        self.summary_text.insert(tk.END, f"Remaining Balance: ${remaining:.2f}\n\n")

        for cat, val in self.expense_categories.items():
            self.summary_text.insert(tk.END, f"{cat}: ${val:.2f}\n")

        self.summary_text.config(state='disabled')

        # Pie chart
        labels = list(self.expense_categories.keys())
        values = list(self.expense_categories.values())
        colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99']

        if total_expenses == 0:
            messagebox.showinfo("No Expenses", "No expenses to show in chart.")
            return

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title(f"Expense Distribution\n(Income: ${self.income:.2f})", fontsize=12)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def update_status(self, msg):
        self.status_label.config(text=msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()
