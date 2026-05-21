"""Punto de entrada WSGI para Gunicorn y AWS Elastic Beanstalk."""

import newrelic.agent
# Inicializa el agente apuntando al archivo de configuración si es necesario, o usa variables de entorno
newrelic.agent.initialize()

# OBLIGAR A NEW RELIC A REGISTRAR LA APLICACIÓN DE INMEDIATO
try:
    newrelic.agent.register_application(timeout=10.0)
    print("New Relic: Aplicación registrada exitosamente con el colector.")
except Exception as e:
    print(f"New Relic Error: No se pudo registrar la app: {e}")

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
