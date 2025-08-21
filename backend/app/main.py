from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from datetime import datetime
from app.operations import operations as op

app = FastAPI(
    title="EduGraf API Simplificada",
    description="API simplificada para processamento de planilhas educacionais",
    version="2.0.0"
)

# CORS mais permissivo para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar diretórios necessários
os.makedirs("temp", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Página inicial do sistema"""
    try:
        return HTMLResponse(content=open("static/home.html", "r", encoding="utf-8").read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>EduGraf</title></head>
            <body>
                <h1>🎓 Sistema EduGraf</h1>
                <p>API para processamento de dados educacionais</p>
                <p>Acesse <a href="/docs">/docs</a> para ver a documentação da API</p>
            </body>
        </html>
        """, status_code=200)

@app.post("/upload")
async def upload_excel(
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None),
    polo: Optional[str] = Form(None),
    trimestre: Optional[int] = Form(None),
    tipo_processamento: Optional[str] = Form("tabela")  # "tabela" ou "grafico"
):
    """
    Upload e processamento de planilhas Excel
    
    Parâmetros:
    - files: Lista de arquivos Excel (.xlsx ou .xls) OU
    - file: Um único arquivo Excel
    - polo: Nome do polo para filtrar (para tabelas)
    - trimestre: Número do trimestre (para gráficos)
    - tipo_processamento: "tabela" ou "grafico"
    """
    
    # Determinar quais arquivos foram enviados
    upload_files = []
    
    if files:
        upload_files = files
    elif file:
        upload_files = [file]
    else:
        raise HTTPException(
            status_code=422, 
            detail="Nenhum arquivo foi enviado. Use 'files' para múltiplos arquivos ou 'file' para um arquivo único."
        )
    
    # Validação de arquivos
    for upload_file in upload_files:
        if not upload_file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(
                status_code=400, 
                detail=f"Apenas arquivos Excel são aceitos. Arquivo rejeitado: {upload_file.filename}"
            )
    
    try:
        # Determinar tipo de processamento
        if tipo_processamento == "grafico" or trimestre is not None:
            # Processamento para gráficos
            if trimestre is None:
                raise HTTPException(status_code=422, detail="Trimestre é obrigatório para gráficos")
            
            result_file = await op.gerar_graficos(upload_files, trimestre)
            
            return FileResponse(
                path=result_file,
                filename=f"relatorio_graficos_{trimestre}T_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                media_type="application/pdf"
            )
            
        else:
            # Processamento para tabelas (padrão)
            polo_name = polo or "Geral"
            
            result_file = await op.gerar_tabela_do_polo(upload_files, polo_name)
            
            return FileResponse(
                path=result_file,
                filename=f"tabela_{polo_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")

@app.post("/upload-simples")
async def upload_simples(
    files: Optional[List[UploadFile]] = File(None),
    file: Optional[UploadFile] = File(None)
):
    """
    Versão simplificada do upload - apenas para compatibilidade
    Processa arquivos e retorna dados JSON
    Aceita tanto 'files' quanto 'file'
    """
    
    # Determinar quais arquivos foram enviados
    upload_files = []
    
    if files:
        upload_files = files
    elif file:
        upload_files = [file]
    else:
        return {"error": "Nenhum arquivo foi enviado. Use 'files' para múltiplos arquivos ou 'file' para um arquivo único.", "status": "error"}
    
    # Validação de arquivos
    for upload_file in upload_files:
        if not upload_file.filename.endswith(('.xlsx', '.xls')):
            return {"error": f"Envie apenas arquivos Excel (.xlsx ou .xls). Arquivo: {upload_file.filename}", "status": "error"}
    
    try:
        # Usar a função original de processamento
        results = await op.processar_planilhas_simples(upload_files)
        return {"results": results, "status": "success"}
        
    except Exception as e:
        return {"error": f"Erro no processamento: {str(e)}", "status": "error"}

@app.post("/upload-original")
async def upload_excel_original(files: List[UploadFile] = File(...)):
    """
    Endpoint idêntico ao seu código original para máxima compatibilidade
    """
    for file in files:
        # Verifica se é Excel
        if not file.filename.endswith(('.xlsx', '.xls')):
            return {"error": f"Envie apenas arquivos excel (xlsx ou xls): {file.filename}"}
    
    try:
        results = await op.processar_planilhas_simples(files)
        return {"results": results}
        
    except Exception as e:
        return {"error": f"Erro no processamento: {str(e)}"}

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "message": "EduGraf API funcionando perfeitamente!"
    }

@app.get("/info")
async def info():
    """Informações sobre a API"""
    return {
        "name": "EduGraf API",
        "version": "2.0.0",
        "description": "Sistema para análise de dados educacionais",
        "endpoints": {
            "/": "Página inicial",
            "/upload": "Upload completo com opções de processamento",
            "/upload-simples": "Upload simplificado (compatibilidade)",
            "/health": "Status da API",
            "/docs": "Documentação automática"
        },
        "supported_files": [".xlsx", ".xls"],
        "features": [
            "Processamento de diagnósticos de leitura e escrita",
            "Geração de tabelas consolidadas",
            "Geração de gráficos e relatórios PDF",
            "Suporte a múltiplos formatos de planilha"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Para desenvolvimento
        log_level="info"
    )