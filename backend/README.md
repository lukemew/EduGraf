# 🐍 EduGraf Backend - API Python FastAPI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-red.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7+-orange.svg)

**API robusta para processamento de dados educacionais**

</div>

---

## 📋 Sobre o Backend

O backend do EduGraf é uma API RESTful construída com FastAPI, responsável por processar planilhas Excel, gerar tabelas consolidadas, criar gráficos e relatórios em PDF. A API oferece endpoints seguros e eficientes para o frontend React.

### 🎯 Características Principais
- ⚡ **Performance**: FastAPI com alta performance
- 🔒 **Segurança**: Validação de dados e tratamento de erros
- 📊 **Processamento**: Manipulação avançada de dados com Pandas
- 📈 **Visualização**: Geração de gráficos com Matplotlib/Seaborn
- 📄 **Relatórios**: Criação de PDFs profissionais

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.8+ | Linguagem principal |
| **FastAPI** | 0.115+ | Framework web moderno |
| **Uvicorn** | 0.34+ | Servidor ASGI |
| **Pandas** | 2.2+ | Manipulação de dados |
| **OpenPyXL** | 3.1+ | Manipulação de Excel |
| **Matplotlib** | 3.7+ | Geração de gráficos |
| **Seaborn** | 0.12+ | Visualização estatística |
| **ReportLab** | 4.0+ | Criação de PDFs |
| **Pydantic** | 2.11+ | Validação de dados |

---

## 📁 Estrutura do Projeto

```
backend/
├── 📁 app/                      # Código da aplicação
│   ├── 📄 main.py              # Aplicação FastAPI principal
│   └── 📄 utils.py             # Funções utilitárias
│
├── 📁 uploads/                  # Arquivos enviados (criado automaticamente)
├── 📁 temp/                     # Arquivos temporários (criado automaticamente)
│
├── 📄 requirements.txt         # Dependências Python
├── 📄 run.py                   # Script de inicialização
├── 📄 .gitignore              # Arquivos ignorados pelo Git
└── 📄 README.md               # Este arquivo
```

---

## 🚀 Instalação e Configuração

### **Pré-requisitos**
- 🐍 Python 3.8 ou superior
- 📦 pip (gerenciador de pacotes Python)
- 🌐 Git

### **1. Configurar Ambiente Virtual**
```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### **2. Instalar Dependências**
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### **3. Configurar Variáveis de Ambiente**
Crie um arquivo `.env` na pasta `backend/`:

```env
# Configurações do servidor
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True

# Configurações de arquivos
UPLOAD_DIR=uploads
TEMP_DIR=temp
MAX_FILE_SIZE=10485760  # 10MB

# Configurações de CORS
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### **4. Executar o Servidor**
```bash
# Método 1: Usando o script run.py
python run.py

# Método 2: Usando uvicorn diretamente
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Método 3: Usando python -m
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **5. Verificar Instalação**
```bash
# Testar endpoint de saúde
curl http://localhost:8000/health

# Acessar documentação interativa
# http://localhost:8000/docs
```

---

## 🔌 Endpoints da API

### **Endpoints Principais**

| Método | Endpoint | Descrição | Parâmetros |
|--------|----------|-----------|------------|
| `GET` | `/` | Status da API | - |
| `GET` | `/health` | Verificação de saúde | - |
| `POST` | `/upload` | Upload e processamento | `file`, `polo` ou `quant_trimestre` |

### **Exemplos de Uso**

#### **1. Upload para Geração de Tabelas**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "polo=Polo 1" \
  -F "file=@planilha.xlsx"
```

#### **2. Upload para Geração de Gráficos**
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "quant_trimestre=1" \
  -F "file=@planilha.xlsx"
```

#### **3. Verificar Status da API**
```bash
curl http://localhost:8000/health
```

---

## 📊 Processamento de Dados

### **Formatos Suportados**

#### **Formato Real da Prefeitura**
- ✅ Planilhas com estrutura específica da Secretaria
- ✅ Dados de leitura e escrita em seções separadas
- ✅ Processamento automático de percentuais

#### **Formato Antigo**
- ✅ Planilhas com colunas: Nome da escola, Modalidade, Níveis
- ✅ Consolidação por polo educacional
- ✅ Cálculo de estatísticas gerais

### **Funcionalidades de Processamento**

#### **Geração de Tabelas**
```python
# Exemplo de processamento
def process_table_generation(file_path: str, polo: str) -> str:
    """
    Processa planilha e gera tabela consolidada
    - Detecta formato automaticamente
    - Consolida dados por polo
    - Aplica formatação profissional
    - Retorna arquivo Excel estilizado
    """
```

#### **Geração de Gráficos**
```python
# Exemplo de geração de gráficos
def process_chart_generation(file_path: str, quant_trimestre: int) -> str:
    """
    Processa planilha e gera relatório em PDF
    - Cria gráficos de barras
    - Gera análises estatísticas
    - Aplica formatação profissional
    - Retorna PDF com gráficos embutidos
    """
```

---

## 🎨 Formatação de Arquivos

### **Excel (.xlsx)**
- 🎨 **Cores**: Cabeçalhos com cores do projeto
- 📊 **Filtros**: Filtros automáticos nas colunas
- 📏 **Larguras**: Colunas ajustadas automaticamente
- 🔢 **Formatação**: Números e percentuais formatados
- 📋 **Abas**: Múltiplas abas organizadas

### **PDF (.pdf)**
- 🎨 **Design**: Layout profissional com cores do projeto
- 📈 **Gráficos**: Imagens de alta qualidade
- 📝 **Análises**: Textos descritivos e recomendações
- 📊 **Estatísticas**: Tabelas com dados consolidados
- 🏷️ **Legendas**: Explicações detalhadas

---

## 🔧 Configuração Avançada

### **Configuração do FastAPI**
```python
# app/main.py
app = FastAPI(
    title="EduGraf API",
    description="API para processamento de planilhas educacionais",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

### **Configuração de CORS**
```python
# Permitir origens específicas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Configuração de Upload**
```python
# Limites de arquivo
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = [".xlsx"]

# Validação de arquivo
def validate_file(file: UploadFile) -> bool:
    return file.filename.endswith('.xlsx') and file.size <= MAX_FILE_SIZE
```

---

## 🧪 Testes

### **Executar Testes**
```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=app

# Executar testes específicos
pytest tests/test_main.py
```

### **Estrutura de Testes**
```
backend/
├── 📁 tests/                   # Testes automatizados
│   ├── 📄 test_main.py        # Testes da API
│   ├── 📄 test_utils.py       # Testes das funções utilitárias
│   └── 📄 conftest.py         # Configuração dos testes
│
└── 📁 test_files/             # Arquivos de teste
    ├── 📄 sample_data.xlsx    # Dados de exemplo
    └── 📄 expected_output.xlsx # Resultado esperado
```

---

## 📦 Scripts Disponíveis

### **Scripts de Desenvolvimento**
```bash
# Executar servidor com reload automático
python run.py

# Executar com logs detalhados
python -m uvicorn app.main:app --reload --log-level debug

# Executar em modo produção
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Scripts de Manutenção**
```bash
# Limpar arquivos temporários
python -c "import shutil; shutil.rmtree('temp', ignore_errors=True)"

# Verificar dependências
pip check

# Atualizar dependências
pip install -r requirements.txt --upgrade
```

---

## 🐛 Debugging

### **Logs de Debug**
```python
# Ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# Logs personalizados
print(f"🔍 DEBUG: Processando arquivo: {file_path}")
print(f"✅ SUCESSO: Arquivo processado com sucesso")
print(f"❌ ERRO: {str(e)}")
```

### **Ferramentas de Debug**
- 🔧 **FastAPI Docs**: http://localhost:8000/docs
- 📊 **ReDoc**: http://localhost:8000/redoc
- 🐛 **Python Debugger**: `import pdb; pdb.set_trace()`

---

## 🚀 Deploy

### **Deploy Local**
```bash
# Build de produção
pip install -r requirements.txt

# Executar servidor
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Deploy com Docker**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Deploy com Gunicorn**
```bash
# Instalar Gunicorn
pip install gunicorn

# Executar com Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔒 Segurança

### **Validações Implementadas**
- ✅ **Tipo de arquivo**: Apenas .xlsx
- ✅ **Tamanho**: Limite de 10MB
- ✅ **Parâmetros**: Validação com Pydantic
- ✅ **CORS**: Origens permitidas configuráveis

### **Tratamento de Erros**
```python
# Exemplo de tratamento de erro
try:
    result = process_file(file_path)
except FileNotFoundError:
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail="Erro interno do servidor")
```

---

## 📊 Monitoramento

### **Métricas Disponíveis**
- 📈 **Requests**: Contador de requisições
- ⏱️ **Tempo**: Tempo de processamento
- 💾 **Memória**: Uso de memória
- 📁 **Arquivos**: Arquivos processados

### **Health Check**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

---

## 🤝 Contribuição

### **Padrões de Código**
- 📝 Use type hints em todas as funções
- 🧪 Escreva testes para novas funcionalidades
- 📚 Documente funções complexas
- 🔒 Valide todas as entradas

### **Estrutura de Commits**
```
feat: adicionar nova funcionalidade
fix: corrigir bug
docs: atualizar documentação
test: adicionar testes
refactor: refatorar código
```

---

## 📞 Suporte

Para dúvidas sobre o backend:

- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/EduGraf/issues)
- 📚 **Documentação**: http://localhost:8000/docs
- 💬 **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/EduGraf/discussions)
- 📧 **Email**: backend@edugraf.com

---

<div align="center">

**Desenvolvido com Python + FastAPI**

*API robusta para o sistema EduGraf*

</div>
