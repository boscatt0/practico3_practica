from sqlmodel import Session

from .database import create_db_and_tables, engine
from .models import Personas, Oficina


def create_personas():
    with Session(engine) as session:
        oficina_administracion = Oficina(name="Administracion", direccion="Casa central")

        persona_tatiana = Persona(
            name="Tatiana", puesto="encargada de RRHH", oficina=oficina_administracion
        )
        session.add(persona_tatiana)
        session.commit()

        session.refresh(persona_tatianas)

        print("Created persona:", persona_tatiana)
        print("Oficina de la persona:", persona_tatiana.oficina)


def main():
    create_db_and_tables()
    create_personas()


if __name__ == "__main__":
    main()