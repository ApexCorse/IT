import uuid
import socket
from tkinter import Tk, LabelFrame, NO, CENTER, Scrollbar, messagebox, StringVar, Button, Toplevel
from tkinter.ttk import Combobox, Label, Style, Treeview
from ttkthemes import ThemedStyle
import sys
from os import path


class SecondWindow(Toplevel):
    """Class to open different window at the same time"""

    def __init__(self, parent, title, geometry, propagate, b):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)
        self.propagate(propagate)
        self.resizable(0, 0)
        self.iconbitmap(resource_path("icon.ico"))



def resource_path(relative_path):
    """ Restituisce il path assoluto, compatibile con PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)


def info_app(self):
    """Termini e Condizioni d'Uso"""
    info_window = SecondWindow(self, "Info App", "720x150", False, (0, 0))
    style = ThemedStyle(info_window)
    style.theme_use("clearlooks")
    font = int(10 * (self.winfo_vrootwidth() / self.winfo_vrootheight()) / (800 / 670))
    text_info = "Questo programma è stato creato dal TeamIT " \
                "per conto di Salvatore Alessi. Lo scopo è comunicare gli utenti attivi "\
                "per quanto riguarda le licenze di Adams e Ansys. Si nota che solo alcuni pc "\
                "possono essere abilitati all'uso di tale programma e per farlo si dovrà contattare "\
                "il Team IT."
    info_label = Label(info_window,
                       text=text_info,
                       font=("Spectral", font), wraplength=700, justify="left",
                       foreground="black")
    info_label.grid(row=0, column=0, columnspan=2, rowspan=2, padx=5, pady=(10, 5), sticky="w")



class ConnectedUsers(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Utenti Attivi - Licenze")
        self.geometry("600x550")
        self.iconbitmap(resource_path("icon.ico"))
        self.style = ThemedStyle(self)
        self.style.theme_use("clearlooks")  

        self.filter_var = StringVar(value="Tutti")

        filter_label = Label(self, text="Filtro:", font=("Lucida Console", 12))
        filter_label.place(relx=0.01, rely=0.05)

        filter_combo = Combobox(self, textvariable=self.filter_var, state="readonly",
                               values=["Tutti", "ADAMS", "ANSYS"], font=("Lucida Console", 12))
        filter_combo.place(relx=0.15, rely=0.05, width=150)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_tree())

        refresh_button = Button(self, text="Aggiorna", command=self.refresh_tree, font=("Lucida Console", 12))
        refresh_button.place(relx=0.75, rely=0.045, width=100, height=35)


        self.container = LabelFrame(self, text="Utenti Connessi")
        self.container.place(height=340 * self.winfo_vrootheight() / 670, width=300 * self.winfo_vrootwidth() / 800,
                             relx=0.01, rely=0.15)
        self.h_container = 340 * self.winfo_vrootheight() / 670
        self.w_container = 300 * self.winfo_vrootwidth() / 800

        self.tree_licenze = None
        self.tree_licenze_lavorazione_scrolly = None
        self.create_tree_licenze()

        self.dict_days = {
            "Mon": "Lun",
            "Tue": "Mar",
            "Wed": "Mer",
            "Thu": "Gio",
            "Fri": "Ven",
            "Sat": "Sab",
            "Sun": "Dom"
        }

        w_factor = self.winfo_vrootwidth() / 800
        h_factor = self.winfo_vrootheight() / 670
        credit = Button(self, text="©teamit", relief="flat", command=lambda: info_app(self))
        credit.place(height=20 * h_factor, width=50 * w_factor, relx=0.4, rely=0.95)
        

    def create_tree_licenze(self):
        """Crea l'Albero per visionare le licenze"""

        tree_style = Style()
        tree_style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                             font=('Lucida Console', 12))  # Font corpo
        tree_style.configure("mystyle.Treeview.Heading", font=('Lucida Console', 14, "italic"), pady=15)  # Header font
        tree_style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Senza bordi
        tree_style.configure('Treeview', rowheight=35)

        self.tree_licenze = Treeview(self.container, style="mystyle.Treeview", selectmode="extended")
        self.tree_licenze["columns"] = ("Type", "User", "Host", "Date", "Time")
        self.tree_licenze.column("#0", width=0, stretch=NO)
        self.tree_licenze.column("Type", anchor=CENTER, width=int(self.w_container * 2 / 10), stretch=NO)
        self.tree_licenze.column("User", anchor=CENTER, width=int(self.w_container * 2 / 10), stretch=NO)
        self.tree_licenze.column("Host", anchor=CENTER, width=int(self.w_container * 2 / 10), stretch=NO)
        self.tree_licenze.column("Date", anchor=CENTER, width=int(self.w_container * 2 / 10), stretch=NO)
        self.tree_licenze.column("Time", anchor=CENTER, width=int(self.w_container * 2 / 10), stretch=NO)

        self.tree_licenze.heading("#0", text="", anchor=CENTER)
        self.tree_licenze.heading("Type", text="Type", anchor=CENTER)
        self.tree_licenze.heading("User", text="User", anchor=CENTER)
        self.tree_licenze.heading("Host", text="Host", anchor=CENTER)
        self.tree_licenze.heading("Date", text="Date", anchor=CENTER)
        self.tree_licenze.heading("Time", text="Time", anchor=CENTER)

        self.tree_licenze.tag_configure("oddrow", background="white")
        self.tree_licenze.tag_configure("evenrow", background="SlateGray2")

        # Scrollbar verticale
        self.tree_licenze_lavorazione_scrolly = Scrollbar(self.container, orient="vertical",
                                                         command=self.tree_licenze.yview)
        self.tree_licenze.configure(yscrollcommand=self.tree_licenze_lavorazione_scrolly.set)
        self.tree_licenze_lavorazione_scrolly.place(relx=1, rely=0.08, anchor="ne", height=self.h_container - 50)
        self.tree_licenze.place(width=self.w_container - 10, height=self.h_container - 20, relx=0, rely=0)

    def delete_entries(self):
        self.tree_licenze.delete(*self.tree_licenze.get_children())

    @staticmethod
    def global_is_active(HOST, PORT) -> bool:
        try:
            with socket.create_connection((HOST, PORT), timeout=3):
                return True
        except (socket.timeout, socket.error) as e:
            print(e)
            return False

    def refresh_tree(self):
        self.delete_entries()
        config = self.load_configs()

        HOST = config['HOST']
        PORT = config['PORT']
        
        MAC = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0, 8 * 6, 8)][::-1]).upper()

        if not self.global_is_active(HOST, PORT):
            messagebox.showerror("Errore", "Attivare GlobalProtect")
            return

        tree_data = None
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(f"?macaddress={MAC}\n".encode())
                data = s.recv(4096)

            tree_data = data.decode()
        except socket.timeout:
            tree_data = "Attiva global protect per favore :)"
        except Exception as e:
            tree_data = "Errore con il server licenze :("
            messagebox.showerror("Errore", str(e))

        if "MAC non autorizzato" in tree_data:
            row = ["MAC", "address", "non", "autorizzato", ":("]
            self.tree_licenze.insert(
                parent="", index="end", iid=0,
                text="",
                values=[row[0], row[1], row[2], row[3], row[4]],
                tags=("oddrow",) if 0 % 2 == 0 else ("evenrow",)
            )
        elif len(tree_data) == 0:
            row = ["Non", "c'è", "nessuno", "online", ":)"]
            self.tree_licenze.insert(
                parent="", index="end", iid=0,
                text="",
                values=[row[0], row[1], row[2], row[3], row[4]],
                tags=("oddrow",) if 0 % 2 == 0 else ("evenrow",)
            )
        else:

            tree_data = tree_data.replace("start ", "")
            tree_data = list(map(str.strip, tree_data.split("\n")))

            filter_choice = self.filter_var.get()
            index = 0
            for element in tree_data:
                row = element.split(" ")
                if len(row) == 6:
                    if filter_choice == "ADAMS" and "ADAMS" not in row[0]:
                        continue
                    if filter_choice == "ANSYS" and "ANSYS" not in row[0]:
                        continue

                    self.tree_licenze.insert(
                        parent="", index="end", iid=index,
                        text="",
                        values=[row[0], row[1], row[2], row[4], row[5]],
                        tags=("oddrow",) if index % 2 == 0 else ("evenrow",)
                    )
                    index += 1

    def load_configs(self) -> dict:
        config = {}
        path = resource_path("port.txt")
        with open(path, 'r') as f:
            config["PORT"] = int(f.readline().strip())

        path = resource_path("host.txt")
        with open(path, "rb") as f:
            config["HOST"] = self.apply_xor(f.read(), str(config["PORT"])).decode().strip()
        return config

    
    @staticmethod
    def apply_xor(data: bytes, key: str) -> bytearray:
        key_bytes = key.encode() if isinstance(key, str) else key
        key_length = len(key_bytes)
        try:
            encrypted_data = bytearray(data)

            for i in range(len(data)):
                encrypted_data[i] ^= key_bytes[i % key_length]

            return encrypted_data
        except TypeError:
            return bytearray(bytes(" ", encoding='utf-8'))


def main():
    app = ConnectedUsers()
    app.mainloop()


if __name__ == "__main__":
    main()
