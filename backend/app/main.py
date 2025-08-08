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
from utils import (
    process_excel_file, 
    process_excel_file_real,
    generate_charts, 
    generate_charts_real,
    consolidate_data, 
    create_pdf_report,
    criar_dataframe
)

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
        
        # Debug: verificar parâmetros recebidos
        print(f"🔍 DEBUG: Parâmetros recebidos - polo: {polo}, quant_trimestre: {quant_trimestre}")
        print(f"🔍 DEBUG: Tipo de quant_trimestre: {type(quant_trimestre)}")
        print(f"🔍 DEBUG: Arquivo recebido: {upload_file.filename}")
        print(f"🔍 DEBUG: Polo presente: {polo is not None}")
        print(f"🔍 DEBUG: Quant_trimestre presente: {quant_trimestre is not None}")
        
        # Processar baseado no tipo de requisição
        if polo:
            print("🔍 DEBUG: ✅ ROTA DE TABELAS - Gerando arquivo .xlsx")
            print(f"🔍 DEBUG: Polo selecionado: {polo}")
            # Geração de tabelas
            result_file = await process_table_generation(file_path, polo)
            print(f"🔍 DEBUG: Arquivo de tabela gerado: {result_file}")
            return FileResponse(
                path=result_file,
                filename=f"tabela_{polo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif quant_trimestre is not None:
            print("🔍 DEBUG: ✅ ROTA DE GRÁFICOS - Gerando arquivo .pdf")
            print(f"🔍 DEBUG: Quantidade de trimestres: {quant_trimestre}")
            # Converter quant_trimestre para inteiro
            try:
                quant_trimestre_int = int(quant_trimestre)
                print(f"🔍 DEBUG: quant_trimestre convertido para int: {quant_trimestre_int}")
            except (ValueError, TypeError):
                print(f"🔍 DEBUG: Erro ao converter quant_trimestre: {quant_trimestre}")
                raise HTTPException(status_code=400, detail="quant_trimestre deve ser um número válido")
            
            # Geração de gráficos
            result_file = await process_chart_generation(file_path, quant_trimestre_int)
            print(f"🔍 DEBUG: Arquivo PDF gerado: {result_file}")
            return FileResponse(
                path=result_file,
                filename=f"relatorio_graficos_{quant_trimestre}_trimestre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                media_type="application/pdf"
            )
        else:
            print("🔍 DEBUG: ❌ Nenhum parâmetro válido encontrado")
            print("🔍 DEBUG: Para tabelas, envie 'polo'")
            print("🔍 DEBUG: Para gráficos, envie 'quant_trimestre'")
            raise HTTPException(status_code=422, detail="Parâmetro 'polo' ou 'quant_trimestre' é obrigatório")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

async def process_table_generation(file_path: str, polo: str) -> str:
    """Processa geração de tabelas consolidadas"""
    try:
        # Ler e processar planilha
        df = pd.read_excel(file_path, header=None)
        
        # Verificar se é formato real da prefeitura ou formato antigo
        is_real_format = check_if_real_format(df)
        
        if is_real_format:
            # Processar formato real da prefeitura
            processed_data = process_excel_file_real(df, polo)
            
            # Salvar tabela processada
            output_file = os.path.join(TEMP_DIR, f"tabela_{polo.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Aba de Leitura
                processed_data['leitura'].to_excel(writer, sheet_name='Dados Leitura', index=False)
                
                # Aba de Escrita
                processed_data['escrita'].to_excel(writer, sheet_name='Dados Escrita', index=False)
                
                # Adicionar aba com estatísticas gerais
                stats_data = {
                    'Estatística': [
                        'Total de Anos/Séries',
                        'Total de Alunos (Leitura)',
                        'Total de Alunos (Escrita)',
                        'Percentual de Não Leitores',
                        'Percentual de Leitores com Fluência',
                        'Percentual de Pré-Silábicos',
                        'Percentual de Ortográficos'
                    ],
                    'Valor': [
                        len(processed_data['leitura']),
                        processed_data['leitura']['total alunos'].sum(),
                        processed_data['escrita']['total alunos'].sum(),
                        f"{processed_data['leitura']['nl_%'].mean():.1f}%",
                        f"{processed_data['leitura']['lcf_%'].mean():.1f}%",
                        f"{processed_data['escrita']['p_%'].mean():.1f}%",
                        f"{processed_data['escrita']['o_%'].mean():.1f}%"
                    ]
                }
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='Estatísticas', index=False)
        else:
            # Processar formato antigo
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
        print(f"🔍 DEBUG: Iniciando processamento de gráficos para trimestre {quant_trimestre}")
        print(f"🔍 DEBUG: Arquivo de entrada: {file_path}")
        
        # Ler planilha
        df = pd.read_excel(file_path, header=None)
        print(f"🔍 DEBUG: Planilha lida com {len(df)} linhas e {len(df.columns)} colunas")
        
        # Verificar se é formato real da prefeitura ou formato antigo
        is_real_format = check_if_real_format(df)
        print(f"🔍 DEBUG: Formato detectado: {'Real' if is_real_format else 'Antigo'}")
        
        if is_real_format:
            # Processar formato real da prefeitura
            print("🔍 DEBUG: Processando formato real da prefeitura...")
            processed_data = process_excel_file_real(df, "Geral")
            print("🔍 DEBUG: Dados processados com sucesso")
            
            # Gerar gráficos
            print("🔍 DEBUG: Gerando gráficos...")
            charts_data = generate_charts_real(processed_data, quant_trimestre)
            print("🔍 DEBUG: Gráficos gerados com sucesso")
            print(f"🔍 DEBUG: Charts data keys: {list(charts_data.keys())}")
        else:
            # Processar formato antigo
            print("🔍 DEBUG: Processando formato antigo...")
            # Validar colunas necessárias
            required_columns = ['Nome da escola', 'Modalidade', 'Niveis de Leitura', 'Niveis de Escrita']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")
            
            # Gerar gráficos
            print("🔍 DEBUG: Gerando gráficos para formato antigo...")
            charts_data = generate_charts(df, quant_trimestre)
            print("🔍 DEBUG: Gráficos gerados com sucesso")
            print(f"🔍 DEBUG: Charts data keys: {list(charts_data.keys())}")
        
        # Criar PDF com gráficos e análises
        print("🔍 DEBUG: Criando PDF...")
        pdf_path = create_pdf_report(charts_data, quant_trimestre)
        print(f"🔍 DEBUG: PDF criado com sucesso: {pdf_path}")
        
        # Verificar se o PDF foi realmente criado
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"🔍 DEBUG: PDF existe no sistema de arquivos, tamanho: {file_size} bytes")
            
            # Verificar se é realmente um PDF
            with open(pdf_path, 'rb') as f:
                header = f.read(4).decode('latin-1')
                print(f"🔍 DEBUG: Header do PDF: {header}")
                if header == '%PDF':
                    print("🔍 DEBUG: ✅ Arquivo é um PDF válido")
                else:
                    print("🔍 DEBUG: ❌ Arquivo não é um PDF válido")
        else:
            print(f"🔍 DEBUG: ❌ PDF não foi criado: {pdf_path}")
        
        return pdf_path
        
    except Exception as e:
        print(f"🔍 DEBUG: Erro no processamento de gráficos: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro no processamento dos gráficos: {str(e)}")

def check_if_real_format(df: pd.DataFrame) -> bool:
    """
    Verifica se a planilha está no formato real da prefeitura
    
    Args:
        df: DataFrame para verificar
    
    Returns:
        True se for formato real, False caso contrário
    """
    try:
        print(f"🔍 DEBUG: Verificando formato da planilha...")
        print(f"🔍 DEBUG: DataFrame shape: {df.shape}")
        
        # Procurar por indicadores do formato real
        for idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                if isinstance(value, str):
                    value_str = str(value).upper()
                    if "DIAGNÓSTICO DE LEITURA" in value_str:
                        print(f"🔍 DEBUG: Formato real detectado: DIAGNÓSTICO DE LEITURA encontrado na linha {idx}, coluna {col_idx}")
                        return True
                    if "DIAGNÓSTICO DE ESCRITA" in value_str:
                        print(f"🔍 DEBUG: Formato real detectado: DIAGNÓSTICO DE ESCRITA encontrado na linha {idx}, coluna {col_idx}")
                        return True
                    if "LEITURA" in value_str and "ESCRITA" in value_str:
                        print(f"🔍 DEBUG: Formato real detectado: LEITURA/ESCRITA encontrado na linha {idx}, coluna {col_idx}")
                        return True
        
        # Verificar se tem as colunas esperadas do formato antigo
        if len(df.columns) > 0:
            first_row = df.iloc[0] if len(df) > 0 else []
            print(f"🔍 DEBUG: Primeira linha: {first_row.tolist()}")
            if any('Nome da escola' in str(cell) for cell in first_row):
                print("🔍 DEBUG: Formato antigo detectado: 'Nome da escola' encontrado")
                return False
        
        print("🔍 DEBUG: Formato não reconhecido, assumindo formato real")
        return True  # Assumir formato real por padrão
        
    except Exception as e:
        print(f"🔍 DEBUG: Erro na detecção de formato: {e}")
        return True  # Em caso de erro, assumir formato real

@app.get("/health")
async def health_check():
    """Endpoint para verificar saúde da API"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)