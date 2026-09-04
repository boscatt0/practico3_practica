from sqlmodel import Field, Relationship, SQLModel


class Oficina(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    direccion: str

    personas: list["Persona"] = Relationship(back_populates="oficina")


class Persona(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    puesto: str
    age: int | None = Field(default=None, index=True)

    oficina_id: int | None = Field(default=None, foreign_key="oficina.id")
    oficina: | None = Relationship(back_populates="personas")