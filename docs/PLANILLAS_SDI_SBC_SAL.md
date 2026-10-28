# Planillas habilitadas en readyproof

El catálogo operativo tiene **cuatro familias y 16 planillas individuales**. Los JSON de grupo y las versiones anteriores se conservan para mantener referencias, cargas y PDFs históricos. El total de filas de la tabla `planillas` incluye esos registros; no se borran para forzar un contador de cuatro.



## Cuatro sistemas y 16 planillas disponibles

Elegí primero el **Sistema** y después la **Planilla** correspondiente. El formulario cambia con esa elección y el borrador anterior se conserva en el dispositivo.

| Sistema | Planilla | Uso |
|---|---|---|
| SAA | SAA-1 | Información general · una A4 horizontal |
| SAL | SAL-1 | Información general |
| SAL | SAL-2 | Inspección mensual |
| SAL | SAL-3 | Inspección y pruebas semestral y anual |
| SAL | SAL-4 | Inspección y prueba quinquenal |
| SBC | SBC-1 | Información general |
| SBC | SBC-2 | Inspección semanal / autocontrol |
| SBC | SBC-3 | Inspección mensual |
| SBC | SBC-4 | Mantenimiento mensual - trimestral |
| SBC | SBC-5 | Mantenimiento semestral - anual |
| SBC | SBC-6 | Pruebas |
| SDI | SDI-1 | Información general |
| SDI | SDI-2 | Prueba mensual |
| SDI | SDI-3 | Prueba trimestral, semestral y anual |
| SDI | SDI-4 | Mantenimiento anual |
| SDI | SDI-5 | Información semanal (autocontrol) |

SAL corresponde al **Sistema de Extinción por Agentes Limpios**.

- Información general: completar los campos y opciones originales del sistema.
- Controles periódicos: completar las columnas ENE a DIC o S1 a S5 según la planilla. Deslizá la tabla horizontalmente en el celular.
- Listas de verificación: indicar la fecha del bloque, el valor cuando corresponda y el resultado: ✓ cumple, O no cumple, X no apreciable o NA no aplicable. Las condiciones O o X se describen en Observaciones, como indica el pie del kit.
- Firmar en los dos recuadros, revisar **Vista previa** y finalizar. **Descargar PDF** y **Enviar PDF por correo** usan la planilla elegida.

SAA-1 conserva una sola A4 horizontal. SDI, SBC y SAL conservan la paginación del kit en A4 horizontal para mantener sus filas y columnas. Solo se admiten datos y firmas ficticios en este piloto.


## Instalación y verificación

Con la configuración privada de PostgreSQL cargada:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\flask.exe --app app init-db --ejemplos
```

La revisión `009_multisistema` registra SDI-1 a 5, SBC-1 a 6 y SAL-1 a 4 desde los JSON verificados, asociados a sus manuales SG-PEM-IFI. Agrega los sistemas que falten únicamente a los clientes ficticios existentes. La inicialización normal prepara los cuatro sistemas del cliente de prueba. La operación es idempotente y no reemplaza plantillas ya registradas. Un downgrade se bloquea si existen cargas vinculadas o plantillas alteradas.

`GET /api/planillas` ofrece únicamente las 16 plantillas vigentes. `GET /api/clientes/{id}/sistemas` muestra los sistemas asignados al cliente. Las versiones y los contenedores JSON históricos continúan en la base; no forman parte del selector operativo.

Para verificar las familias vigentes en SQL:

```sql
SELECT sistema_tipo, COUNT(*)
FROM planillas
WHERE (codigo = 'SG-PEM-IFI-SAA-1' AND version = '00-26-rp2')
   OR (version = '00-26-ms1' AND sistema_tipo IN ('SDI', 'SBC', 'SAL'))
GROUP BY sistema_tipo
ORDER BY sistema_tipo;
```

Resultado: SAA=1, SDI=5, SBC=6, SAL=4. Los formularios se derivan de las definiciones del kit; el Excel se genera con `build_planilla.py` y se convierte a PDF por LibreOffice. Se conservan los encabezados, las filas, las opciones y el pie originales. No se agrega ninguna frecuencia ni valor normativo.


## Evidencia de la habilitación privada

El 27/10/2026 se aplicó la migración 009 con respaldo previo, conservando cargas, firmas, envíos, contraseñas y versiones anteriores. El servidor ofrece 16 planillas vigentes; las 25 filas totales incluyen el historial y los catálogos JSON. Se probaron las 16 emisiones y descargas mediante login normal de tecnico_readyproof, con datos y firmas ficticios. Se revisaron sus 29 páginas en A4 horizontal; las firmas permanecen dentro del casillero aun cuando continúe en otra página. La suite final aprobó 208 pruebas; compilación y sintaxis JavaScript sin errores.

La comprobación del correo de documentación se realizó sin transmisión nueva. Los pendientes de dominio, HTTPS, datos reales y respaldo externo siguen en el checklist general.
