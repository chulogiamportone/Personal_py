from dataclasses import dataclass
import datetime
@dataclass
class Persona:
    id: int = -1
    nombre: str = ""
    nacimiento: datetime.date = datetime.date.today()