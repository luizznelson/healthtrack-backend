@echo off
echo ================================================
echo  Iniciando setup do HealthTrack Backend
echo ================================================

echo.
echo  Subindo containers Docker...
docker-compose up -d --build

echo.
echo  Aguardando 3 segundos para inicializacao do banco...
timeout /t 3

echo.
echo Iniciando migracoes
docker-compose exec backend alembic revision --autogenerate -m "initial migration"

echo.
echo  Executando migracoes Alembic...
docker-compose exec backend alembic upgrade head

echo.
echo  Populando questionario de Avaliação de Risco de Diabetes...
docker-compose exec backend python -m seeds.diabetes_questionario

echo.
echo  Populando questionario de Avaliação de Risco de Hiperensao...
docker-compose exec backend python -m seeds.hipertensao_questionario

echo.
echo ================================================
echo  Setup concluido!
echo  Acesse: http://localhost:8000/docs
echo ================================================
pause
