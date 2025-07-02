#!/bin/bash
set -e  # Faz o script parar se der erro

echo "==============================================="
echo "  Iniciando setup do HealthTrack Backend"
echo "==============================================="

echo "🔁 Garantindo que pasta de versões existe..."
mkdir -p alembic/versions

echo "🔁 Criando migration (ignorado se já existir)..."
alembic revision --autogenerate -m "initial migration" || true

echo "📦 Aplicando migrations Alembic..."
alembic upgrade head

echo "🌱 Populando questionário de diabetes..."
python -m seeds.diabetes_questionario

echo "🌱 Populando questionário de hipertensão..."
python -m seeds.hipertensao_questionario

echo "✅ Setup completo. Iniciando servidor..."

# Esse comando substitui o processo atual (é o correto!)
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
