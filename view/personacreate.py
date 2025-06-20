import tkinter as tk
from tkcalendar import DateEntry
from tkinter.messagebox import showinfo, showwarning, showerror
from typing import Callable
from model import Persona
class PersonaCreate:
    def __init__(self, parent: tk.Tk, action: Callable):
        self.__parent = parent
        self.__action = action
        # Ventana
        root = tk.Tk()
        self.__root = root
        root.geometry("800x600")
        root.title("Registrar persona")
        root.protocol("WM_DELETE_WINDOW", self.__on_close)
        # Input nombre
        lbl_nombre = tk.Label(root, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        txt_nombre = tk.Entry(root)
        self.__txt_n = txt_nombre
        txt_nombre.grid(row=0, column=1, padx=10, pady=10)
        # Input nacimiento
        lbl_nac = tk.Label(root, text="Fecha de nacimiento:")
        lbl_nac.grid(row=1, column=0, padx=10, pady=10)
        date_nac = DateEntry(root, width=12, background='#336633', foreground='#cccccc', borderwidth=2)
        date_nac.grid(row=1, column=1, padx=10, pady=10)
        self.__date_n = date_nac
        # Botón guardar
        submit_button = tk.Button(root, text="Guardar", command=self.__on_submit)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)
        # Mostrar ventana
        root.mainloop()
    def __on_close(self):
        self.__root.destroy()
        self.__parent.deiconify()
    def __on_submit(self):
        if(self.__validate()):
            if self.__action(Persona(nombre=self.__txt_n.get(), nacimiento=self.__date_n.get_date())):
                showinfo("Éxito", "Registro de persona creado.")
                self.__on_close()
            else:
                showerror("Error", "No se pudo registrar la persona.")
    def __validate(self) -> bool:
        valido = True
        if len(self.__txt_n.get()) == 0:
            showwarning("Aviso", "El campo nombre es obligatorio")
            valido = False
        return valido