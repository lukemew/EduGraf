# 🎓 EduGraf - Sistema de Automação de Planilhas Educacionais

<div align="center">

![EduGraf Logo](frontend/src/assets/logo.png)

**Sistema inteligente para processamento e análise de dados educacionais**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](LICENSE)

</div>

---

## 📋 Sobre o Projeto

O **EduGraf** é um sistema web desenvolvido para a **Secretaria de Educação do Município**, com o objetivo de automatizar o processamento de planilhas do **Diagnóstico de Leitura e Escrita (DLE)**. O sistema consolida dados de múltiplas escolas, gera relatórios visuais e facilita a tomada de decisões pedagógicas.

### 🎯 Objetivos
- ✅ Reduzir erros manuais no processamento de dados
- ✅ Agilizar a análise de resultados educacionais
- ✅ Facilitar a visualização de dados em reuniões pedagógicas
- ✅ Automatizar a geração de relatórios comparativos

---

## 🚀 Funcionalidades Principais

### 📊 **Geração de Tabelas Consolidadas**
- Upload de planilhas `.xlsx` das escolas
- Consolidação automática por polo educacional
- Estatísticas detalhadas de leitura e escrita
- Formatação profissional com cores e estilos

### 📈 **Geração de Gráficos e Relatórios**
- Gráficos de barras comparativos por trimestre
- Relatórios em PDF com análises detalhadas
- Visualizações interativas e profissionais
- Análise de tendências educacionais

### 🎨 **Interface Moderna e Intuitiva**
- Design responsivo e acessível
- Navegação simples e clara
- Feedback visual em tempo real
- Upload drag-and-drop de arquivos

---

## 🛠️ Stack Tecnológica

### **Frontend**
- ⚛️ **React 18** - Biblioteca para interfaces de usuário
- ⚡ **Vite** - Build tool moderna e rápida
- 🎨 **CSS3** - Estilização responsiva
- 📡 **Axios** - Cliente HTTP para API

### **Backend**
- 🐍 **Python 3.8+** - Linguagem principal
- 🚀 **FastAPI** - Framework web moderno
- 📊 **Pandas** - Manipulação de dados
- 📈 **Matplotlib/Seaborn** - Geração de gráficos
- 📄 **ReportLab** - Criação de PDFs
- 📋 **OpenPyXL** - Manipulação de Excel

### **Infraestrutura**
- 🐳 **Docker** - Containerização (opcional)
- 🔄 **Docker Compose** - Orquestração de serviços
- 🌐 **CORS** - Comunicação frontend-backend

---

## 📁 Estrutura do Projeto

```
EduGraf/
├── 📁 frontend/                 # Interface React
│   ├── 📁 src/
│   │   ├── 📁 components/       # Componentes reutilizáveis
│   │   ├── 📁 pages/           # Páginas da aplicação
│   │   ├── 📁 assets/          # Imagens e recursos
│   │   └── 📄 main.jsx         # Ponto de entrada
│   ├── 📄 package.json         # Dependências frontend
│   └── 📄 vite.config.js       # Configuração Vite
│
├── 📁 backend/                  # API Python
│   ├── 📁 app/
│   │   ├── 📄 main.py          # Aplicação FastAPI
│   │   └── 📄 utils.py         # Funções utilitárias
│   ├── 📄 requirements.txt     # Dependências Python
│   └── 📄 run.py              # Script de inicialização
│
├── 📄 docker-compose.yml       # Configuração Docker
└── 📄 README.md               # Este arquivo
```

---

## 🚀 Instalação e Configuração

### **Pré-requisitos**
- 🐍 Python 3.8 ou superior
- 📦 Node.js 16 ou superior
- 📦 npm ou yarn
- 🌐 Git

### **1. Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/EduGraf.git
cd EduGraf
```

### **2. Configuração do Backend**
```bash
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar o servidor
python run.py
```

### **3. Configuração do Frontend**
```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

### **4. Acessar a Aplicação**
- 🌐 **Frontend**: http://localhost:5173
- 🔧 **Backend API**: http://localhost:8000
- 📚 **Documentação API**: http://localhost:8000/docs

---

## 🐳 Execução com Docker (Opcional)

```bash
# Construir e executar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d

# Parar os serviços
docker-compose down
```

---

## 📖 Como Usar

### **1. Geração de Tabelas**
1. Acesse a página "Gerar Tabelas do Polo"
2. Selecione o polo desejado
3. Faça upload da planilha Excel
4. Clique em "Gerar Tabela"
5. Baixe o arquivo consolidado

### **2. Geração de Gráficos**
1. Acesse a página "Gerar Gráficos do Polo"
2. Selecione o trimestre (1-4)
3. Faça upload da planilha Excel
4. Clique em "Gerar Gráfico"
5. Baixe o relatório em PDF

---

## 🔧 Configuração Avançada

### **Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto:

```env
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
UPLOAD_DIR=uploads
TEMP_DIR=temp

# Frontend
VITE_API_URL=http://localhost:8000
```

### **Personalização de Cores**
Edite o arquivo `frontend/src/index.css` para personalizar as cores:

```css
:root {
  --cor-primaria: #3d626d;
  --cor-secundaria: #165b70;
  --cor-destaque: #1abc9c;
  --texto-claro: #ffffff;
  --texto-escuro: #333333;
  --cor-primaria-de-fundo: rgba(22, 91, 112, 0.09);
}
```

---

## 🧪 Testes

```bash
# Testes do backend
cd backend
python -m pytest

# Testes do frontend
cd frontend
npm test
```

---

## 📊 Formatos de Arquivo Suportados

### **Planilhas de Entrada**
- ✅ Excel (.xlsx)
- ✅ Formato padrão da Secretaria de Educação
- ✅ Dados de leitura e escrita por escola

### **Arquivos de Saída**
- 📊 **Tabelas**: Excel (.xlsx) com formatação profissional
- 📈 **Gráficos**: PDF (.pdf) com análises detalhadas

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 👥 Equipe de Desenvolvimento

| Nome | Função | Contato |
|------|--------|---------|
| **Lucas Rodrigues de Melo** | Desenvolvedor Full-Stack | [GitHub](https://github.com/lucas) |
| **Wesley de Sousa Moreira** | Desenvolvedor Backend | [GitHub](https://github.com/wesley) |
| **Kaique Brayan de Andrade Lima** | Desenvolvedor Frontend | [GitHub](https://github.com/kaique) |
| **Micaele Rodrigues de Morais** | Designer UI/UX | [GitHub](https://github.com/micaele) |

---

## 📄 Licença

Este projeto é de uso **educacional e institucional**. Todos os direitos reservados à Secretaria de Educação do Município.

---

## 📞 Suporte

Para dúvidas, sugestões ou problemas:

- 📧 **Email**: suporte@edugraf.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/EduGraf/issues)
- 📚 **Documentação**: [Wiki do Projeto](https://github.com/seu-usuario/EduGraf/wiki)

---

<div align="center">

**Desenvolvido com ❤️ para a Educação**

*EduGraf - Transformando dados em insights educacionais*

</div>