# 🚀 EduGraf Backend

Backend da API para o sistema EduGraf - Sistema de Automação de Planilhas Educacionais.

## 📋 Funcionalidades

- **Upload de Planilhas**: Recebe arquivos `.xlsx` com dados educacionais
- **Processamento de Dados**: Consolida informações por escola e polo
- **Geração de Tabelas**: Cria tabelas consolidadas com estatísticas
- **Geração de Gráficos**: Produz gráficos comparativos automáticos
- **API RESTful**: Endpoints organizados e bem documentados

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **Pandas**: Processamento e análise de dados
- **OpenPyXL**: Manipulação de arquivos Excel
- **Matplotlib/Seaborn**: Geração de gráficos
- **Uvicorn**: Servidor ASGI

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # API principal
│   └── utils.py         # Funções de processamento
├── uploads/             # Arquivos enviados
├── temp/                # Arquivos temporários
├── requirements.txt     # Dependências
├── run.py              # Script de inicialização
├── env.example         # Variáveis de ambiente
└── README.md           # Este arquivo
```

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente

```bash
cp env.example .env
# Editar .env conforme necessário
```

### 3. Executar o Servidor

```bash
# Opção 1: Usando o script
python run.py

# Opção 2: Direto com uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Endpoints da API

### GET `/`
- **Descrição**: Endpoint de teste
- **Resposta**: Status da API

### POST `/upload`
- **Descrição**: Upload de planilhas Excel
- **Parâmetros**:
  - `file`: Arquivo `.xlsx`
  - `polo`: Nome do polo (para tabelas)
  - `quant_trimestre`: Quantidade de trimestres (para gráficos)
- **Resposta**: Arquivo processado para download

### GET `/health`
- **Descrição**: Verificação de saúde da API
- **Resposta**: Status e timestamp

## 📋 Formato das Planilhas

As planilhas devem conter as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| Nome da escola | Texto | Nome da instituição |
| Modalidade | Texto | Modalidade de ensino |
| Niveis de Leitura | Texto | Baixo/Médio/Alto |
| Niveis de Escrita | Texto | Baixo/Médio/Alto |

## 🔧 Configurações

### Variáveis de Ambiente

- `API_HOST`: Host do servidor (padrão: 0.0.0.0)
- `API_PORT`: Porta do servidor (padrão: 8000)
- `DEBUG`: Modo debug (padrão: True)
- `UPLOAD_DIR`: Pasta de uploads
- `TEMP_DIR`: Pasta de arquivos temporários
- `MAX_FILE_SIZE`: Tamanho máximo de arquivo (bytes)

### CORS

Configurado para permitir acesso do frontend Vite:
- `http://localhost:5173`
- `http://127.0.0.1:5173`

## 📚 Documentação

A documentação automática está disponível em:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testes

Para testar a API:

```bash
# Teste de saúde
curl http://localhost:8000/health

# Teste de upload (exemplo)
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@planilha.xlsx" \
  -F "polo=Polo 1"
```

## 🔒 Segurança

- Validação de tipos de arquivo (apenas `.xlsx`)
- Limite de tamanho de arquivo configurável
- Validação de estrutura das planilhas
- Tratamento de erros robusto

## 📝 Logs

Os logs são exibidos no console e incluem:
- Requisições recebidas
- Erros de processamento
- Tempo de resposta
- Validações de arquivo

## 🤝 Integração com Frontend

O backend está configurado para integrar perfeitamente com o frontend React + Vite, fornecendo:

- Endpoints compatíveis com as requisições do frontend
- CORS configurado para desenvolvimento local
- Respostas em formato adequado para download de arquivos
- Tratamento de erros compatível com o frontend 