# Mantener esta consola abierta durante el uso de readyproof por tunel SSH.
$ErrorActionPreference = 'Stop'
$claveDespliegue = Join-Path $env:USERPROFILE '.ssh\readyproof_deploy_67_205_170_29'
if (-not (Test-Path -LiteralPath $claveDespliegue)) {
    throw 'Falta la clave de acceso. Ejecutar primero habilitar_acceso_despliegue.ps1.'
}
Write-Host 'Abrir http://127.0.0.1:8876/login y mantener esta consola abierta.'
Write-Host 'El puerto 8876 corresponde al servidor remoto. Ctrl+C cierra el tunel.'
& ssh -i $claveDespliegue -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -N -L 127.0.0.1:8876:127.0.0.1:8000 root@67.205.170.29
if ($LASTEXITCODE -ne 0) {
    throw 'El tunel no pudo mantenerse. Revisar conectividad y que el puerto 8876 este libre.'
}
