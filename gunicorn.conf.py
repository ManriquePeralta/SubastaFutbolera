# Configuración para el servidor gunicorn
bind = "0.0.0.0:10000"
workers = 2
# Tiempo máximo para respuestas largas
timeout = 120