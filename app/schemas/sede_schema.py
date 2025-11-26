from pydantic import BaseModel, Field

class SedeBase(BaseModel):
    nombre: str
    direccion: str | None = None
    ciudad: str
    capacidad_total: int = Field(..., alias="capacidadTotal")
    descripcion: str | None = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }


class SedeCreate(SedeBase):
    pass


class SedeUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    ciudad: str | None = None
    capacidad_total: int | None = Field(None, alias="capacidadTotal")
    descripcion: str | None = None
    estado: str | None = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }


class SedeOut(BaseModel):
    sede_id: int = Field(..., alias="sedeId")
    nombre: str
    direccion: str | None
    ciudad: str
    capacidad_total: int = Field(..., alias="capacidadTotal")
    descripcion: str | None
    estado: str

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }
