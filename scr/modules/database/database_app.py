import tkinter as tk
import sqlite3
import csv
import os
from tkinter import messagebox, filedialog
from tkinter.simpledialog import askstring

class SQLiteQueryTool:
    def __init__(self, database_path=None):
        self.database_path = database_path
        self.save_button = None

        self.window = tk.Tk()
        self.window.title("SQLite Query Tool")
        self.window.geometry("1080x720")

        self.select_button = tk.Button(self.window, text="Datenbank auswählen", command=self.select_database_file)
        self.select_button.pack()

        self.database_label = tk.Label(self.window, text="")
        self.database_label.pack()

        self.sql_entry = tk.Text(self.window, height=5)
        self.sql_entry.pack(fill=tk.BOTH, expand=True)

        self.execute_button = tk.Button(self.window, text="Ausführen", command=self.execute_sql)
        self.execute_button.pack()

        self.result_text = tk.Text(self.window, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.update_database_label()

    def select_database_file(self):
        self.database_path = filedialog.askopenfilename(filetypes=[("SQLite-Datenbankdateien", "*.db")])
        self.update_database_label()

    def update_database_label(self):
        if self.database_path:
            self.database_label.config(text=f"Ausgewählte Datenbank: {self.database_path}")
        else:
            self.database_label.config(text="Keine Datenbank ausgewählt")

    def execute_sql(self):
        if not self.database_path:
            messagebox.showwarning("Datenbank fehlt", "Bitte wählen Sie eine Datenbank aus.")
            return

        sql = self.sql_entry.get("1.0", tk.END)

        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            self.result_text.delete("1.0", tk.END)
            for row in result:
                self.result_text.insert(tk.END, str(row) + "\n")

            if self.save_button:
                self.save_button.pack_forget()

            self.save_button = tk.Button(self.window, text="Speichern", command=lambda: self.save_csv(result, sql))
            self.save_button.pack()

        except sqlite3.Error as e:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Fehler: " + str(e))

        conn.close()

    def save_csv(self, result, sql):
        if not os.path.exists("Outputs"):
            os.makedirs("Outputs")

        filename = askstring("Dateinamen eingeben", "Bitte geben Sie den Dateinamen ein:", initialvalue=sql)

        if filename:
            filename = filename.replace(" ", "_")
            output_path = os.path.join("Outputs", f"{filename}.csv")
            with open(output_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(result)

            messagebox.showinfo("Speichern", f"Die Ausgabe wurde erfolgreich gespeichert:\n{output_path}")
        else:
            messagebox.showinfo("Speichern", "Die Ausgabe wurde nicht gespeichert.")

    def run(self):
        self.window.mainloop()
