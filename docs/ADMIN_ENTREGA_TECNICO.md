# Administración de la entrega privada al técnico

Guía para Jorge, no incluida en el paquete ni en los adjuntos automáticos.

Usuario de aplicación creado: **tecnico_readyproof**, rol técnico, cliente ficticio asignado. Acceso SSH del paquete: **readyproof_tunel_tecnico**, limitado al puerto de la aplicación. La clave de root de Jorge no forma parte del paquete.

La contraseña temporal quedó guardada únicamente en un archivo de root, modo 0600. Para consultarla en tu propia consola PowerShell:

```powershell
ssh -i "$env:USERPROFILE\.ssh\readyproof_deploy_67_205_170_29" -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes root@67.205.170.29 "cat /root/readyproof-tecnico-inicial.json"
```

No pegar la salida en el chat, capturas o documentación. Entregar la clave por un canal privado separado. El técnico debe cambiarla en Mi cuenta al primer ingreso; después corresponde retirar la copia temporal de forma controlada. Cambiar la contraseña no cambia su rol ni sus asignaciones.

Paquete local: `out/entrega_tecnico/readyproof-acceso-tecnico-privado.zip`. Contiene una clave SSH individual restringida, datos públicos de verificación del servidor, guías y script Windows. No contiene contraseña de la app, clave root, credenciales de Google ni de BD. Entregarlo por canal privado únicamente a la persona autorizada; otra persona necesita su propio acceso.

La casilla guardada en tecnico_readyproof es **jorgesanchezing@gmail.com**, exclusivamente para la prueba autorizada. Al entregar, el técnico guarda su dirección propia desde Mi cuenta. El correo de documentación incluye usuario y guías; no puede recuperar ni adjuntar la contraseña actual almacenada como hash.

Prueba de entrega: Gmail HTTPS, remitente readyproof.ar@gmail.com, destino de prueba de Jorge, mensaje Gmail `1a17dee776fd216c`, dos guías adjuntas y recepción confirmada. No hace falta repetir el envío para verificarlo. El permiso OAuth del remitente pertenece al servicio; no se distribuye al técnico.

El servidor sigue privado y admite ejemplos. La prueba física de Android, el go-live productivo y la vigencia/renovación de la autorización Google continúan bajo revisión de los responsables.
