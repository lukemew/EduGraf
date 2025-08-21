# --- Estágio de Build ---
# Usa uma imagem do Node para construir a aplicação React
FROM node:18-alpine as builder

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos package.json e package-lock.json
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Copia o restante dos arquivos da aplicação
COPY . .

# Executa o build da aplicação para produção
RUN npm run build

# --- Estágio de Produção ---
# Usa uma imagem leve do Nginx para servir os arquivos estáticos
FROM nginx:1.25-alpine

# Copia os arquivos gerados no build do estágio anterior para a pasta do Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]