import sqlite3
import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook
import shutil

# === ИНИЦИАЛИЗАЦИЯ БД ===
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    birth_year INTEGER,
    death_year INTEGER,
    cause_of_death TEXT
)''')

cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users VALUES ('admin', 'admin123', 'admin')")
    cursor.execute("INSERT INTO users VALUES ('user', 'user123', 'user')")
conn.commit()

# === ФУНКЦИИ ===
def add_person():
    def save():
        try:
            cursor.execute('''
                INSERT INTO people (first_name, last_name, birth_year, death_year, cause_of_death)
                VALUES (?, ?, ?, ?, ?)
            ''', (fname.get(), lname.get(), int(birth.get()), int(death.get()), cause.get()))
            conn.commit()
            messagebox.showinfo("Успех", "Запись добавлена")
            win.destroy()
            open_main_menu()
        except:
            messagebox.showerror("Ошибка", "Проверьте введённые данные")

    win = tk.Tk()
    win.title("Добавить запись")
    win.geometry("400x300")

    fname = tk.Entry(win)
    lname = tk.Entry(win)
    birth = tk.Entry(win)
    death = tk.Entry(win)
    cause = tk.Entry(win)

    for label, widget in zip(["Имя", "Фамилия", "Год рождения", "Год смерти", "Причина смерти"],
                             [fname, lname, birth, death, cause]):
        tk.Label(win, text=label).pack()
        widget.pack()

    tk.Button(win, text="Сохранить", command=save).pack(pady=10)
    win.mainloop()

def view_all():
    cursor.execute("SELECT * FROM people")
    data = cursor.fetchall()
    result = "\n".join(str(row) for row in data) or "Нет записей."
    messagebox.showinfo("Все записи", result)
    open_main_menu()

def search_by_lastname():
    def find():
        cursor.execute("SELECT * FROM people WHERE last_name = ?", (entry.get(),))
        data = cursor.fetchall()
        with open("search_results.txt", "w", encoding="utf-8") as f:
            for row in data:
                f.write(str(row) + "\n")
        messagebox.showinfo("Результаты поиска", "\n".join(str(r) for r in data) or "Ничего не найдено")
        win.destroy()
        open_main_menu()

    win = tk.Tk()
    win.title("Поиск по фамилии")
    entry = tk.Entry(win)
    tk.Label(win, text="Введите фамилию:").pack()
    entry.pack()
    tk.Button(win, text="Поиск", command=find).pack(pady=10)
    win.mainloop()

def edit_person():
    def update():
        try:
            cursor.execute('''
                UPDATE people SET first_name=?, last_name=?, birth_year=?, death_year=?, cause_of_death=?
                WHERE id=?
            ''', (fname.get(), lname.get(), int(birth.get()), int(death.get()), cause.get(), int(pid.get())))
            conn.commit()
            messagebox.showinfo("Успех", "Запись обновлена")
            win.destroy()
            open_main_menu()
        except:
            messagebox.showerror("Ошибка", "Неверные данные")

    win = tk.Tk()
    win.title("Изменить запись")

    pid = tk.Entry(win)
    fname = tk.Entry(win)
    lname = tk.Entry(win)
    birth = tk.Entry(win)
    death = tk.Entry(win)
    cause = tk.Entry(win)

    for label, widget in zip(["ID", "Имя", "Фамилия", "Год рождения", "Год смерти", "Причина смерти"],
                             [pid, fname, lname, birth, death, cause]):
        tk.Label(win, text=label).pack()
        widget.pack()

    tk.Button(win, text="Обновить", command=update).pack(pady=10)
    win.mainloop()

def delete_by_id():
    def delete():
        try:
            cursor.execute("DELETE FROM people WHERE id=?", (int(entry.get()),))
            conn.commit()
            messagebox.showinfo("Удалено", "Запись удалена")
            win.destroy()
            open_main_menu()
        except:
            messagebox.showerror("Ошибка", "ID должен быть числом")

    win = tk.Tk()
    win.title("Удаление по ID")
    entry = tk.Entry(win)
    tk.Label(win, text="Введите ID для удаления:").pack()
    entry.pack()
    tk.Button(win, text="Удалить", command=delete).pack(pady=10)
    win.mainloop()

def delete_by_lastname():
    def delete():
        lastname = entry.get()
        cursor.execute("DELETE FROM people WHERE last_name=?", (lastname,))
        conn.commit()
        messagebox.showinfo("Удалено", "Удалены все записи с фамилией: " + lastname)
        win.destroy()
        open_main_menu()

    win = tk.Tk()
    win.title("Удаление по фамилии")
    entry = tk.Entry(win)
    tk.Label(win, text="Введите фамилию для удаления:").pack()
    entry.pack()
    tk.Button(win, text="Удалить", command=delete).pack(pady=10)
    win.mainloop()

def export_to_excel():
    cursor.execute("SELECT * FROM people")
    rows = cursor.fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "People"
    ws.append(["ID", "Имя", "Фамилия", "Год рождения", "Год смерти", "Причина смерти"])
    for row in rows:
        ws.append(row)

    wb.save("people_export.xlsx")
    messagebox.showinfo("Экспорт", "Данные экспортированы в people_export.xlsx")
    open_main_menu()

def backup_database():
    shutil.copy("users.db", "backup_users.db")
    messagebox.showinfo("Резервная копия", "Файл backup_users.db создан")
    open_main_menu()

# === ГЛАВНОЕ МЕНЮ ===
def open_main_menu():
    menu = tk.Tk()
    menu.title("Главное меню")
    menu.attributes("-fullscreen", True)

    frame = tk.Frame(menu)
    frame.pack(pady=50)

    if user_role == "admin":
        tk.Button(frame, text="Добавить запись", width=30, height=2, command=lambda: [menu.destroy(), add_person()]).pack(pady=5)
        tk.Button(frame, text="Изменить запись", width=30, height=2, command=lambda: [menu.destroy(), edit_person()]).pack(pady=5)
        tk.Button(frame, text="Удалить по ID", width=30, height=2, command=lambda: [menu.destroy(), delete_by_id()]).pack(pady=5)
        tk.Button(frame, text="Удалить по фамилии", width=30, height=2, command=lambda: [menu.destroy(), delete_by_lastname()]).pack(pady=5)

    tk.Button(frame, text="Посмотреть все записи", width=30, height=2, command=lambda: [menu.destroy(), view_all()]).pack(pady=5)
    tk.Button(frame, text="Поиск по фамилии", width=30, height=2, command=lambda: [menu.destroy(), search_by_lastname()]).pack(pady=5)

    if user_role == "admin":
        tk.Button(frame, text="Экспорт в Excel", width=30, height=2, command=lambda: [menu.destroy(), export_to_excel()]).pack(pady=5)
        tk.Button(frame, text="Резервная копия БД", width=30, height=2, command=lambda: [menu.destroy(), backup_database()]).pack(pady=5)

    tk.Button(frame, text="Выйти", width=30, height=2, command=menu.destroy).pack(pady=10)
    menu.mainloop()

# === АВТОРИЗАЦИЯ ===
def start_login():
    global root
    root = tk.Tk()
    root.title("Авторизация")
    root.attributes("-fullscreen", True)

    login_frame = tk.Frame(root)
    login_frame.pack(pady=100)

    tk.Label(login_frame, text="Логин:").pack()
    login_entry = tk.Entry(login_frame)
    login_entry.pack()

    tk.Label(login_frame, text="Пароль:").pack()
    pass_entry = tk.Entry(login_frame, show="*")
    pass_entry.pack()

    def do_login():
        global user_role
        login = login_entry.get()
        password = pass_entry.get()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (login, password))
        result = cursor.fetchone()
        if result:
            user_role = result[0]
            root.destroy()
            open_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    tk.Button(login_frame, text="Войти", command=do_login).pack(pady=20)
    root.mainloop()

# === СТАРТ ===
user_role = None
start_login()
conn.close()
