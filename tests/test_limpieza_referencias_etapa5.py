"""Limpieza de referencias acotada, sin cerrar procesos reales."""
from pathlib import Path
import json
import subprocess
import pytest
from scripts import referencias_etapa5 as refs


def test_identifica_solo_perfil_y_ejecutable_propios(tmp_path):
    exe=tmp_path/"LibreOffice/program/soffice.exe"
    profile=(tmp_path/"r-unico/p0").as_uri()
    prep={"ejecutable":str(exe),"perfiles":[profile],"pids_preexistentes":[10]}
    def row(pid, path=exe, cli=profile):
        return {"ProcessId":pid,"ExecutablePath":str(path),"CommandLine":"-env:UserInstallation="+cli}
    rows=[row(10),row(11),row(12,cli="file:///otro/perfil"),row(13,path=tmp_path/"otra/soffice.exe"),row(14,path=exe.with_name("otro.exe"))]
    assert [r["ProcessId"] for r in refs._son_propios(rows,prep)]==[11]


def test_ejecutar_lote_conserva_argumentos_salida_timeout_y_registra_pid(monkeypatch):
    events=[]
    class Fake:
        pid=123;returncode=0
        def __init__(self,args,**kwargs):events.append((args,kwargs))
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def communicate(self,timeout):events.append(timeout);return b"pdf",b""
    monkeypatch.setattr(refs.subprocess,"Popen",Fake)
    prep={"iniciados":[]};args=["soffice.exe","--convert-to","pdf:calc_pdf_Export"]
    result=refs._ejecutar_lote(args,prep)
    assert events==[(args,{"stdout":subprocess.PIPE,"stderr":subprocess.PIPE}),300]
    assert result.returncode==0 and result.stdout==b"pdf" and result.stderr==b""
    assert prep["iniciados"][0]["pid"]==123


def test_limpieza_normal_y_cierre_solo_del_pid_propio(tmp_path,monkeypatch):
    exe=tmp_path/"program/soffice.exe";closed=[];rows=[]
    monkeypatch.setattr(refs,"_soffice_vivos",lambda:rows)
    monkeypatch.setattr(refs,"_cerrar_por_identidad",lambda row:closed.append(row["ProcessId"]))
    with refs._referencias_temporales(tmp_path) as prep:
        root=Path(prep["directorio"]);(root/"archivo").write_text("[Ejemplo]")
        profile=(root/"p0").as_uri();prep.update(ejecutable=str(exe),perfiles=[profile])
        rows.extend([{"ProcessId":123,"ExecutablePath":str(exe),"CommandLine":profile},
                     {"ProcessId":999,"ExecutablePath":str(exe),"CommandLine":"file:///sesion-ajena"}])
    assert closed==[123] and not root.exists()
    audit=json.loads(next(tmp_path.glob("r-*_limpieza.json")).read_text(encoding="utf-8"))
    assert audit["fallback_usado"] is False and audit["residuos"]==[]


def test_error_145_transitorio_se_reintenta_sin_fallback(tmp_path,monkeypatch):
    real=refs.shutil.rmtree;calls=[]
    monkeypatch.setattr(refs,"_soffice_vivos",lambda:[])
    monkeypatch.setattr(refs.time,"sleep",lambda _:None)
    def transient(path,*args,**kwargs):
        calls.append(str(path))
        if len(calls)==1:raise OSError(145,"[Ejemplo] directorio no vacío")
        return real(path,*args,**kwargs)
    monkeypatch.setattr(refs.shutil,"rmtree",transient)
    with refs._referencias_temporales(tmp_path) as prep:root=Path(prep["directorio"])
    assert not root.exists()
    audit=json.loads(next(tmp_path.glob("r-*_limpieza.json")).read_text(encoding="utf-8"))
    assert len(audit["intentos_limpieza"])==2 and not audit["fallback_usado"]


def test_maximo_cinco_intentos_residuo_reportado_sin_borrar_otra_carpeta(tmp_path,monkeypatch):
    other=tmp_path/"no_tocar";other.mkdir();(other/"archivo").write_text("[Ejemplo]")
    calls=[];created=[]
    class Temp:
        def __init__(self,*,prefix,dir,ignore_cleanup_errors):
            assert ignore_cleanup_errors is True
            self.name=str(Path(dir)/(prefix+"simulado"));Path(self.name).mkdir();created.append(self.name)
        def cleanup(self):calls.append(self.name)
    def blocked(path,*args,**kwargs):calls.append(str(path));raise OSError(145,"[Ejemplo] todavía ocupado")
    monkeypatch.setattr(refs,"TemporaryDirectory",Temp);monkeypatch.setattr(refs.shutil,"rmtree",blocked)
    monkeypatch.setattr(refs,"_soffice_vivos",lambda:[]);monkeypatch.setattr(refs.time,"sleep",lambda _:None)
    with pytest.warns(RuntimeWarning,match="Quedaron temporales"):
        with refs._referencias_temporales(tmp_path):pass
    assert len(calls)==5 and set(calls)==set(created)
    assert (other/"archivo").read_text()=="[Ejemplo]"
    audit=json.loads(next(tmp_path.glob("r-*_limpieza.json")).read_text(encoding="utf-8"))
    assert audit["fallback_usado"] is True and audit["carpeta_residual"]==created[0]
