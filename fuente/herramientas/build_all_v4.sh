#!/bin/bash
# build_all_v4.sh <scratch>: genera los 15 manuales con índice, fija el total de páginas del pie y los valida
B="$1"; T=$B/tools; O=$B/out_v4/manuales; mkdir -p $O
TPL=$B/out/SG-PEM-IFI_Plantilla_Maestra.docx
for SIG in SDI SRA SAP SRE SGE STM SBC SAA SHC SEP SSA SCC SAL SDC SIM; do
  C=$B/manuales/content_$SIG.py
  NOM=$(python3 -I -c "import importlib.util as u,sys;s=u.spec_from_file_location('m',sys.argv[1]);m=u.module_from_spec(s);s.loader.exec_module(m);print(m.NOM)" $C)
  F="$O/SG-PEM-IFI-$SIG $NOM.docx"
  python3 -I $T/build_manual.py $TPL $C "$F" | sed "s#$O/##"
  [ $SIG = SIM ] && python3 -I $T/insert_symbols.py "$F" $B/sim_png
  python3 -I $T/add_toc.py "$F" 2>&1 | tail -1
  python3 -I $T/fix_numpages.py "$F" | sed "s#$O/##"
  python3 /mnt/skills/public/docx/scripts/office/validate.py "$F" 2>&1 | tail -1
done
