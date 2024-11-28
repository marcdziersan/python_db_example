import sqlite3

# Teil 1: Datenbank einrichten
def create_database():
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()

        # Tabelle benutzer erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS benutzer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            age INTEGER
        )''')

        # Tabelle aufgaben erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS aufgaben (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT,
            status TEXT
        )''')
        conn.commit()

def add_default_users():
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()

        # Standard-Datensätze einfügen
        users = [
            ("Alice", "alice@example.com", 30),
            ("Bob", "bob@example.com", 22),
            ("Charlie", "charlie@example.com", 28)
        ]

        cursor.executemany('INSERT INTO benutzer (name, email, age) VALUES (?, ?, ?)', users)
        conn.commit()

# Teil 2: Aufgaben mit Datenbankinteraktion
def read_all_users():
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM benutzer')
        users = cursor.fetchall()
        for user in users:
            print(user)

def add_user():
    name = input("Name: ")
    email = input("E-Mail: ")
    age = int(input("Alter: "))
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO benutzer (name, email, age) VALUES (?, ?, ?)', (name, email, age))
        conn.commit()

def update_user_email():
    user_id = int(input("ID des Benutzers: "))
    new_email = input("Neue E-Mail: ")
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE benutzer SET email = ? WHERE id = ?', (new_email, user_id))
        conn.commit()

def filter_users_by_age():
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM benutzer WHERE age > 25')
        users = cursor.fetchall()
        for user in users:
            print(user)

def search_user_by_name():
    name = input("Name des Benutzers: ")
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM benutzer WHERE name = ?', (name,))
        users = cursor.fetchall()
        for user in users:
            print(user)

# Teil 4: Integration in Python-Anwendungen
def add_task():
    title = input("Titel der Aufgabe: ")
    status = input("Status der Aufgabe (offen/erledigt): ")
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO aufgaben (titel, status) VALUES (?, ?)', (title, status))
        conn.commit()

def show_all_tasks():
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM aufgaben')
        tasks = cursor.fetchall()
        for task in tasks:
            print(task)

def mark_task_done():
    task_id = int(input("ID der Aufgabe: "))
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE aufgaben SET status = ? WHERE id = ?', ("erledigt", task_id))
        conn.commit()

def delete_task():
    task_id = int(input("ID der Aufgabe: "))
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM aufgaben WHERE id = ?', (task_id,))
        conn.commit()

# Hauptmenü
def main():
    create_database()
    add_default_users()

    while True:
        print("""
        Menü:
        1. Alle Benutzer anzeigen
        2. Benutzer hinzufügen
        3. Benutzer aktualisieren (E-Mail)
        4. Benutzer nach Alter filtern
        5. Benutzer nach Name suchen
        6. Aufgabe hinzufügen
        7. Alle Aufgaben anzeigen
        8. Aufgabe als erledigt markieren
        9. Aufgabe löschen
        0. Beenden
        """)
        choice = input("Auswahl: ")
        if choice == "1":
            read_all_users()
        elif choice == "2":
            add_user()
        elif choice == "3":
            update_user_email()
        elif choice == "4":
            filter_users_by_age()
        elif choice == "5":
            search_user_by_name()
        elif choice == "6":
            add_task()
        elif choice == "7":
            show_all_tasks()
        elif choice == "8":
            mark_task_done()
        elif choice == "9":
            delete_task()
        elif choice == "0":
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
