from typing import Union, List

from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .database import engine
from . import models, schemas, database
from passlib.context import CryptContext
from jose import JWTError, jwt
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# =====================
# Utilidades de seguridad y autenticación
# =====================

# Configuración para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración para JWT
SECRET_KEY = "Sup3rS3cr3tK3y"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def get_password_hash(password):
    """Genera un hash seguro para la contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verifica que la contraseña en texto plano coincida con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    """Crea un token JWT con los datos proporcionados y tiempo de expiración."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(database.get_db)):
    """Obtiene el usuario autenticado a partir del token JWT enviado en el header Authorization."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.Usuario).filter(models.Usuario.correo == correo).first()
    if user is None:
        raise credentials_exception
    return user

# =====================
# Endpoints principales
# =====================

@app.get("/")
def read_root():
    """Endpoint de prueba para verificar que la API está corriendo."""
    return {"Hello": "World"}

@app.post("/register", response_model=schemas.UsuarioResponse)
def register(user: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    """Registra un nuevo usuario. El correo debe ser único. La contraseña se almacena de forma segura."""
    db_user = db.query(models.Usuario).filter(models.Usuario.correo == user.correo).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    hashed_password = get_password_hash(user.contrasena)
    new_user = models.Usuario(nombre=user.nombre, correo=user.correo, contrasena=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: schemas.UsuarioLogin, db: Session = Depends(database.get_db)):
    """Autentica al usuario y devuelve un token JWT si las credenciales son correctas."""
    user = db.query(models.Usuario).filter(models.Usuario.correo == form_data.correo).first()
    if not user or not verify_password(form_data.contrasena, user.contrasena):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.correo}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/libros", response_model=List[schemas.LibroResponse])
def listar_libros(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    """Lista los libros del usuario autenticado, con paginación."""
    libros = db.query(models.Libro).filter(models.Libro.propietario_id == current_user.id).offset(skip).limit(limit).all()
    return libros

@app.post("/libros", response_model=schemas.LibroResponse)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    """Crea un nuevo libro asociado al usuario autenticado."""
    nuevo_libro = models.Libro(**libro.dict(), propietario_id=current_user.id)
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

@app.put("/libros/{libro_id}", response_model=schemas.LibroResponse)
def actualizar_libro(libro_id: int, libro: schemas.LibroUpdate, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    """Actualiza los datos de un libro del usuario autenticado."""
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id, models.Libro.propietario_id == current_user.id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db_libro.nombre = libro.nombre
    db_libro.descripcion = libro.descripcion
    db.commit()
    db.refresh(db_libro)
    return db_libro

@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(database.get_db), current_user: models.Usuario = Depends(get_current_user)):
    """Elimina un libro del usuario autenticado."""
    db_libro = db.query(models.Libro).filter(models.Libro.id == libro_id, models.Libro.propietario_id == current_user.id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(db_libro)
    db.commit()
    return {"ok": True}
