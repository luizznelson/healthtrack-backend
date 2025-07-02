@echo off
echo ================================================
echo  Iniciando setup do HealthTrack Backend
echo ================================================

echo.
echo Iniciando migracoes
alembic revision --autogenerate -m "initial migration"

echo.
echo  Executando migracoes Alembic...
alembic upgrade head

echo.
echo  Populando questionario de Avaliação de Risco de Diabetes...
python -m seeds.diabetes_questionario

echo.
echo  Populando questionario de Avaliação de Risco de Hiperensao...
python -m seeds.hipertensao_questionario

echo "Setup completo. Iniciando backend..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

echo.
echo ================================================
echo  Setup concluido!
echo  Acesse: http://localhost:8000/docs
echo ================================================
pause
