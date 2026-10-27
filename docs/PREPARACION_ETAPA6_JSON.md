# Preparación de definiciones JSON para etapa 6

Los cuatro archivos de fuente/planillas/ son exportaciones de los diccionarios originales. El kit sigue siendo la fuente de verdad. No se editaron los originales Python ni el generador.

- SDI.json: SISTEMAS[SDI] completo de planillas_data2.py, 5 planillas.
- SBC.json: SISTEMAS[SBC] completo de planillas_data2.py, 6 planillas.
- SAL.json: SISTEMAS[SAL] completo de planillas_data2.py, 4 planillas.
- SAA-1.json: definición número 1 de SISTEMAS[SAA] en planillas_data3.py.

## Estructura

Cada archivo tiene codigo, version v1 y sistema_tipo SG-PEM-IFI como metadatos del contenedor, más origen/generador con ruta relativa y SHA256. Esos metadatos no renombraron sistemas ni modificaron la revisión 00-26 del generador.

cabecera contiene los 11 campos comunes y sus celdas, tomados del adaptador existente. datos conserva el diccionario de sistema y sus planillas, bloques, filas, opciones y unidades. firmas contiene los dos espacios del pie, con las etiquetas extraídas del generador original. No contiene firmas personales ni cargas de clientes.

Las tuplas Python se representan como arrays JSON, conservando el orden. Esto es la representación declarativa; un futuro adaptador para llamar al generador deberá recuperar las tuplas según el contexto de bloques/campos. No se entrega el JSON directamente al generador ni se cambia el generador para esta preparación.

## Conversión y validación

```powershell
.venv\Scripts\python.exe scripts/convertir_planillas_json.py
.venv\Scripts\python.exe scripts/convertir_planillas_json.py --verificar
.venv\Scripts\python.exe -m json.tool fuente/planillas/SDI.json > $null
```

Repetir json.tool con SBC.json, SAL.json y SAA-1.json. El conversor crea archivos ausentes y compara los existentes; si difieren del origen, falla sin sobrescribirlos. No borra ni regenera archivos distintos automáticamente.

Las pruebas de tests/test_preparacion_etapa6.py verifican cada JSON, claves duplicadas, equivalencia con Python, SHA256 de procedencia y conservación completa de los grupos. El manifiesto de integridad original y los recuentos están en out/etapa6_inventario/.

## Estado

Preparación JSON terminada; la migración 006, el importador y el vínculo de los tres manuales se auditarán y completarán después. Para los manuales ficticios se usarán los títulos del kit confirmados por Jorge, con prefijo [Ejemplo]. Esta conversión no habilita generación/uso de otras planillas ni correo real. M1 está resuelto para la leyenda y los demás controles de uso real siguen pendientes y la prueba del iPhone permanece suspendida.
