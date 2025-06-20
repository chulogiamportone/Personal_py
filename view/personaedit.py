import tkinter as tk
from model import Persona
from typing import Callable
from tkcalendar import DateEntry
from tkinter.messagebox import showinfo, showwarning, showerror
class PersonaEdit:
    def __init__(self, parent: tk.Tk, action: Callable, p: Persona):
        self.__parent = parent
        self.__action = action
        self.__p = p
        # Ventana
        root = tk.Tk()
        self.__root = root
        root.geometry("800x600")
        root.title("Actualizar persona")
        root.protocol("WM_DELETE_WINDOW", self.__on_close)
        # Input nombre
        lbl_nombre = tk.Label(root, text="Nombre:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        txt_nombre = tk.Entry(root, textvariable= tk.Variable(root, p.nombre))
        self.__txt_n = txt_nombre
        txt_nombre.grid(row=0, column=1, padx=10, pady=10)
        # Input nacimiento
        lbl_nac = tk.Label(root, text="Fecha de nacimiento:")
        lbl_nac.grid(row=1, column=0, padx=10, pady=10)
        date_nac = DateEntry(root, width=12, background='#336633', foreground='#cccccc', borderwidth=2)
        date_nac.grid(row=1, column=1, padx=10, pady=10)
        date_nac.set_date(p.nacimiento)
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
        if self.__modified() and self.__validate():
            if self.__action(Persona(self.__p.id, self.__txt_n.get(), self.__date_n.get_date())):
                showinfo("Éxito", "Registro de persona actualizado.")
                self.__on_close()
            else:
                showerror("Error", "No se pudo actualizar el registro de la persona.")
    def __validate(self) -> bool:
        v = len(self.__txt_n.get()) != 0
        if not v:
            showwarning("Aviso", "El campo nombre es obligatorio")
        return v
    def __modified(self) -> bool:
        m = self.__txt_n.get() != self.__p.nombre or str(self.__date_n.get_date()) != str(self.__p.nacimiento.strftime("%Y-%m-%d"))
        if not m:
            showwarning("Aviso", "No hay cambio en el registro de la persona.")
        return m