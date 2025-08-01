from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
from datetime import datetime
from typing import List, Optional
import tempfile
import shutil
from .utils import process_excel_file, generate_charts, consolidate_data, create_pdf_report

app = FastAPI(
    title="EduGraf API",
    description="API para processamento de planilhas educacionais",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de pastas
UPLOAD_DIR = "uploads"
TEMP_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def root():
    """Endpoint de teste da API"""
    return {"message": "EduGraf API está funcionando!", "version": "1.0.0"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(None),
    files: List[UploadFile] = File(None),
    polo: Optional[str] = Form(None),
    quant_trimestre: Optional[int] = Form(None)
):
    """
    Endpoint para upload de planilhas Excel (.xlsx)
    
    - Para geração de tabelas: envia 'polo' e 'file'
    - Para geração de gráficos: envia 'quant_trimestre' e 'file'
    """
    try:
        # Determinar qual arquivo usar
        upload_file = None
        if file:
            upload_file = file
        elif files and len(files) > 0:
            upload_file = files[0]  # Usar o primeiro arquivo para gráficos
        else:
            raise HTTPException(status_code=422, detail="Nenhum arquivo foi enviado")
        
        # Validar tipo de arquivo
        if not upload_file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Apenas arquivos .xlsx são aceitos")
        
        # Salvar arquivo temporariamente
        file_path = os.path.join(UPLOAD_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{upload_file.filename}")
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        
        # Processar baseado no tipo de requisição
        if polo:
            # Geração de tabelas
            result_file = await process_table_generation(file_path, polo)
            return FileResponse(
                path=result_file,
                filename=f"tabela_{polo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif quant_trimestre:
            # Geração de gráficos
            result_file = await process_chart_generation(file_path, quant_trimestre)
            return FileResponse(
                path=result_file,
                filename=f"relatorio_graficos_{quant_trimestre}_trimestre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                media_type="application/pdf"
            )
        else:
            raise HTTPException(status_code=422, detail="Parâmetro 'polo' ou 'quant_trimestre' é obrigatório")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

async def process_table_generation(file_path: str, polo: str) -> str:
    """Processa geração de tabelas consolidadas"""
    try:
        # Ler e processar planilha
        df = pd.read_excel(file_path)
        
        # Validar colunas necessárias
        required_columns = ['Nome da escola', 'Modalidade', 'Niveis de Leitura', 'Niveis de Escrita']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")
        
        # Verificar se há dados
        if df.empty:
            raise ValueError("A planilha está vazia")
        
        # Processar dados
        processed_data = process_excel_file(df, polo)
        
        # Verificar se há dados processados
        if processed_data.empty:
            raise ValueError(f"Nenhum dado encontrado para o polo '{polo}'")
        
        # Salvar tabela processada
        output_file = os.path.join(TEMP_DIR, f"tabela_{polo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            processed_data.to_excel(writer, sheet_name='Dados Consolidados', index=False)
            
            # Adicionar aba com estatísticas gerais
            stats_data = {
                'Estatística': [
                    'Total de Escolas',
                    'Total de Alunos',
                    'Média de Alunos por Escola',
                    'Escola com Mais Alunos',
                    'Escola com Menos Alunos'
                ],
                'Valor': [
                    len(processed_data),
                    processed_data['Total Alunos'].sum(),
                    f"{processed_data['Total Alunos'].mean():.1f}",
                    processed_data.loc[processed_data['Total Alunos'].idxmax(), 'Escola'],
                    processed_data.loc[processed_data['Total Alunos'].idxmin(), 'Escola']
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='Estatísticas', index=False)
        
        return output_file
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento da tabela: {str(e)}")

async def process_chart_generation(file_path: str, quant_trimestre: int) -> str:
    """Processa geração de gráficos e PDF"""
    try:
        # Ler planilha
        df = pd.read_excel(file_path)
        
        # Validar colunas necessárias
        required_columns = ['Nome da escola', 'Modalidade', 'Niveis de Leitura', 'Niveis de Escrita']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")
        
        # Gerar gráficos
        charts_data = generate_charts(df, quant_trimestre)
        
        # Criar PDF com gráficos e análises
        pdf_path = create_pdf_report(charts_data, quant_trimestre)
        
        return pdf_path
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento dos gráficos: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)