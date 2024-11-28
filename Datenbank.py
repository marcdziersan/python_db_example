import sqlite3
import hashlib

# Funktion zum Hashen von Passwörtern
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Teil 1: Datenbank einrichten
def create_database():
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()

        # Tabelle benutzer erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS benutzer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'User'
        )''')

        # Tabelle aufgaben erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS aufgaben (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT,
            status TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES benutzer(id)
        )''')

        # Admin-Benutzer hinzufügen, falls nicht vorhanden
        cursor.execute('SELECT * FROM benutzer WHERE email = ?', ('admin@example.com',))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO benutzer (name, email, password, role) VALUES (?, ?, ?, ?)',
                ('Admin', 'admin@example.com', hash_password('admin123'), 'Admin')
            )

        conn.commit()

# Funktion zur Registrierung eines neuen Benutzers
def register():
    print("=== Registrierung ===")
    name = input("Name: ")
    email = input("E-Mail: ")
    password = input("Passwort: ")
    hashed_password = hash_password(password)

    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO benutzer (name, email, password) VALUES (?, ?, ?)',
                (name, email, hashed_password)
            )
            conn.commit()
            print("Registrierung erfolgreich! Bitte melden Sie sich an.")
        except sqlite3.IntegrityError:
            print("Diese E-Mail-Adresse wird bereits verwendet.")

# Funktion zur Anmeldung eines Benutzers
def login():
    print("=== Anmeldung ===")
    email = input("E-Mail: ")
    password = input("Passwort: ")
    hashed_password = hash_password(password)

    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, role, password FROM benutzer WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user and user[3] == hashed_password:
            print(f"Willkommen, {user[1]}!")
            return {"id": user[0], "name": user[1], "role": user[2]}
        else:
            print("E-Mail oder Passwort ist falsch.")
            return None

# Funktionen für Aufgabenverwaltung durch Benutzer/Admin
def add_task(user):
    print("=== Aufgabe hinzufügen ===")
    title = input("Titel der Aufgabe: ")
    status = input("Status der Aufgabe (offen/erledigt): ")

    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO aufgaben (titel, status, user_id) VALUES (?, ?, ?)',
            (title, status, user["id"])
        )
        conn.commit()
        print("Aufgabe hinzugefügt.")

def show_user_tasks(user):
    print("=== Ihre Aufgaben ===")
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, titel, status FROM aufgaben WHERE user_id = ?', (user["id"],))
        tasks = cursor.fetchall()
        for task in tasks:
            print(f"{task[0]}: {task[1]} ({task[2]})")

def edit_user_task(user):
    print("=== Aufgabe bearbeiten ===")
    show_user_tasks(user)
    task_id = int(input("ID der zu bearbeitenden Aufgabe: "))
    title = input("Neuer Titel (leer lassen, um unverändert zu lassen): ")
    status = input("Neuer Status (offen/erledigt, leer lassen, um unverändert zu lassen): ")

    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        if title:
            cursor.execute('UPDATE aufgaben SET titel = ? WHERE id = ? AND user_id = ?', (title, task_id, user["id"]))
        if status:
            cursor.execute('UPDATE aufgaben SET status = ? WHERE id = ? AND user_id = ?', (status, task_id, user["id"]))
        if cursor.rowcount > 0:
            conn.commit()
            print("Aufgabe aktualisiert.")
        else:
            print("Aufgabe nicht gefunden oder Sie sind nicht berechtigt.")

def delete_user_task(user):
    print("=== Aufgabe löschen ===")
    show_user_tasks(user)
    task_id = int(input("ID der zu löschenden Aufgabe: "))

    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM aufgaben WHERE id = ? AND user_id = ?', (task_id, user["id"]))
        if cursor.rowcount > 0:
            conn.commit()
            print("Aufgabe gelöscht.")
        else:
            print("Aufgabe nicht gefunden oder Sie sind nicht berechtigt.")

# Admin-spezifische Funktionen
def admin_manage_users():
    print("=== Benutzerverwaltung ===")
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, role FROM benutzer')
        users = cursor.fetchall()
        for user in users:
            print(f"{user[0]}: {user[1]}, {user[2]}, Rolle: {user[3]}")

def admin_manage_tasks():
    print("=== Aufgabenverwaltung ===")
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT aufgaben.id, aufgaben.titel, aufgaben.status, benutzer.name '
                       'FROM aufgaben LEFT JOIN benutzer ON aufgaben.user_id = benutzer.id')
        tasks = cursor.fetchall()
        for task in tasks:
            print(f"{task[0]}: {task[1]} ({task[2]}) - Zugewiesen an: {task[3]}")

def change_user_details(user):
    print("=== Profildaten ändern ===")
    new_name = input(f"Aktueller Name: {user['name']}. Neuer Name (leer lassen, um nicht zu ändern): ")
    new_email = input(f"Aktuelle E-Mail: {user['email']}. Neue E-Mail (leer lassen, um nicht zu ändern): ")
    new_password = input("Neues Passwort (leer lassen, um nicht zu ändern): ")
    # Update-Logik
    with sqlite3.connect('aufgaben.db') as conn:
        cursor = conn.cursor()
        if new_name:
            cursor.execute('UPDATE benutzer SET name = ? WHERE id = ?', (new_name, user["id"]))
            user["name"] = new_name  # Update des Benutzernamens im User-Objekt
        if new_email:
            cursor.execute('UPDATE benutzer SET email = ? WHERE id = ?', (new_email, user["id"]))
            user["email"] = new_email  # Update der Benutzer-E-Mail im User-Objekt
        if new_password:
            hashed_password = hash_password(new_password)
            cursor.execute('UPDATE benutzer SET password = ? WHERE id = ?', (hashed_password, user["id"]))
            print("Passwort wurde geändert.")
        conn.commit()
        print("Profildaten wurden erfolgreich aktualisiert.")

def admin_menu(user):
    while True:
        print("""
        === Admin-Bereich ===
        1. Benutzer verwalten
        2. Alle Aufgaben anzeigen
        3. Eigene Aufgaben anzeigen
        4. Eigene Aufgabe hinzufügen
        5. Eigene Aufgabe bearbeiten
        6. Eigene Aufgabe löschen
        0. Zurück
        """)
        choice = input("Auswahl: ")
        if choice == "1":
            admin_manage_users()
        elif choice == "2":
            admin_manage_tasks()
        elif choice == "3":
            show_user_tasks(user)
        elif choice == "4":
            add_task(user)
        elif choice == "5":
            edit_user_task(user)
        elif choice == "6":
            delete_user_task(user)
        elif choice == "0":
            break
        else:
            print("Ungültige Auswahl.")

# Hauptmenü
def main():
    create_database()

    print("Willkommen! Bitte registrieren oder anmelden:")
    print("1. Registrieren")
    print("2. Anmelden")
    choice = input("Auswahl: ")

    user = None
    if choice == "1":
        register()
    elif choice == "2":
        user = login()

    if not user:
        return

    if user["role"] == "Admin":
        admin_menu(user)
    else:
        while True:
            print("""
            Menü:
            1. Aufgaben anzeigen
            2. Aufgabe hinzufügen
            3. Aufgabe bearbeiten
            4. Aufgabe löschen
            5. Profildaten ändern
            0. Abmelden
            """)
            choice = input("Auswahl: ")
            if choice == "1":
                show_user_tasks(user)
            elif choice == "2":
                add_task(user)
            elif choice == "3":
                edit_user_task(user)
            elif choice == "4":
                delete_user_task(user)
            elif choice == "5":
                change_user_details(user)
            elif choice == "0":
                print("Abgemeldet.")
                break
            else:
                print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()
