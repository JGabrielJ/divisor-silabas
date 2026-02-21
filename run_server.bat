@echo off
setlocal
title Divisor de Silabas

echo Verificando o ambiente Python...

REM Verifica se o ambiente virtual .venv existe.
IF NOT EXIST .venv (
    echo Nenhum ambiente virtual encontrado. Criando venv...
    REM Tenta usar `py` que eh mais robusto no Windows; se falhar, usa `python`
    py -m venv .venv || python -m venv .venv
)

echo Ativando ambiente virtual e instalando dependencias...
REM Ativa o venv e instala os pacotes do requirements.txt
call .\.venv\Scripts\activate.bat
pip install -r requirements.txt

echo Inicializando o servidor...
REM Executa o script principal do servidor
python manage.py runserver

endlocal