"""Guarda una copia de recuperación cifrada para el usuario actual de Windows."""
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import subprocess


class Blob(ctypes.Structure):
    _fields_ = [('size', wintypes.DWORD), ('data', ctypes.POINTER(ctypes.c_ubyte))]


def protect(data):
    buffer = ctypes.create_string_buffer(data)
    source = Blob(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    target = Blob()
    crypt = ctypes.WinDLL('crypt32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    crypt.CryptProtectData.argtypes = [ctypes.POINTER(Blob), wintypes.LPCWSTR, ctypes.POINTER(Blob),
                                       ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    crypt.CryptProtectData.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    if not crypt.CryptProtectData(ctypes.byref(source), 'readyproof backup key', None, None, None, 1, ctypes.byref(target)):
        raise OSError('No se pudo proteger la clave con Windows DPAPI.')
    try:
        return ctypes.string_at(target.data, target.size)
    finally:
        kernel.LocalFree(target.data)


def main():
    if os.name != 'nt':
        raise ValueError('Ejecutar desde la PC Windows administradora de Jorge.')
    directory = Path.home()/'.ssh'
    target = directory/'readyproof_backup_key.dpapi'
    if target.exists():
        raise ValueError('La copia ya existe; verificarla antes de reemplazar.')
    command = ['ssh', '-i', str(directory/'readyproof_deploy_67_205_170_29'), '-o', 'IdentitiesOnly=yes',
               '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=15',
               'root@67.205.170.29', 'cat /etc/readyproof/backup.env']
    result = subprocess.run(command, capture_output=True, timeout=30)
    if result.returncode or not result.stdout.startswith(b'READYPROOF_BACKUP_KEY='):
        raise ValueError('No se pudo recuperar la clave privada por SSH.')
    data = result.stdout
    encrypted = protect(data)
    # Comprobar la copia mediante DPAPI antes de guardarla.
    crypt = ctypes.WinDLL('crypt32', use_last_error=True)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    source_buffer = ctypes.create_string_buffer(encrypted)
    source = Blob(len(encrypted), ctypes.cast(source_buffer, ctypes.POINTER(ctypes.c_ubyte)))
    target_blob = Blob()
    crypt.CryptUnprotectData.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.POINTER(Blob), ctypes.c_void_p,
                                        ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    crypt.CryptUnprotectData.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    if not crypt.CryptUnprotectData(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target_blob)):
        raise ValueError('No se pudo verificar la copia DPAPI.')
    try:
        if ctypes.string_at(target_blob.data, target_blob.size) != data:
            raise ValueError('La copia de recuperación no coincide.')
    finally:
        kernel.LocalFree(target_blob.data)
    with target.open('xb') as file:
        file.write(encrypted)
    print(json.dumps({'estado':'clave_protegida_y_verificada', 'archivo':str(target),
                      'huella':hashlib.sha256(data).hexdigest(), 'proteccion':'DPAPI CurrentUser'}))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('No se completó el resguardo de la clave. No compartir archivos privados.')
        raise SystemExit(1)
