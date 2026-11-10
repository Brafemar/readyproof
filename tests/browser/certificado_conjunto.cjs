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
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), 390);
    await page.locator("#fecha").fill("2028-01-31");
    await page.locator("#intervencion").fill("2028-01-30");
    await page.locator("#carga_1").selectOption({ index: 1 });
    await page.locator("#cantidad_1").fill("1");
    await page.locator("#unidad_1").selectOption("meses");
    await page.locator("#establecimiento").fill("[Ejemplo] Sede ficticia");
    await page.locator("#dictamen").fill("[Ejemplo] Dictamen de prueba");
    const agregar = page.getByRole("button", { name: "Agregar planilla" });
    await agregar.click();
    await agregar.click();
    assert.match(await page.locator("#limite-planillas").textContent(), /máximo 2 planillas/);
    if (data.segunda) {
      await page.locator("#carga_1").selectOption(data.primera);
      await page.locator("#carga_2").selectOption(data.segunda);
      await page.locator("#cantidad_2").fill("7");
      await page.locator("#unidad_2").selectOption("dias");
    }
    await page.locator("[name=confirmacion]").check();
    await page.screenshot({ path: path.join(data.salida, "formulario_390.png"), fullPage: true });
    const [download] = await Promise.all([page.waitForEvent("download"),
      page.getByRole("button", { name: "Descargar propuesta PDF" }).click()]);
    await download.saveAs(path.join(data.salida, "propuesta_conjunta.pdf"));
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
