import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import get_db, Base, engine, AsyncSessionLocal
from .models import User


router = APIRouter(prefix="/auth", tags=["auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), password_hash.encode('utf-8'))


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=JWT_EXPIRES_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user




@router.post("/register")
async def register(
    payload: dict = Body(...),
    db: AsyncSession = Depends(get_db)
):
    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    if not all([name, email, password]):
        raise HTTPException(status_code=422, detail="Campos obrigatórios: name, email, password")
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    user = User(name=name, email=email, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Validação básica de campos obrigatórios
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=422, detail="E-mail e senha são obrigatórios")

    # Buscar usuário pelo e-mail
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if user is None:
        # Usuário não encontrado
        raise HTTPException(status_code=400, detail="Conta não existe")

    if not verify_password(form_data.password, user.password_hash):
        # Senha incorreta
        raise HTTPException(status_code=400, detail="Senha incorreta")

    access_token = create_access_token(subject=user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "name": user.name, "email": user.email},
    }

async def create_default_admin():
    """Cria um usuário administrador padrão se ele não existir"""
    admin_email = os.getenv("ADMIN_EMAIL", "edugraf")
    admin_password = os.getenv("ADMIN_PASSWORD", "senha123") # Fallback de emergência

    async with AsyncSessionLocal() as db:
        # Verifica se o admin já existe
        result = await db.execute(select(User).where(User.email == admin_email))
        user = result.scalar_one_or_none()

        if user is None:
            print(f"⚙️ Criando usuário administrador padrão: {admin_email}")
            # Usa a sua função de hash já existente!
            hashed_pw = hash_password(admin_password)
            
            # Cria o usuário
            new_admin = User(
                name="Administrador do Sistema", 
                email=admin_email, 
                password_hash=hashed_pw
            )
            
            db.add(new_admin)
            await db.commit()
            print("✅ Administrador criado com sucesso!")
        else:
            print(f"👍 Administrador '{admin_email}' já existe no banco.")
