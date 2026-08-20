# Divisor de Sílabas 2.0

![GitHub License](https://img.shields.io/github/license/JGabrielJ/DivisorSilabas?style=flat&labelColor=darkblue&color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/JGabrielJ/DivisorSilabas?display_timestamp=committer&style=flat)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/JGabrielJ/DivisorSilabas?style=flat)
![GitHub deployments](https://img.shields.io/github/deployments/JGabrielJ/DivisorSilabas/master%20-%20divisorsilabas?style=flat)
![GitHub forks](https://img.shields.io/github/forks/JGabrielJ/DivisorSilabas?style=flat)
![GitHub Repo stars](https://img.shields.io/github/stars/JGabrielJ/DivisorSilabas?style=flat)
![GitHub contributors](https://img.shields.io/github/contributors/JGabrielJ/DivisorSilabas?style=flat)
![GitHub top language](https://img.shields.io/github/languages/top/JGabrielJ/DivisorSilabas?style=flat&labelColor=yellow&color=blue)

## Sobre o Projeto

Uma aplicação web desenvolvida com Django que recebe uma palavra qualquer da Língua Portuguesa e retorna sua divisão silábica usando padrões locais do [**Pyphen**](https://pyphen.org/), juntamente com algumas informações adicionais sobre a palavra. Lembre-se de que
esta é uma versão gratuita de demonstração, portanto nem todas as palavras serão separadas corretamente.

_Para habilitar o botão de apoio, defina a variável de ambiente `PAYPAL_DONATION_URL` com o seu link oficial de doação do PayPal antes de iniciar o servidor._

## Utilizando o Website

Existem duas maneiras de acessar o Divisor de Sílabas, descritas logo abaixo:

- **Com o Render (remoto):** O site pode ser acessado em [**divisorsilabas.onrender.com ↗**](https://divisorsilabas.onrender.com)
- **Com o Python (local):** Primeiro, baixe a pasta compactada do projeto clicando em `<> Code → Download ZIP`, depois extraia os arquivos, abra um terminal na pasta do projeto e siga o passo a passo do seu sistema operacional:

#### No Windows:

1. Instale o Python 3.12 ou mais recente através do site [**python.org**](https://www.python.org/downloads/), marcando a opção **Add Python to PATH** durante a instalação;
2. Crie e ative o ambiente virtual:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   No Prompt de Comando, use `.venv\Scripts\activate.bat` para ativá-lo;

3. Instale as dependências e inicialize o banco local:

   ```powershell
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

4. Inicie o servidor:

   ```powershell
   python manage.py runserver
   ```

#### No Linux:

1. Instale o Python, o pip e o módulo de ambientes virtuais:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências e inicialize o banco local:

   ```bash
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

4. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

#### No macOS:

1. Instale o Python 3.12 ou mais recente através do [**python.org**](https://www.python.org/downloads/macos/) ou do [**Homebrew**](https://brew.sh/):

   ```bash
   brew install python
   ```

2. Crie e ative o ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale as dependências e inicialize o banco local:

   ```bash
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

4. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

- Agora, é só acessar o endereço `127.0.0.1:8000` no seu navegador e o Divisor de Sílabas estará disponível para uso.

> Nota do Dev: a versão original do projeto, desenvolvida com PySimpleGUI (agora descontinuado e obsoleto), pode ser encontrada em [**ProjetosAcademicos**](<https://github.com/JGabrielJ/ProjetosAcademicos/tree/main/DivisorSilabas%20(old)>).
