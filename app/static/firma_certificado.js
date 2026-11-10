"use strict";
(() => {
  const csrf = document.querySelector('meta[name="csrf-token"]').content;
  const form = document.getElementById("formulario-firma");
  const estado = document.getElementById("estado-firma");
  const resultado = document.getElementById("resultado-firma");
  async function consultar(url, body) {
    const response = await fetch(url, { method: "POST", headers: { "X-CSRF-Token": csrf }, body });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "No se pudo completar la operación.");
    estado.textContent = data.activa
      ? `Activa · ${new Date(data.actualizada_en).toLocaleString("es-AR")} · SHA-256 ${data.sha256}`
      : "Sin firma activa.";
  }
  consultar("/api/admin/firma-certificado/estado").catch(error => { estado.textContent = error.message; });
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const boton = form.querySelector("button");
    boton.disabled = true;
    resultado.textContent = "";
    try {
      await consultar(form.action, new FormData(form));
      form.reset();
      resultado.textContent = "Firma guardada.";
    } catch (error) {
      resultado.textContent = error.message;
    } finally {
      boton.disabled = false;
    }
  });
})();
