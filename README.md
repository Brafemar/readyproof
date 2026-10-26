# readyproof

Aplicación para cargar y emitir planillas SG-PEM-IFI de BRAFEMAR. El técnico carga la planilla en el navegador, la firma en pantalla, y el sistema emite el PDF con el formato de la serie y lo envía por correo al cliente.

## Documentos del proyecto

- `AGENTS.md`: encargo técnico y reglas de trabajo.
- `PASOS_SERVICIO_FINAL_readyproof.md`: accesos y puesta en marcha.
- `fuente/`: copia de las herramientas y datos del kit interno SG-PEM-IFI v5. Solo lectura.
- `REGISTRO_DE_CAMBIOS.md`: historial de cada etapa.
- `PREGUNTAS_ABIERTAS.md`: decisiones pendientes.
- `docs/INSTALACION.md`: instalación (se completa en la etapa 9).

## Requisitos

- Python 3.11 o superior.
- LibreOffice (para generar PDF), a partir de la etapa 1.
- PostgreSQL, a partir de la etapa 2.

## Desarrollo local (etapa 0)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -q
```

En Linux o macOS, activar con `source .venv/bin/activate`.

## Configuración

Copiar `.env.ejemplo` a `.env` y completar los valores. El archivo `.env` nunca se versiona.

## Piloto SAA-1 (etapa 1)

El adaptador local genera SAA-1 con los datos del kit y convierte el Excel interno a PDF con LibreOffice. Se conservan los logos del encabezado y se rechazan destinos existentes. Ejecución con datos ficticios:

```powershell
.venv\Scripts\python.exe -m app.planillas.piloto --salida out/nueva_revision_saa1
```

El procedimiento, el contrato de datos y la validación se describen en `docs/PILOTO_SAA1.md`. La aceptación de esta etapa requiere revisar el PDF y aprobar el formato antes de continuar a la etapa 2.


## Modelo de datos y API local (etapa 2)

La API de SAA-1 permite crear y guardar borradores, finalizar, emitir PDF con datos ficticios y descargarlo. PostgreSQL es local; las pruebas crean y cierran un clúster temporal separado. Se requiere instalar `requirements-dev.txt`, además de disponer de PostgreSQL y LibreOffice, para ejecutar la suite completa.

El contrato de los endpoints, la configuración local y las reglas de validación están en `docs/API_ETAPA2.md`. La emisión a clientes reales permanece bloqueada por la confirmación pendiente de la leyenda. No se incluyen interfaz, usuarios ni correo.
