from hashlib import sha256
from io import BytesIO

from pypdf import PdfReader


def test_flujo_completo_de_ejemplo(client, catalogo, datos_api):
    _, sistema, planilla = catalogo
    response = client.post("/api/cargas", json={"sistema_id": sistema["id"], "planilla_id": planilla["id"], "datos": datos_api})
    assert response.status_code == 201
    carga = response.get_json()
    datos_api["observaciones"] = ["[Ejemplo] Flujo local de API"]
    saved = client.put(f"/api/cargas/{carga['id']}/borrador", json={"revision": 1, "datos": datos_api})
    assert saved.status_code == 200 and saved.get_json()["revision"] == 2
    finalized = client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": 2})
    assert finalized.status_code == 200 and finalized.get_json()["revision"] == 3
    emitted = client.post(f"/api/cargas/{carga['id']}/emitir", json={"revision": 3})
    assert emitted.status_code == 201
    result = emitted.get_json()
    assert result["estado"] == "emitida" and result["revision"] == 4
    download = client.get(f"/api/cargas/{carga['id']}/pdf")
    assert download.status_code == 200 and download.mimetype == "application/pdf"
    assert download.headers["Cache-Control"] == "no-store"
    assert sha256(download.data).hexdigest() == result["pdf_sha256"]
    document = PdfReader(BytesIO(download.data))
    assert len(document.pages) == 2
    assert all(len(page.images) == 2 for page in document.pages)
    text = "\n".join(page.extract_text() for page in document.pages)
    assert "[Ejemplo]" in text and "T.C. 3 AÑOS" in text
    revisions = client.get(f"/api/cargas/{carga['id']}/revisiones").get_json()
    assert [r["numero"] for r in revisions] == [1, 2, 3, 4]
    assert [r["evento"] for r in revisions] == ["creada", "borrador_guardado", "finalizada", "emitida"]
    assert client.post(f"/api/cargas/{carga['id']}/emitir", json={"revision": 4}).status_code == 409
