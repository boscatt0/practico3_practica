from sqlmodel import Session, select
from .database import create_db_and_tables, engine
from .models import Persona, Oficina


def create_oficinas_y_personas():
    with Session(engine) as session:
        oficina_administracion = Oficina(
        name="Administracion",
        direccion="Casa central"
        )
        oficina_sistemas = Oficina(
            name="Sistemas",
            direccion="Casa central"
        )

        persona_tatiana = Persona(
            name="Tatiana",
            puesto="Encargada de RRHH",
            age=28,
            oficina=oficina_administracion,
        )

        persona_eugenia = Persona(
            name="Eugenia",
            puesto="Administrativo",
            age=25,
            oficina=oficina_administracion,
        )

        persona_lucia = Persona(
            name="Lucia",
            puesto="desarrolladora",
            age=29,
            oficina=oficina_sistemas,
        )
        session.add(persona_tatiana)
        session.add(persona_eugenia)
        session.add(persona_lucia)
        session.commit()

        for persona in (persona_tatiana, persona_eugenia, persona_lucia):
            session.refresh(persona)

        print("Created persona:", persona)
        print("Oficina de la persona:", persona.oficina)

def listar_personas_de_oficina(nombre_oficina: str):
    """Lista de personas de una oficina navegando oficina.personas"""
    with Session(engine) as session:
        oficina = session.exec(
            select(Oficina).where(Oficina.name == nombre_oficina)

        ).first()

        if oficina is None:
            print(f"\nPersonas de la oficina '{nombre_oficina}'")
            return
        print(f"\nPersonas de la oficina '{oficina.name}:'")
        for persona in oficina.personas:
            print(f" - {persona.name} ({persona.puesto})")

def select_con_join():
    """"Consulta con join entre Persona Y Oficina"""
    with Session(engine) as session:
        resultados = session.exec(
            select(Persona, Oficina)
            .join(Oficina)
            .where(Oficina.name == "Sistemas")
        )
        print("\nJOIN Personas/oficina (solo Sistemas):")
        for persona, oficina in resultados:
            print(f" - {persona.name} trabaja en {oficina.name} ({oficina.direccion})")

def select_con_filtro(edad_minima: int = 28):
    """Filtro where sobre un campo numerico"""
    with Session(engine) as session:
        personas = session.exec(
            select(Persona).where(Persona.age >= edad_minima)
        ).all()

        print(f"\nPersonas de {edad_minima} años o mas")
        for persona in personas:
            print(f" - {persona.name}, {persona.age} años")

def reasignar_persona(nombre_persona: str, nombre_oficina_destino: str):
    """Reasignar una persona a otra oficina usando el atributo de relacion"""
    with Session(engine) as session:
        persona = session.exec(
        select(Persona).where(Persona.name == nombre_persona)
    ).first()
    oficina_destino = session.exec(
        select(Oficina).where(Oficina.name == nombre_oficina_destino)
    ).first()

    if persona is None or oficina_destino is None:
        print("No se encontro la persona o la oficina destino")
        return

    print(f"\n{persona.name} estaba  en : {persona.oficina.name}")
    persona.oficina = oficina_destino
    session.add(persona)
    session.commit()
    session.refresh(persona)
    print(f"{persona.name} ahora esta en: {persona.oficina.name}")

#Delete

def eliminar_persona(nombre_persona: str):
    with Session(engine) as session:
        persona= session.exec(
            select(Persona).where(Persona.name == nombre_persona)
        ).first()

    if persona is None:
        print(F"\nNo existe la persona '{nombre_persona}'")
        return

    session.delete(persona)
    session.commit()
    print(f"\nPersona eliminada: {nombre_persona}")

def eliminar_oficina_con_personas(nombre_oficina: str):
#demuestra que pasa al borrar una oficina que todavia tiene personas
#SQLALchemy desvincula a las hijas antes de borrar a la madre: les pone oficina:id = NULL (la columna es opcional)
# Las personas "huerfanas", no se borran en cascada

    with Session(engine) as session:
        oficina = session.exec(
            select(Oficina).where(oficina.name == nombre_oficina)
        ).first()

        if oficina is None:
            print(f"\nEiminando la oficina {oficina.name}, que tiene "
            f"{len(oficina.personas)} persona(s)...")
            session.delete(oficina)
            session.commit()

            personas = session.exec(select(Persona)).all()
            print("Estado de las personas despues del borrado: ")
            for persona in personas:
                print(f" - {persona.name}: oficina_id = {persona.oficina_id}")


def main():
    create_db_and_tables()
    create_oficinas_y_personas()
    listar_personas_de_oficina("Administracion")
    select_con_join()
    select_con_filtro(28)
    reasignar_persona("Eugenia", "Sistemas")
    eliminar_persona("Lucia")
    eliminar_oficina_con_personas("Sistemas")


if __name__ == "__main__":
    main()