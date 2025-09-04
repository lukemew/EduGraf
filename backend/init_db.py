#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
"""
import asyncio
import os
from app.database import engine, Base

async def init_db():
    """Cria todas as tabelas no banco de dados"""
    print("🔄 Inicializando banco de dados...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    asyncio.run(init_db())
