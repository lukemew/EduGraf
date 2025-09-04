#!/usr/bin/env python3
"""
Script para testar se todos os imports estão funcionando
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa todos os imports necessários"""
    try:
        print("🔄 Testando imports...")
        
        # Testar imports básicos
        print("✅ Importando FastAPI...")
        from fastapi import FastAPI
        
        print("✅ Importando SQLAlchemy...")
        from sqlalchemy.ext.asyncio import create_async_engine
        
        print("✅ Importando pandas...")
        import pandas as pd
        
        print("✅ Importando matplotlib...")
        import matplotlib.pyplot as plt
        
        print("✅ Importando openpyxl...")
        import openpyxl
        
        print("✅ Importando reportlab...")
        from reportlab.pdfgen import canvas
        
        # Testar imports do app
        print("✅ Importando database...")
        from app.database import engine, Base, init_db
        
        print("✅ Importando models...")
        from app.models import User
        
        print("✅ Importando auth...")
        from app.auth import router
        
        print("✅ Importando operations...")
        from app.operations import Operations
        
        print("✅ Importando utils...")
        from app.utils import process_excel_file_real
        
        print("✅ Importando main...")
        from app.main import app
        
        print("\n🎉 Todos os imports funcionaram perfeitamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro no import: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
