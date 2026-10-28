ENCARGO PARA CODEX — ETAPAS 1 A 6

ANTECEDENTE: Etapa 0 (diagnóstico, sin modificaciones) confirmó:
- 79 planillas verificadas byte-a-byte vs v5 zips oficiales: 0 diferencias
- 16 habilitadas en producción (SAA-1, SAL-1–4, SBC-1–6, SDI-1–5): 389 ítems/campos intactos
- SDI-2 detectores de humo: no hay bug (emitidas bloquean por diseño, borradores OK)
- Schema: aplicación en 010_firmantes, último backup en 009_multisistema (stale)
- Modo piloto: 232 tests OK

ETAPA 1: BACKUP AUTOMÁTICO A GOOGLE DRIVE + RESTORE TEST
Encargo: Automatizar respaldo de readyproof a Google Drive con cifrado, retención y alertas.

PRECONDICIÓN: Jorge ha autorizado Google Drive para readyproof.ar@gmail.com mediante rclone OAuth.

TAREAS:
1. Verificar rclone config readyproof-drive existe y es válida
2. Crear script /var/backups/readyproof/backup_y_subida.sh:
   - pg_dump -U readyproof -h localhost readyproof → archivo .dump
   - Cifrar con openssl AES-256-CBC usando variable READYPROOF_BACKUP_KEY (no en repo)
   - Subir a Google Drive readyproof-drive:/readyproof-backups/ con rclone
   - Logging a /var/backups/readyproof/backup.log
   - Alertas por Gmail a readyproof.ar@gmail.com si falla
3. Programar en systemd timer: /etc/systemd/system/readyproof-backup.timer
   - OnCalendar=*-*-* 02:00:00 (UTC nightly)
   - RandomizedDelaySec=900 (jitter 15 min)
4. Test manual: ejecutar script, verificar en Drive
5. Test de restauración EN BD OFFLINE (NO en producción):
   - Descargar backup .enc desde Drive
   - Descifrar con openssl
   - Restaurar en readyproof_test_restore
   - Validar: psql "SELECT version FROM alembic_version" → 010_firmantes
   - Validar counts: planillas=25, carga≥1, firma_carga≥1
6. Crear docs/BACKUP_Y_RESTAURACION.md con procedimiento de restauración manual

CRITERIOS ACEPTACIÓN ETAPA 1:
✓ rclone OAuth sin contraseña en repo
✓ Script backup ejecutable, test exitoso
✓ Timer systemd activo
✓ Restauración test OK: schema 010, datos íntegros
✓ Documentación incluida

---

ETAPA 2: MIGRACIÓN CUIT Y SISTEMAS
Encargo: Agregar CUIT normalizado a cliente, validación, reporte faltantes.

TAREAS:
1. Alembic migration 011_cliente_cuit_opcional.py:
   - ADD COLUMN cliente.cuit VARCHAR(11) UNIQUE, nullable=True
   - CREATE INDEX ix_cliente_cuit
2. Módulo app/utils/cuit_validator.py:
   - validar_cuit(cuit_str): valida 11 dígitos + dígito verificador (IRAM)
   - normalizar_cuit(cuit_str): retorna CUIT sin guiones
3. Script scripts/audit_cuit.py:
   - Reporte clientes SIN CUIT
   - Reporte CUIT DUPLICADOS (si los hay)
   - Salida: JSON
4. Alembic migration 012_sistema_cliente_activo.py:
   - ADD COLUMN sistema.activo BOOLEAN DEFAULT True
   - Asegurar cliente_id NOT NULL en Sistema
5. En app/models/__init__.py:
   - Cliente.cuit: String(11), unique, nullable
   - Sistema.cliente_id: UUID FK NOT NULL
   - Sistema.activo: Boolean DEFAULT True

CRITERIOS ACEPTACIÓN ETAPA 2:
✓ Migraciones 011–012 aplicadas (sin datos reales)
✓ Validador CUIT testeado (82000000000 válido, etc.)
✓ audit_cuit.py ejecutado, reporte generado
✓ Clientes y sistemas consistentes

---

ETAPA 3: IMPORTADOR + VALIDACIÓN REGLAS
Encargo: Importador determinista desde 79 Excel oficiales. Validar O + observación, mediciones.

TAREAS:
1. Script scripts/importador_planillas.py:
   - Lee 79 Excel desde fuente/planillas/
   - Para cada uno:
     * Extrae contenido (bloques, ítems, opciones, unidades)
     * Calcula hash SHA256
     * Compara contra catalogo_referencia_planillas.json
     * Si no existe en BD: crea Planilla versionada
     * Si existe: reporta "YA_EXISTE"
     * Si difiere: reporta "CONTENIDO_DIFERENTE" (diferencia de líneas)
   - Output JSON: cambios realizados
   - No sobrescribe 16 existentes
2. Módulo app/carga/validacion.py:
   - validar_item_verificacion(item_resultado, item_def):
     * O (NO CUMPLE) REQUIERE observación
     * Campos con unidad: medición OBLIGATORIA salvo NA
     * X y NA: sin observación requerida (opcional)
   - Lanzar ValidationError si faltan
3. Tests unitarios:
   - Cargar cada una de las 16 en un borrador
   - Validar reglas O + mediciones
   - Emitir y validar PDF

CRITERIOS ACEPTACIÓN ETAPA 3:
✓ Importador: 79 vs catálogo 0 diferencias
✓ Validación O + observación: implementada y testeada
✓ Validación mediciones: implementada y testeada
✓ Reporte de cambios: JSON válido

---

ETAPA 4: DESBLOQUEO, DATOS DINÁMICOS, VALIDACIÓN SDI
Encargo: Desbloqueo con motivo + revisión pública. Validar SDI grillas.

TAREAS:
1. Alembic migration 013_desbloqueo_revision.py:
   - CREATE TABLE numero_registro_contador (id INT PK, ultimo INT DEFAULT 0)
   - ADD COLUMN carga.numero_registro INT UNIQUE, nullable
   - ADD COLUMN carga.revision_publica INT DEFAULT 0
   - ADD COLUMN carga.pdf_hash VARCHAR(64)
   - ADD COLUMN carga.desbloqueado_por UUID FK usuario
   - ADD COLUMN carga.motivo_desbloqueo TEXT
   - ADD COLUMN carga.estado_anulada BOOLEAN DEFAULT False
2. Función en app/carga/servicios.py:
   - desbloquear_carga(carga_id, usuario_id, motivo):
     * Solo si creador o admin
     * Solo si estado='emitida'
     * Cambiar a 'borrador'
     * Guardar desbloqueado_por, motivo_desbloqueo
     * Incrementar revision_publica
3. Módulo app/planillas/sdi_validacion.py:
   - validar_sdi_grilla_mensual(carga_dict):
     * Aceptar ✓, O, X, NA (3 o 4 estados, a confirmar con Martín)
     * Bloquear otros estados
4. Tests:
   - Desbloquear carga emitida → OK
   - Desbloquear borrador → error
   - Desbloquear sin permisos → error
   - SDI-2 grilla con 3/4 estados → OK

CRITERIOS ACEPTACIÓN ETAPA 4:
✓ Desbloqueo implementado: motivo + creador/admin
✓ Revisión pública incrementada
✓ Validación SDI conforme (pendiente Martín 3 vs 4 estados)

---

ETAPA 5: IMPORTACIÓN 63 PLANILLAS RESTANTES
Encargo: Importar SAA-2–6, SAP-1–5, SCC-1–5, SDC-1–5, SEP-1–3, SGE-1–7, SHC-1–3, SIM-1–2, SRA-1–9, SRE-1–7, SSA-1–4, STM-1–8.

TAREAS:
1. Ejecutar importador_planillas.py: debe importar 63 nuevas, reportar 16 ya existentes
2. Habilitar en API:
   - Agregar 11 sistemas (SAP, SCC, SDC, SEP, SGE, SHC, SIM, SRA, SRE, SSA, STM) a app/config.py SISTEMAS_HABILITADOS
   - Migrations additive para cada sistema
3. UI: mostrar dropdown sistemas con los 15
4. Tests: 3 por planilla (carga borrador, validación, emisión)
   - 63 × 3 = 189 tests nuevos
   - Total: 232 + 189 = 421 tests

CRITERIOS ACEPTACIÓN ETAPA 5:
✓ 63 planillas importadas correctamente
✓ 11 sistemas habilitados en API
✓ 421 tests passing (232 + 189)
✓ Dropdown sistemas muestra 15

---

ETAPA 6: BÚSQUEDA, CONTINUIDAD, AUDITORÍA, DECISIÓN REAL VS PILOTO
Encargo: Búsqueda por número, auditoría, preparar transición piloto → real.

TAREAS:
1. API endpoint /api/carga/buscar?numero=12345:
   - Buscar por numero_registro
   - Retornar: cliente, sistema, planilla, estado, revision_publica, fecha_emision
2. Tabla Auditoria (app/models/__init__.py):
   - Registrar INSERT, UPDATE, DELETE, DESBLOQUEO
   - Campos: tabla, registro_id, accion, usuario_id, datos_anterior, datos_nuevo, timestamp
3. Modelo Visita (estructura compatible con cargas históricas):
   - visita_id UUID FK carga
   - sistema_id, planilla_id
   - año, mes, semana (S1–S5)
   - resultado JSON
4. Docs:
   - docs/BACKUP_Y_RESTAURACION.md (ya en Etapa 1)
   - docs/TRANSICION_PILOTO_A_REAL.md: checklist antes de flipear MODO_PILOTO=False
5. Config para transición:
   - MODO_PILOTO = True/False (inicio True)
   - EMPRESA_MANTENEDORA = "[Ejemplo] ACME Maintenance" (ficticio hasta autorización)
   - CERTIFICADO_N = "IFI-2024-00000" (ficticio)
   - MAIL_MODO_PRUEBA = True (no enviar reales hasta MODO_PILOTO=False)

CHECKLIST ANTES DE FLIPEAR A REAL:
✓ Respaldo Etapa 1 testeado en 010
✓ CUIT cliente real cargado
✓ 79 planillas, 15 sistemas activos
✓ Validaciones (O + observación, mediciones) OK
✓ Desbloqueo testeado
✓ Búsqueda funcional
✓ 421 tests passing
✓ Auditoría registrando cambios
✓ EMPRESA_MANTENEDORA y CERTIFICADO_N reales confirmados por Jorge
✓ Documentación completa

CRITERIOS ACEPTACIÓN ETAPA 6:
✓ Búsqueda por número funcional
✓ Auditoría registra todos los cambios
✓ Documentación de transición incluida
✓ Checklist listo para revisión Jorge

---

DECISIONES PENDIENTES (CONFIRMACIÓN JORGE ANTES DE CADA ETAPA)

Antes de Etapa 2:
- ¿Cómo generas READYPROOF_BACKUP_KEY? (1Password, archivo local, otra)

Antes de Etapa 3:
- ¿Si O falta observación: rechazar o completar automáticamente?
- ¿Mediciones obligatorias en TODOS campos con unidad, o solo verificación (ver)?

Antes de Etapa 4:
- Grillas semanal/mensual: ¿3 estados (✓/O/X) o 4 (✓/O/X/NA)? Confirma Martín.
- ¿Quién aprueba desbloqueo: solo creador/admin, o técnico también?

Antes de Etapa 5:
- ¿Cada planilla 3 tests (carga, validación, emisión) o más?

Antes de Etapa 6:
- ¿Cuándo estás listo para MODO_PILOTO=False?
- EMPRESA_MANTENEDORA y CERTIFICADO_N definitivos?

---

AHORA MISMO:
Responde las 3 preguntas del resumen ejecutivo:
1. ¿Autorizas Google Drive ahora? (rclone OAuth readyproof.ar@gmail.com)
2. ¿Quién hace test restauración? (vos, ops, Codex sugiere pasos)
3. ¿Cuándo esperas modo real? (timeline)

Con eso, arrancan Etapas 1–6 automáticamente sin esperar más.