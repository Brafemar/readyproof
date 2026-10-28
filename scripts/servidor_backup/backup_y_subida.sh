#!/bin/bash
set -euo pipefail
umask 077
cd /home/readyproof
exec /home/readyproof/venv/bin/python scripts/backup_readyproof.py backup
