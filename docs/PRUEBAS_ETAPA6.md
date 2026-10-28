# Verificación de etapa 6

La suite final contiene 541 casos: 494 ejecutados en Ubuntu con PostgreSQL temporal y 47 en Windows con LibreOffice y navegador. No se suman las ejecuciones de diagnóstico ni se cuentan dos veces los casos. Ambos XML finales están en `out/etapa6_final/`.

Instalar `requirements-dev.txt` en el entorno de desarrollo. Se requieren además PostgreSQL, LibreOffice y Node con Playwright y Chromium para los casos de navegador; las herramientas de revisión detectan las rutas configuradas en esta estación. Coverage y pypdfium2 son dependencias de prueba, no se incorporan al entorno productivo por esta entrega.

`scripts/revision_etapa6.py` prepara el paquete privado y separa los identificadores de pytest por plataforma. No ejecutar sus comandos de nuevo sobre la misma carpeta temporal: el comando Windows exige un directorio aún inexistente para proteger evidencia previa. El comando Linux usa una base temporal, sin credenciales de producción. Revisar las rutas antes de repetir en otra estación.

Combinar solo los dos archivos finales de cobertura mediante Coverage con `.coveragerc`. La medición corresponde a líneas Python de `app/`, no a JavaScript ni a cobertura de ramas. Resultado final: 93,04 %. Se verificaron además los dos PDF de modo, su formato A4 horizontal, logo, firmas y leyenda IRAM.

La verificación de servidor ensaya primero 014→016 en una copia aislada, exige la suite aprobada, respalda antes del corte y compara las filas anteriores. Mantiene `MODO_PILOTO=true` y `MAIL_MODO_PRUEBA=true`. El respaldo posterior se descarga, se restaura en otra base y se comparan tablas, binarios y PDF. Nunca se restaura sobre producción.

Durante el primer arranque se detectó que la máscara privada 0077 había dejado el directorio nuevo de auditoría sin acceso para el grupo del servicio. Se corrigió a root:readyproof 0750 y se hizo explícito chmod en el instalador. No fue necesario alterar la base ni los datos históricos.
