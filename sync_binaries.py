#!/usr/bin/env python3
"""Archive les binaires construits en .zip pour le site Astro et émet un manifeste.

Source : <racine du dépôt>/dist  (produit par ./build-all.sh)
Cible  : site-astro/public/bin/*.zip  (servi tel quel par le build Astro)
Manifeste : site-astro/src/data/binaries.json  (os, arch, taille, sha256 du .zip)

Le .zip est nommé par plateforme (<outil>-<os>-<arch>.zip) ; à l'intérieur,
le binaire porte le nom de la commande (why / why-lsp, avec .exe sur Windows),
pour être utilisable tel quel dès la décompression.

Usage :
    python3 sync_binaries.py

Deux modes :
  • dist/ présent → (re)zippe les binaires frais et réécrit le manifeste (dev local).
  • dist/ absent  → si public/bin/ contient déjà des .zip + src/data/binaries.json,
                    on les réutilise tels quels (CI / checkout propre) et on ne fait rien ;
                    sinon on échoue au lieu de laisser un build avec des liens cassés.
Le zipage est idempotent : il vide public/bin/ avant de rezipper, pour qu'aucun
fichier obsolète ne subsiste.
"""

import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent        # site-astro/
ROOT = HERE.parent                            # racine du dépôt
DIST = ROOT / "dist"
OUT_BIN = HERE / "public" / "bin"
OUT_DATA = HERE / "src" / "data"

# why / why-lsp  ×  darwin|linux|windows  ×  amd64|arm64  [.exe]
PATTERN = re.compile(r"^(why|why-lsp)-(darwin|linux|windows)-(amd64|arm64)(\.exe)?$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def version() -> str:
    try:
        out = subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--dirty"],
            cwd=ROOT, stderr=subprocess.DEVNULL, text=True,
        )
        return out.strip()
    except Exception:
        return "dev"


def make_zip(src: Path, dst: Path, arcname: str) -> None:
    """Comprime src dans dst, en donnant au binaire le nom de la commande."""
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(src, arcname=arcname)


def committed_artifacts() -> bool:
    """Vrai si le dépôt contient déjà des .zip et leur manifeste (mode CI / checkout propre)."""
    if not OUT_BIN.is_dir() or not (OUT_DATA / "binaries.json").is_file():
        return False
    return any(p.is_file() for p in OUT_BIN.glob("*.zip"))


def main() -> None:
    if not DIST.is_dir():
        if committed_artifacts():
            print(
                "→ dist/ introuvable : "
                f"{DIST}\n"
                "→ on réutilise les binaires déjà commités dans "
                f"{OUT_BIN.relative_to(HERE)}/ + {OUT_DATA.relative_to(HERE)}/binaries.json"
            )
            return
        raise SystemExit(
            f"✗ dist/ introuvable : {DIST}\n"
            f"  Et aucun binaire commité dans {OUT_BIN}/\n"
            f"  Soit construisez les binaires depuis la racine du dépôt : ./build-all.sh\n"
            f"  Soit committez public/bin/*.zip + src/data/binaries.json (comme pour la CI)."
        )

    files = sorted(p for p in DIST.iterdir() if p.is_file())
    matched = [f for f in files if PATTERN.match(f.name)]
    skipped = [f.name for f in files if not PATTERN.match(f.name)]

    if not matched:
        raise SystemExit(
            "✗ aucun binaire reconnu dans dist/\n"
            f"  Fichiers présents : {', '.join(f.name for f in files) or '(aucun)'}\n"
            "  Attendu : why-{darwin|linux|windows}-{amd64|arm64}[.exe], why-lsp-…\n"
            "  (ne lancez pas build-all.sh avec --tar ici : il faut les binaires nus)"
        )

    # Nettoyage puis rezipage.
    if OUT_BIN.exists():
        shutil.rmtree(OUT_BIN)
    OUT_BIN.mkdir(parents=True, exist_ok=True)
    OUT_DATA.mkdir(parents=True, exist_ok=True)

    binaries = []
    for src in matched:
        m = PATTERN.match(src.name)
        tool, os_, arch = m.group(1), m.group(2), m.group(3)
        zip_name = f"{tool}-{os_}-{arch}.zip"           # .zip nommé par plateforme
        inner = f"{tool}.exe" if os_ == "windows" else tool   # commande à l'intérieur (why / why-lsp)
        dst = OUT_BIN / zip_name
        make_zip(src, dst, arcname=inner)
        binaries.append({
            "name": zip_name,                            # nom du .zip = lien de téléchargement
            "binary": inner,                             # commande dans le .zip (ex. why, why-lsp, why.exe)
            "tool": tool,
            "os": os_,
            "arch": arch,
            "sizeBytes": dst.stat().st_size,             # taille du .zip
            "sha256": sha256(dst),                       # empreinte du .zip
        })

    manifest = {
        "version": version(),
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "binaries": binaries,
    }
    manifest_path = OUT_DATA / "binaries.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def mb(n: int) -> str:
        return f"{n / 1_048_576:.1f} Mo"

    print(f"→ {len(matched)} binaires archivés en .zip dans public/bin/")
    for b in binaries:
        print(f"   {b['name']:30} {mb(b['sizeBytes']):>7}  (contient {b['binary']})")
    if skipped:
        print(f"   (ignorés : {', '.join(skipped)})")
    print(f"→ manifeste : src/data/binaries.json (build {manifest['version']})")


if __name__ == "__main__":
    main()
