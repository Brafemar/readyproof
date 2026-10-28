# Ejecutar desde el paquete individual; no utiliza una clave de root.
param([string]$DirectorioAcceso = (Join-Path $PSScriptRoot '..\acceso'))
$ErrorActionPreference = 'Stop'
$claveTecnico = Join-Path $DirectorioAcceso 'readyproof_tecnico_ed25519'
$hostsTecnico = Join-Path $DirectorioAcceso 'known_hosts'
if (-not (Test-Path -LiteralPath $claveTecnico) -or -not (Test-Path -LiteralPath $hostsTecnico)) {
    throw 'Descomprimir el paquete completo de acceso antes de iniciar el tunel.'
}
$identidadWindows = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
& icacls.exe $claveTecnico /inheritance:r /grant:r "${identidadWindows}:(R,W)" | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron restringir los permisos de la clave individual.' }
Write-Host 'Abrir http://127.0.0.1:8876/login y mantener esta consola abierta.'
Write-Host 'Usuario de la app: tecnico_readyproof. Ctrl+C cierra el tunel.'
& ssh -i $claveTecnico -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$hostsTecnico" -o ConnectTimeout=15 -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -N -L 127.0.0.1:8876:127.0.0.1:8000 readyproof_tunel_tecnico@67.205.170.29
if ($LASTEXITCODE -ne 0) { throw 'El tunel no pudo mantenerse; revisar conectividad y que el puerto 8876 este libre.' }
