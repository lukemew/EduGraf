@echo off
echo 🔄 Reconstruindo EduGraf com correções...

REM Parar e remover tudo
echo 🛑 Parando e removendo containers...
docker compose down -v

echo 🧹 Removendo imagens antigas...
docker compose down --rmi all

echo 🗑️ Limpando volumes não utilizados...
docker volume prune -f

echo 🔨 Reconstruindo tudo do zero...
docker compose up --build -d

echo ⏳ Aguardando serviços iniciarem...
timeout /t 15 /nobreak > nul

echo 📊 Status dos containers:
docker compose ps

echo.
echo ✅ Rebuild concluído!
echo.
echo 🌐 Acesse:
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📊 Para ver logs:
echo    docker compose logs -f

pause
