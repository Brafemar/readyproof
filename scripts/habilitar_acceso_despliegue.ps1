# Ejecutar en la consola privada de Jorge; no recibe contraseñas por argumentos.
$ErrorActionPreference = 'Stop'
$destino = 'root@67.205.170.29'
$raizProyecto = Split-Path -Parent $PSScriptRoot
$pythonProyecto = Join-Path $raizProyecto '.venv\Scripts\python.exe'
$directorioSSH = Join-Path $env:USERPROFILE '.ssh'
$claveDespliegue = Join-Path $directorioSSH 'readyproof_deploy_67_205_170_29'

if (-not (Test-Path -LiteralPath $pythonProyecto)) {
    throw 'No se encontró el Python del proyecto. Ejecutar desde la copia de readyproof preparada.'
}
New-Item -ItemType Directory -Path $directorioSSH -Force | Out-Null
if (-not (Test-Path -LiteralPath $claveDespliegue)) {
    & $pythonProyecto -c "import subprocess,sys; subprocess.run(['ssh-keygen','-q','-t','ed25519','-f',sys.argv[1],'-N','','-C','readyproof-despliegue-privado'],check=True)" $claveDespliegue
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo generar la clave SSH.' }
}
if (-not (Test-Path -LiteralPath "$claveDespliegue.pub")) {
    throw 'Existe una clave sin archivo público. No se sobrescribe; consultar antes de continuar.'
}

# Restringir la clave privada a la cuenta Windows que ejecuta el procedimiento.
$identidadWindows = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
& icacls.exe $claveDespliegue /inheritance:r /grant:r "${identidadWindows}:(R,W)" | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron restringir los permisos de la clave privada.' }

# Capturar stderr fuera de PowerShell 5.1: un rechazo esperado de SSH debe
# habilitar el paso interactivo, no convertirse en NativeCommandError.
& $pythonProyecto -c "import subprocess,sys; result=subprocess.run(['ssh','-i',sys.argv[1],'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10',sys.argv[2],'true'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); sys.exit(0 if result.returncode==0 else 1)" $claveDespliegue $destino
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Se autorizará esta clave en root@67.205.170.29. No instala ni publica la aplicación.'
    Write-Host 'Ingresá la contraseña de root solo cuando SSH la solicite; no aparecerá en pantalla.'
    $clavePublica = (Get-Content -LiteralPath "$claveDespliegue.pub" -Raw).Trim()
    if ($clavePublica -notmatch '^ssh-ed25519 [A-Za-z0-9+/=]+(?: .*)?$') {
        throw 'Formato de clave pública no esperado.'
    }
    $lineaAutorizada = 'no-agent-forwarding,no-X11-forwarding,no-pty ' + $clavePublica
    $comandoInstalacion = 'umask 077; mkdir -p /root/.ssh && chmod 700 /root/.ssh && touch /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys && printf ''\n'' >> /root/.ssh/authorized_keys && cat >> /root/.ssh/authorized_keys'
    $lineaAutorizada | & ssh -o StrictHostKeyChecking=yes -o ConnectTimeout=10 -o PubkeyAuthentication=no -o PreferredAuthentications=keyboard-interactive,password $destino $comandoInstalacion
    if ($LASTEXITCODE -ne 0) { throw 'SSH no autorizó la clave. No se realizaron pasos de despliegue.' }
}

& ssh -i $claveDespliegue -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 $destino 'echo Acceso_SSH_readyproof_verificado'
if ($LASTEXITCODE -ne 0) { throw 'No se confirmó el acceso por clave. Conservar el diagnóstico y consultar.' }
Write-Host 'Listo. Avisá en el chat: Acceso SSH readyproof verificado. No compartas contraseñas ni archivos de clave.'
