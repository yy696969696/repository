import tkinter as tk
from tkinter import ttk
import sqlite3


class EmployeeManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список сотрудников компании")

        # Создаем базу данных SQLite и таблицу
        self.conn = sqlite3.connect("employees.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                phone_number TEXT,
                email TEXT,
                salary REAL
            )
        """
        )
        self.conn.commit()

        # Создаем и настраиваем интерфейс
        self.create_gui()

    def create_gui(self):
        # Фрейм для отображения списка сотрудников
        self.employee_frame = ttk.LabelFrame(self.root, text="Сотрудники")
        self.employee_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        # Создаем и настраиваем Treeview для отображения списка сотрудников
        self.tree = ttk.Treeview(
            self.employee_frame, columns=("ID", "ФИО", "Телефон", "Email", "Зарплата")
        )
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="ФИО")
        self.tree.heading("#3", text="Телефон")
        self.tree.heading("#4", text="Email")
        self.tree.heading("#5", text="Зарплата")
        self.tree.pack(fill="both", expand="yes")

        # Заполняем Treeview данными из базы данных
        self.refresh_employee_list()

        # Фрейм для добавления/изменения сотрудников
        self.entry_frame = ttk.LabelFrame(
            self.root, text="Добавить/Изменить сотрудника"
        )
        self.entry_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        self.full_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.salary_var = tk.DoubleVar()

        ttk.Label(self.entry_frame, text="ФИО:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.entry_frame, textvariable=self.full_name_var).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Label(self.entry_frame, text="Телефон:").grid(
            row=1, column=0, padx=5, pady=5
        )
        ttk.Entry(self.entry_frame, textvariable=self.phone_var).grid(
            row=1, column=1, padx=5, pady=5
        )
        ttk.Label(self.entry_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.entry_frame, textvariable=self.email_var).grid(
            row=2, column=1, padx=5, pady=5
        )
        ttk.Label(self.entry_frame, text="Зарплата:").grid(
            row=3, column=0, padx=5, pady=5
        )
        ttk.Entry(self.entry_frame, textvariable=self.salary_var).grid(
            row=3, column=1, padx=5, pady=5
        )

        self.add_button = ttk.Button(
            self.entry_frame, text="Добавить", command=self.add_employee
        )
        self.add_button.grid(row=4, column=0, padx=5, pady=5)
        self.update_button = ttk.Button(
            self.entry_frame, text="Изменить", command=self.update_employee
        )
        self.update_button.grid(row=4, column=1, padx=5, pady=5)

        # Фрейм для поиска сотрудника
        self.search_frame = ttk.LabelFrame(self.root, text="Поиск сотрудника")
        self.search_frame.pack(padx=10, pady=10, fill="both", expand="yes")

        self.search_var = tk.StringVar()
        ttk.Label(self.search_frame, text="Поиск по ФИО:").grid(
            row=0, column=0, padx=5, pady=5
        )
        ttk.Entry(self.search_frame, textvariable=self.search_var).grid(
            row=0, column=1, padx=5, pady=5
        )
        search_button = ttk.Button(
            self.search_frame, text="Найти", command=self.search_employee
        )
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Удаление сотрудника
        delete_button = ttk.Button(
            self.root,
            text="Удалить выбранного сотрудника",
            command=self.delete_employee,
        )
        delete_button.pack(padx=10, pady=10)

        # Обработка события выбора сотрудника в Treeview
        self.tree.bind("<<TreeviewSelect>>", self.on_employee_select)

    def refresh_employee_list(self):
        # Очистка Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Запрос данных из базы данных и добавление их в Treeview
        self.cursor.execute("SELECT * FROM employees")
        employees = self.cursor.fetchall()
        for employee in employees:
            self.tree.insert("", "end", values=employee)

    def add_employee(self):
        full_name = self.full_name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        salary = self.salary_var.get()

        if full_name and phone and email:
            self.cursor.execute(
                "INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)",
                (full_name, phone, email, salary),
            )
            self.conn.commit()
            self.refresh_employee_list()
            self.clear_entry_fields()
        else:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")

    def update_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            id = self.tree.item(selected_item)["values"][0]
            full_name = self.full_name_var.get()
            phone = self.phone_var.get()
            email = self.email_var.get()
            salary = self.salary_var.get()

            if full_name and phone and email:
                self.cursor.execute(
                    "UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?",
                    (full_name, phone, email, salary, id),
                )
                self.conn.commit()
                self.refresh_employee_list()
                self.clear_entry_fields()
                tk.messagebox.showinfo("Успех", "Данные сотрудника обновлены")
            else:
                tk.messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")

    def search_employee(self):
        search_term = self.search_var.get()
        if search_term:
            self.tree.delete(*self.tree.get_children())  # Очищаем Treeview
            self.cursor.execute(
                "SELECT * FROM employees WHERE full_name LIKE ?",
                ("%" + search_term + "%",),
            )
            employees = self.cursor.fetchall()
            for employee in employees:
                self.tree.insert("", "end", values=employee)

    def delete_employee(self):
        selected_item = self.tree.selection()
        if selected_item:
            id = self.tree.item(selected_item)["values"][0]
            self.cursor.execute("DELETE FROM employees WHERE id=?", (id,))
            self.conn.commit()
            self.refresh_employee_list()

    def on_employee_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            employee = self.tree.item(selected_item)["values"]
            self.full_name_var.set(employee[1])
            self.phone_var.set(employee[2])
            self.email_var.set(employee[3])
            self.salary_var.set(employee[4])

    def clear_entry_fields(self):
        self.full_name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.salary_var.set(0.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementApp(root)
    root.mainloop()
