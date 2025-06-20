from db import DBConnector
from model import Persona
from view import PersonalDisplay
class PersonalController:
    def __init__(self):
        self.__dbc = DBConnector() 
    def run(self):
        funciones = {
            PersonalDisplay.ALTA: self.alta,
            PersonalDisplay.BAJA: self.baja,
            PersonalDisplay.MODIFICACION: self.modificacion,
            PersonalDisplay.CONSULTA: self.consulta
        }
        PersonalDisplay(funciones)
    def alta(self, p: Persona) -> bool:
        try:
            self.__dbc.insert(p)
            b = True
        except Exception:
            b = False
        return b
    def baja(self, p: Persona) -> bool:
        try:
            self.__dbc.delete(p, p.id)
            b = True
        except Exception:
            b = False
        return b
    def consulta(self) -> list[Persona]:
        try:
            p = self.__dbc.select(Persona())
        except Exception:
            p = []
        return p
    def modificacion(self, p: Persona) -> bool:
        try:
            self.__dbc.update(p)
            b = True
        except Exception: #as e:
            b = False #print(e)
        return b