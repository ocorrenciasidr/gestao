#!/usr/bin/env bash

# O Gunicorn é um servidor de produção que rodará o seu aplicativo Flask.
# O Render irá executar este arquivo.
# 'app:app' significa: encontre o objeto 'app' dentro do arquivo 'app.py'
gunicorn --bind 0.0.0.0:$PORT app:app
