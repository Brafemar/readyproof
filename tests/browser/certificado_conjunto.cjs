"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
(async () => {
  const data = JSON.parse(fs.readFileSync(0, "utf8"));
  const executablePath = [process.env.READYPROOF_BROWSER, chromium.executablePath(),
    "C:/Program Files/Google/Chrome/Application/chrome.exe"].find(p => p && fs.existsSync(p));
  assert.ok(executablePath);
  const browser = await chromium.launch({ executablePath, headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, acceptDownloads: true });
    await page.route("**/*", route => new URL(route.request().url()).origin === data.url ? route.continue() : route.abort());
    await page.goto(data.url + "/login");
    await page.locator("#login").fill(data.usuario.login);
    await page.locator("#clave").fill(data.usuario.clave);
    await Promise.all([page.waitForURL(data.url + "/"), page.getByRole("button", { name: "Ingresar", exact: true }).click()]);
    if (data.verificarFirmaVacia) {
      await page.getByRole("link", { name: "Administración", exact: true }).click();
      await page.getByRole("link", { name: "Firma del certificado", exact: true }).click();
      await page.getByText("Sin firma activa.").waitFor();
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 390);
      await page.screenshot({ path: path.join(data.salida, "firma_admin_390.png"), fullPage: true });
      await page.goto(data.url + "/");
    }
    await page.getByRole("link", { name: "Certificado conjunto" }).click();
    assert.equal(await page.getByRole("button", { name: "Emitir certificado", exact: true }).isEnabled(), true);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 390);
    await page.locator("#fecha").fill("2028-01-31");
    await page.locator("#intervencion").fill("2028-01-30");
    await page.locator("#carga_1").selectOption({ index: 1 });
    const periodicidad = page.getByLabel("Periodicidad", { exact: true });
    const vigencia = page.locator("#vigencia-hasta");
    assert.equal(await vigencia.textContent(), "—");
    for (const [opcion, hasta] of Object.entries({
      mensual: "29/02/2028", trimestral: "29/04/2028",
      semestral: "28/07/2028", anual: "29/01/2029"
    })) {
      await periodicidad.selectOption(opcion);
      assert.equal(await vigencia.textContent(), hasta);
    }
    await periodicidad.selectOption("mensual");
    await page.locator("#fecha").fill("2027-01-31");
    assert.equal(await vigencia.textContent(), "01/03/2027");
    await page.locator("#fecha").fill("2028-01-31");
    await page.locator("#intervencion").fill("2028-02-01");
    assert.equal(await vigencia.textContent(), "29/02/2028");
    await page.locator("#establecimiento").fill("[Ejemplo] Sede ficticia");
    const dictamen = page.getByRole("textbox", { name: "Dictamen", exact: true });
    assert.equal(await dictamen.count(), 1);
    assert.equal(await page.getByText("Dictamen de prueba", { exact: true }).count(), 0);
    await dictamen.fill("[Ejemplo] Dictamen de prueba");
    const agregar = page.getByRole("button", { name: "Agregar planilla" });
    await agregar.click();
    await agregar.click();
    assert.match(await page.locator("#limite-planillas").textContent(), /máximo 2 planillas/);
    if (data.segunda) {
      await page.locator("#carga_1").selectOption(data.primera);
      await page.locator("#carga_2").selectOption(data.segunda);
    }
    await page.locator("[name=confirmacion]").check();
    await page.screenshot({ path: path.join(data.salida, "formulario_390.png"), fullPage: true });
    const [download] = await Promise.all([page.waitForEvent("download"),
      page.getByRole("button", { name: "Descargar propuesta PDF" }).click()]);
    await download.saveAs(path.join(data.salida, "propuesta_conjunta.pdf"));
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
