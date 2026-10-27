"""Interfaz local de carga y recursos sin servicios externos."""
from flask import Blueprint, current_app, jsonify, render_template, send_from_directory
from ..planillas.piloto import datos_ejemplo
from ..planillas.validacion import FECHAS, ENTEROS
web = Blueprint("web", __name__)

@web.get("/")
def inicio():
    return render_template("carga.html")

@web.get("/sw.js")
def service_worker():
    response = send_from_directory(current_app.static_folder, "sw.js", mimetype="application/javascript")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@web.get("/api/ejemplo/saa1")
def ejemplo():
    data = datos_ejemplo()
    data["cabecera"]["empresa_mantenedora"] = "readyproof"
    data["cabecera"]["fecha"] = data["cabecera"]["fecha"].isoformat()
    for title, label in FECHAS:
        data["bloques"][title][label] = "2026-10-25"
    for title, label in ENTEROS:
        data["bloques"][title][label] = 1
    return jsonify(data)
