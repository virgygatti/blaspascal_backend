from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Usuario(Base):
    """
    Modelo de usuario para la base de datos.
    Representa a un usuario del sistema, que puede tener varios libros asociados.
    """
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)  # Identificador único
    nombre = Column(String, nullable=False)  # Nombre del usuario
    correo = Column(String, unique=True, index=True, nullable=False)  # Correo electrónico (único)
    contrasena = Column(String, nullable=False)  # Contraseña (almacenada como hash)
    libros = relationship('Libro', back_populates='propietario', cascade='all, delete-orphan')  # Relación uno a muchos con Libro

class Libro(Base):
    """
    Modelo de libro para la base de datos.
    Cada libro pertenece a un usuario (propietario).
    """
    __tablename__ = 'libros'
    id = Column(Integer, primary_key=True, index=True)  # Identificador único
    nombre = Column(String, nullable=False)  # Nombre del libro
    descripcion = Column(String, nullable=False)  # Descripción del libro
    propietario_id = Column(Integer, ForeignKey('usuarios.id'))  # ID del usuario propietario
    propietario = relationship('Usuario', back_populates='libros')  # Relación inversa con Usuario
