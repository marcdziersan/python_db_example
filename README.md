# Aufgaben-Manager

Ein einfaches Python-Projekt zum Verwalten von Benutzern und Aufgaben mithilfe von SQLite.

## Funktionen

Die Anwendung bietet folgende Funktionen:

### Benutzerverwaltung
1. **Alle Benutzer anzeigen**: Zeigt eine Liste aller Benutzer in der Datenbank an.
2. **Benutzer hinzufügen**: Fügt einen neuen Benutzer zur Datenbank hinzu.
3. **Benutzer aktualisieren**: Aktualisiert die E-Mail-Adresse eines Benutzers basierend auf seiner ID.
4. **Benutzer nach Alter filtern**: Zeigt alle Benutzer an, deren Alter über einem bestimmten Wert liegt.
5. **Benutzer nach Name suchen**: Sucht nach Benutzern anhand ihres Namens.

### Aufgabenverwaltung
6. **Aufgabe hinzufügen**: Fügt eine neue Aufgabe mit Titel und Status (offen/erledigt) hinzu.
7. **Alle Aufgaben anzeigen**: Zeigt eine Liste aller Aufgaben in der Datenbank an.
8. **Aufgabe als erledigt markieren**: Aktualisiert den Status einer Aufgabe zu "erledigt".
9. **Aufgabe löschen**: Löscht eine Aufgabe basierend auf ihrer ID.

### Allgemein
- Die Daten werden in einer SQLite-Datenbank (`aufgaben.db`) gespeichert.
- Standard-Benutzer werden beim ersten Start automatisch zur Datenbank hinzugefügt.

## Aufbau der Datenbank

Die Anwendung verwendet SQLite mit zwei Tabellen:

Tabelle: benutzer

Spalte	Typ	Beschreibung
- id	INTEGER	Eindeutige ID des Benutzers
- name	TEXT	Name des Benutzers
- email	TEXT	E-Mail-Adresse des Benutzers
- age	INTEGER	Alter des Benutzers

Tabelle: aufgaben

Spalte	Typ	Beschreibung
- id	INTEGER	Eindeutige ID der Aufgabe
- titel	TEXT	Titel der Aufgabe
-  status	TEXT	Status der Aufgabe (offen/erledigt)
