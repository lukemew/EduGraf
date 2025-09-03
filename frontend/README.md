# 🎨 EduGraf Frontend - Interface React

<div align="center">

![React](https://img.shields.io/badge/React-18+-61dafb.svg)
![Vite](https://img.shields.io/badge/Vite-5.0+-646cff.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-f7df1e.svg)

**Interface moderna e responsiva para o sistema EduGraf**

</div>

---

## 📋 Sobre o Frontend

O frontend do EduGraf é uma aplicação React moderna construída com Vite, oferecendo uma interface intuitiva e responsiva para upload de planilhas, geração de tabelas consolidadas e criação de relatórios gráficos em PDF.

### 🎯 Características Principais
- ⚡ **Performance**: Build otimizada com Vite
- 📱 **Responsivo**: Interface adaptável para todos os dispositivos
- 🎨 **Design Moderno**: UI/UX profissional e acessível
- 🔄 **Tempo Real**: Feedback instantâneo para o usuário

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **React** | 18+ | Biblioteca para interfaces de usuário |
| **Vite** | 5.0+ | Build tool moderna e rápida |
| **Axios** | 1.6+ | Cliente HTTP para comunicação com API |
| **React Router** | 6+ | Roteamento de páginas |
| **CSS3** | - | Estilização responsiva e moderna |

---

## 📁 Estrutura do Projeto

```
frontend/
├── 📁 public/                   # Arquivos estáticos
│   └── 📄 vite.svg             # Logo do Vite
│
├── 📁 src/                      # Código fonte
│   ├── 📁 assets/              # Recursos estáticos
│   │   ├── 📄 logo.png         # Logo do EduGraf
│   │   ├── 📄 grafico-exemplo.png
│   │   ├── 📄 tabela-exemplo.png
│   │   └── 📄 ilustracao*.png  # Ilustrações
│   │
│   ├── 📁 components/          # Componentes reutilizáveis
│   │   ├── 📁 Banner/          # Banner principal
│   │   ├── 📁 Button/          # Botões personalizados
│   │   ├── 📁 FileUpload/      # Upload de arquivos
│   │   ├── 📁 Navbar/          # Barra de navegação
│   │   ├── 📁 Select/          # Componente de seleção
│   │   ├── 📁 SmallButton/     # Botões pequenos
│   │   └── 📁 Tips/            # Dicas e informações
│   │
│   ├── 📁 pages/               # Páginas da aplicação
│   │   ├── 📁 HomePage/        # Página inicial
│   │   ├── 📁 TabelasPage/     # Geração de tabelas
│   │   └── 📁 GraficoPage/     # Geração de gráficos
│   │
│   ├── 📄 App.jsx              # Componente principal
│   ├── 📄 App.css              # Estilos globais
│   ├── 📄 index.css            # Estilos base
│   └── 📄 main.jsx             # Ponto de entrada
│
├── 📄 package.json             # Dependências e scripts
├── 📄 vite.config.js           # Configuração do Vite
├── 📄 eslint.config.js         # Configuração do ESLint
└── 📄 index.html               # Template HTML
```

---

## 🚀 Instalação e Configuração

### **Pré-requisitos**
- 📦 Node.js 16 ou superior
- 📦 npm ou yarn
- 🌐 Navegador moderno (Chrome, Firefox, Safari, Edge)

### **1. Instalar Dependências**
```bash
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install
# ou
yarn install
```

### **2. Configurar Variáveis de Ambiente**
Crie um arquivo `.env` na pasta `frontend/`:

```env
# URL da API Backend
VITE_API_URL=http://localhost:8000

# Modo de desenvolvimento
VITE_DEV_MODE=true
```

### **3. Executar em Desenvolvimento**
```bash
# Executar servidor de desenvolvimento
npm run dev
# ou
yarn dev

# A aplicação estará disponível em:
# http://localhost:5173
```

### **4. Build para Produção**
```bash
# Gerar build de produção
npm run build
# ou
yarn build

# Preview do build
npm run preview
# ou
yarn preview
```

---

## 🎨 Sistema de Design

### **Paleta de Cores**
```css
:root {
  --cor-primaria: #3d626d;           /* Azul escuro principal */
  --cor-secundaria: #165b70;         /* Azul médio */
  --cor-destaque: #1abc9c;           /* Verde água */
  --texto-claro: #ffffff;            /* Branco */
  --texto-escuro: #333333;           /* Cinza escuro */
  --cor-primaria-de-fundo: rgba(22, 91, 112, 0.09); /* Fundo suave */
}
```

### **Tipografia**
- **Fonte Principal**: Inter, -apple-system, BlinkMacSystemFont
- **Tamanhos**: 12px, 14px, 16px, 18px, 24px, 32px
- **Pesos**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold)

### **Componentes Principais**

#### **Button**
```jsx
<Button
  onClick={handleClick}
  filled={true}
  description="Texto do botão"
  link="/rota"
/>
```

#### **FileUpload**
```jsx
<FileUpload
  onFileSelect={setSelectedFile}
  accept=".xlsx"
  multiple={false}
/>
```

#### **Select**
```jsx
<Select
  type="polo"
  value={selectedValue}
  onChange={handleChange}
/>
```

---

## 📱 Páginas da Aplicação

### **1. HomePage** (`/`)
- 🏠 Página inicial com navegação
- 🎯 Botões para acessar funcionalidades
- 📊 Preview dos resultados

### **2. TabelasPage** (`/TabelasPage`)
- 📋 Seleção de polo educacional
- 📤 Upload de planilhas Excel
- 📊 Geração de tabelas consolidadas
- 💾 Download automático do arquivo

### **3. GraficoPage** (`/GraficoPage`)
- 📅 Seleção de trimestre (1-4)
- 📤 Upload de planilhas Excel
- 📈 Geração de gráficos e relatórios
- 📄 Download de PDF com análises

---

## 🔧 Configuração Avançada

### **Personalização de Temas**
Edite `src/index.css` para personalizar cores:

```css
/* Tema Escuro */
[data-theme="dark"] {
  --cor-primaria: #2c3e50;
  --cor-secundaria: #34495e;
  --cor-destaque: #3498db;
  --texto-claro: #ecf0f1;
  --texto-escuro: #bdc3c7;
}
```

### **Configuração do Vite**
Edite `vite.config.js` para configurações personalizadas:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

---

## 🧪 Testes

### **Executar Testes**
```bash
# Testes unitários
npm run test

# Testes com coverage
npm run test:coverage

# Testes em modo watch
npm run test:watch
```

### **Estrutura de Testes**
```
src/
├── 📁 __tests__/              # Testes unitários
│   ├── 📁 components/         # Testes de componentes
│   └── 📁 pages/             # Testes de páginas
└── 📁 __mocks__/             # Mocks para testes
```

---

## 📦 Scripts Disponíveis

| Script | Comando | Descrição |
|--------|---------|-----------|
| **dev** | `npm run dev` | Servidor de desenvolvimento |
| **build** | `npm run build` | Build de produção |
| **preview** | `npm run preview` | Preview do build |
| **lint** | `npm run lint` | Verificar código com ESLint |
| **lint:fix** | `npm run lint:fix` | Corrigir problemas do ESLint |

---

## 🐛 Debugging

### **Ferramentas de Desenvolvimento**
- 🔧 **React DevTools**: Extensão do navegador
- 🌐 **Vite DevTools**: Console integrado
- 📊 **Network Tab**: Monitorar requisições HTTP

### **Logs de Debug**
```javascript
// Ativar logs detalhados
console.log('🔍 DEBUG:', data);

// Logs de erro
console.error('❌ ERRO:', error);

// Logs de sucesso
console.log('✅ SUCESSO:', result);
```

---

## 🚀 Deploy

### **Deploy Estático**
```bash
# Build de produção
npm run build

# Os arquivos estarão em dist/
# Faça upload para seu servidor web
```

### **Deploy com Vercel**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### **Deploy com Netlify**
```bash
# Build
npm run build

# Upload da pasta dist/ para Netlify
```

---

## 🤝 Contribuição

### **Padrões de Código**
- 📝 Use ESLint para manter consistência
- 🎨 Siga o sistema de design estabelecido
- 📱 Teste em diferentes dispositivos
- ♿ Mantenha acessibilidade

### **Estrutura de Commits**
```
feat: adicionar nova funcionalidade
fix: corrigir bug
style: alterações de estilo
refactor: refatoração de código
docs: atualizar documentação
test: adicionar testes
```

---

## 📞 Suporte

Para dúvidas sobre o frontend:

- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/EduGraf/issues)
- 💬 **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/EduGraf/discussions)
- 📧 **Email**: frontend@edugraf.com

---

<div align="center">

**Desenvolvido com React + Vite**

*Interface moderna para o sistema EduGraf*

</div>