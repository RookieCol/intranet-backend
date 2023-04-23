# Intranet  SOUTA

Este proyecto es una API de ejemplo desarrollada en Python y FastAPI que utiliza una base de datos SQLite.

## Instalación

1. Clona este repositorio en tu máquina local:

`git clone https://github.com/RookieCol/intranet-backend.git`


2. Instala las dependencias del proyecto:

        cd intranet-backend
        pip install -r requirements.txt

3. Crear la base de datos
	Una vez en la raiz del proyecto se debe crear la base de datos de desarollo siguiendo los siguentes comandos:

        	python3 
        	import services 
        	services.create_database ()

4. Inicia la aplicación:
`uvicorn main:app --reload`