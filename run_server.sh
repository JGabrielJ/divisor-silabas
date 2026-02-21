#!/bin/bash

# Encerra o script se qualquer comando falhar
set -e

echo "Verificando o ambiente Python..."

# Verifica se há um ambiente virtual .venv e cria um caso não exista
if [ ! -d ".venv" ]; then
    echo "Nenhum ambiente virtual encontrado. Criando venv..."
    python3 -m venv .venv
fi

echo "Ativando ambiente virtual e instalando dependencias..."
source .venv/bin/activate
pip install -r requirements.txt

echo "Inicializando o servidor..."
python3 manage.py runserver