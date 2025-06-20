import tkinter as tk
from tkinter.messagebox import askyesno, showinfo, showwarning, showerror
from model import Persona
from view import PersonaCreate, PersonaEdit
from typing import Callable
class PersonalDisplay:
    ALTA = "A"
    BAJA = "B"
    MODIFICACION = "M"
    CONSULTA = "C"
    def __init__(self, abmc: dict[str, Callable]):
        self.__abmc = abmc
        # Ventana
        root = tk.Tk()
        self.__root = root
        root.geometry("800x600")
        root.title("Personal")
        root.bind("<Map>", self.__recargarlista)
        # Listado de personas
        frm_people = tk.Frame(root)
        frm_people.pack(fill=tk.X, padx=20, pady=20)
        lst_people = tk.Listbox(frm_people, width=0)
        self.__lst = lst_people
        lst_people.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        vsc_people = tk.Scrollbar(frm_people, orient=tk.VERTICAL)
        vsc_people.pack(fill=tk.Y, side=tk.RIGHT)
        lst_people.config(yscrollcommand=vsc_people.set)
        vsc_people.config(command=lst_people.yview)
        self.__recargarlista()
        # Botones
        frm_buttons = tk.Frame(root)
        frm_buttons.pack(fill=tk.X, padx=20, pady=20)
        btn_new = tk.Button(frm_buttons, text="Registrar persona", command=self.__veralta)
        btn_new.grid(row=0, column=0, padx=20, pady=20)
        btn_edit = tk.Button(frm_buttons, text="Actualizar persona", command=self.__vermodificacion)
        btn_edit.grid(row=0, column=1, padx=20, pady=20)
        btn_del = tk.Button(frm_buttons, text="Borrar persona", command=self.__verbaja)
        btn_del.grid(row=0, column=2, padx=20, pady=20)
        # Mostrar ventana
        root.mainloop()
    # Auxiliares de lista
    def __personaseleccionada(self) -> Persona | None:
        index = -1        
        for i in self.__lst.curselection():
            index = i
        return self.__personal[index] if index > -1 else None
    def __recargarlista(self, _ = None):
        self.__personal = self.__abmc[PersonalDisplay.CONSULTA]()
        items = tk.Variable(value=[f"{p.nombre} nació en {p.nacimiento.strftime('%d/%m/%Y')}" for p in self.__personal])
        self.__lst.config(listvariable=items)
    # Navegaciones
    def __veralta(self):
        self.__root.withdraw() # destroy no permite reutilizar
        PersonaCreate(self.__root, self.__abmc[PersonalDisplay.ALTA])
    def __vermodificacion(self):
        p = self.__personaseleccionada()
        if p is None:
            showwarning("Aviso", "Debe seleccionar una persona del listado para actualizar su registro.")
        else:
            self.__root.withdraw()
            PersonaEdit(self.__root, self.__abmc[PersonalDisplay.MODIFICACION], p)
    def __verbaja(self):
        p = self.__personaseleccionada()
        if p is None:
            showwarning("Aviso", "Debe seleccionar una persona del listado para borrar su registro.")
        elif askyesno("¿Borrar registro?", f"¿Borrar el registro de {p.nombre}?"):
            if self.__abmc[PersonalDisplay.BAJA](p):
                self.__recargarlista()
                showinfo("Éxito", "Registro de persona borrado.")
            else:
                showerror("Error", "El registro de la persona no pudo ser borrado.")