from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class LibroBase(BaseModel):
    """
    Esquema base para un libro. Incluye los campos comunes para creación y actualización.
    """
    nombre: constr(min_length=1)  # Nombre del libro
    descripcion: constr(min_length=1)  # Descripción del libro

class LibroCreate(LibroBase):
    """
    Esquema para la creación de un libro.
    """
    pass

class LibroUpdate(LibroBase):
    """
    Esquema para la actualización de un libro.
    """
    pass

class LibroResponse(LibroBase):
    """
    Esquema de respuesta para un libro, incluye el ID.
    """
    id: int
    class Config:
        orm_mode = True

class UsuarioBase(BaseModel):
    """
    Esquema base para un usuario. Incluye los campos comunes para creación y respuesta.
    """
    nombre: constr(min_length=1)  # Nombre del usuario
    correo: EmailStr  # Correo electrónico

class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un usuario (registro).
    """
    contrasena: constr(min_length=6)  # Contraseña

class UsuarioLogin(BaseModel):
    """
    Esquema para login de usuario. Solo requiere correo y contraseña.
    """
    correo: EmailStr
    contrasena: constr(min_length=6)

class UsuarioResponse(UsuarioBase):
    """
    Esquema de respuesta para un usuario, incluye el ID y la lista de libros.
    """
    id: int
    libros: Optional[List[LibroResponse]] = []
    class Config:
        orm_mode = True
