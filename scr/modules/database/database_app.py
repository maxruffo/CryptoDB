import tkinter as tk
import sqlite3
import csv
import os
from tkinter import messagebox, filedialog
from tkinter.simpledialog import askstring

def execute_sql():
    global save_button  # Deklaration als globale Variable

    # SQL-Befehl aus dem Textfeld abrufen
    sql = sql_entry.get("1.0", tk.END)

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    try:
        # SQL-Befehl ausführen
        cursor.execute(sql)
        result = cursor.fetchall()

        # Ergebnis im Textfeld anzeigen
        result_text.delete("1.0", tk.END)
        for row in result:
            result_text.insert(tk.END, str(row) + "\n")

        # Vorherigen Speichern-Button entfernen, falls vorhanden
        if save_button is not None:
            save_button.pack_forget()

        # Speichern-Button hinzufügen
        save_button = tk.Button(window, text="Speichern", command=lambda: save_csv(result, sql))
        save_button.pack()

    except sqlite3.Error as e:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Fehler: " + str(e))

    # Verbindung zur Datenbank schließen
    conn.close()

def save_csv(result, sql):
    # Ordner 'Outputs' erstellen, falls nicht vorhanden
    if not os.path.exists("Outputs"):
        os.makedirs("Outputs")

    # Benutzernamen für die CSV-Datei abfragen
    filename = askstring("Dateinamen eingeben", "Bitte geben Sie den Dateinamen ein:", initialvalue=sql)

    if filename:
        # Leerzeichen durch Unterstriche ersetzen
        filename = filename.replace(" ", "_")

        # CSV-Datei speichern
        output_path = os.path.join("Outputs", f"{filename}.csv")
        with open(output_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(result)

        messagebox.showinfo("Speichern", f"Die Ausgabe wurde erfolgreich gespeichert:\n{output_path}")
    else:
        messagebox.showinfo("Speichern", "Die Ausgabe wurde nicht gespeichert.")

def select_database_file():
    global database_file
    database_file = filedialog.askopenfilename(filetypes=[("SQLite-Datenbankdateien", "*.db")])
    database_label.config(text=f"Ausgewählte Datenbank: {database_file}")

# GUI erstellen
window = tk.Tk()
window.title("SQLite Query Tool")
window.geometry("1080x720")

# Datenbankdatei auswählen
select_button = tk.Button(window, text="Datenbank auswählen", command=select_database_file)
select_button.pack()

# Label für ausgewählte Datenbank
database_label = tk.Label(window, text="Keine Datenbank ausgewählt")
database_label.pack()

# SQL-Eingabefeld
sql_entry = tk.Text(window, height=5)
sql_entry.pack(fill=tk.BOTH, expand=True)

# Ausführen-Button
execute_button = tk.Button(window, text="Ausführen", command=execute_sql)
execute_button.pack()

# Ergebnis-Anzeige
result_text = tk.Text(window, height=10)
result_text.pack(fill=tk.BOTH, expand=True)

#Speichern-Button
save_button = None

#Gui Starten
window.mainloop()
