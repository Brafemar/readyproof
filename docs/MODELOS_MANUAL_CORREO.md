# Manual y modelos previos al correo

## Alcance de esta entrega

Primero se incorpora Manual y el vínculo nullable de Planilla; después se crean Envio, Intento y Retencion. No se implementó transporte SMTP, archivo .eml, envío por API ni programación automática de reintentos. app/correo.py sigue vacío. La etapa 5 completa continúa pendiente; esta entrega cubre sus modelos y relaciones.

El acceso al iPhone permanece suspendido. No hay datos reales, nuevos usuarios predeterminados ni cambios de fuente/, generadores, formato PDF o Git.

## Manual y SAA-1

Manual tiene id UUID, codigo de hasta 60 caracteres, titulo de hasta 255, sistema_tipo de hasta 12, contenido Text, campos_obligatorios JSON como lista y version de hasta 30. Se conservan las dos restricciones solicitadas: codigo único y combinación (codigo, version) única. La primera impide repetir el código incluso con otra versión; debe revisarse esa decisión antes de registrar múltiples versiones reales.

Planilla agrega manual_id UUID nullable y la relación planilla.manual. La migración vincula las SAA-1 existentes y el catálogo también vincula la SAA-1 de una instalación nueva. El manual ficticio tiene código SG-PEM-IFI-SAA-EJEMPLO, título [Ejemplo] Sistema de Abastecimiento de Agua y versión v1. No contiene el procedimiento normativo: solo un marcador de contenido de prueba.

campos_obligatorios=[] expresa que la política está pendiente de confirmación técnica; no establece que todos los campos sean opcionales ni modifica la validación de cargas. manual_id deberá pasar a obligatorio antes del uso real, con los vínculos y contenidos aprobados. La leyenda M1 está incorporada; persisten los demás controles antes de uso real.

## Modelos de correo

- Envio: id UUID, carga_id, destinatario de hasta 255, enviado_en nullable, estado ENUM PostgreSQL pendiente/enviado/fallo/descartado y creado_en. Estado inicial pendiente y enviado_en vacío; no se marca enviado ningún correo durante las pruebas.
- Intento: id UUID, envio_id, numero positivo y único dentro del envío, intentado_en, resultado de hasta 60 (ok/timeout/rechazado/bounce) y respuesta Text opcional.
- Retencion: id UUID, envio_id, reintentado_en nullable, proximos_intentos entre 0 y 2 y razon de hasta 255 (fallo_temporal/correo_invalido/bloqueado).

Relaciones: carga.envios, envio.carga, envio.intentos, envio.retenciones e intento/retencion.envio. Las tres FKs nuevas usan ON DELETE CASCADE. Las pruebas de borrado se ejecutan únicamente sobre datos ficticios en bases temporales; no se agregó ninguna ruta de borrado a la aplicación ni se borraron registros del ejemplo local.

El modelo Retencion solicitado representa la programación de reintentos. No sustituye la conservación mínima de tres años desde la emisión. Esa conservación, la copia del correo/PDF y el mecanismo de reintento del transporte deberán completarse con el servicio de correo; no se implementa una purga automática. Las restricciones históricas de las cargas y su auditoría se conservan.

## Migraciones Alembic

Dependencias fijadas: Alembic 1.14.1 y Mako 1.3.10. Se incorporaron para cumplir la migración Alembic solicitada. No se guardan URLs ni credenciales en alembic.ini.

La cadena es 003_base_etapa4 → 004_manual → 005_correo_modelos. El esquema previo se conserva en migraciones/base_etapa4.py; permite iniciar una base vacía o reconocer una instalación existente y conservar los marcadores históricos de versiones 1 a 3. Las nuevas revisiones registran las versiones 4 y 5 y alembic_version. No se reemplaza ni borra una base existente.

El comando habitual init-db aplica toda la cadena y es idempotente:

```powershell
.venv\Scripts\python.exe -m flask --app app init-db --ejemplos
```

Requiere DATABASE_URL local configurada por una persona, como antes. Para el ejemplo aislado, scripts/iniciar_ejemplo.py ejecuta el mismo proceso sin utilizar la base habitual. Sobre una base local configurada también se puede ejecutar:

```powershell
.venv\Scripts\python.exe -m alembic upgrade head
```

Alembic toma DATABASE_URL del entorno o del .env local no versionado. Las migraciones de vínculo necesitan conexión PostgreSQL, por lo que no se ofrece --sql offline. Los downgrades destructivos están bloqueados expresamente; esta entrega es aditiva.

## Verificaciones

Pruebas en tests/test_modelos_manual_correo.py: relación SAA-1→Manual, nullable actual de manual_id, unicidad solicitada, actualización desde etapa 4 conservando datos, idempotencia, creación y relaciones UUID, cascadas de las tres FKs, restricciones de estados/números y comparación de esquema Alembic con ORM. SMTP y SMTP_SSL están bloqueados en la prueba de creación de correo.

```powershell
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app
```

Las bases de las pruebas siguen siendo temporales, separadas de la habitual y con datos [Ejemplo]. Los destinatarios son del dominio reservado example.invalid. No se usa cPanel, DNS, servicios externos ni correo real. El recorrido de navegador continúa ejecutándose desde pytest con las dependencias locales existentes; playwright.config.js permanece pendiente.
