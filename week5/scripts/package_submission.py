"""Create a portable source archive, with secrets, environments and model weights excluded."""
import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
# Explicit content allowlist; never recurse through a developer's environment or SQLite records.
roots = ['app', 'components', 'hooks', 'lib', 'backend/src', 'backend/scripts', 'backend/tests',
         'backend/data', 'week5', 'docs', 'public', '.github', '.openai']
files = ['README.md', '.gitignore', '.env.example', '.oxfmtrc.json', '.oxlintrc.json', 'components.json',
         'package.json', 'package-lock.json', 'tsconfig.json', 'vite.config.ts', 'next.config.ts',
         'docker-compose.yml', 'backend/pyproject.toml', 'backend/Dockerfile', 'backend/Modelfile']
selected = [ROOT / f for f in files if (ROOT / f).is_file()]
for folder in roots:
    for path in (ROOT / folder).rglob('*'):
        relative = path.relative_to(ROOT)
        if not path.is_file() or path.is_symlink():
            continue
        if any(part in {'runs', '__pycache__', '.pytest_cache', '.ruff_cache', 'node_modules', 'artifacts'} for part in relative.parts):
            continue
        if path.suffix in {'.db', '.sqlite', '.pyc', '.safetensors', '.gguf'} or path.name.startswith('.env'):
            continue
        selected.append(path)
archive = args.output / 'ultramedia-week5-source.zip'
checksums = {}
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(set(selected)):
        relative = path.relative_to(ROOT)
        checksums[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
        bundle.write(path, Path('ultramedia-studio') / relative)
    version = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    bundle.writestr('ultramedia-studio/SOURCE_MANIFEST.json', json.dumps({'git_head': version,
        'files_sha256': checksums, 'note': 'File hashes identify this exact archive, including any working changes.'}, indent=2))
(args.output / 'archive-sha256.json').write_text(json.dumps({archive.name: hashlib.sha256(archive.read_bytes()).hexdigest()}, indent=2)+'\n')
print(json.dumps({'archive': str(archive), 'files': len(checksums), 'bytes': archive.stat().st_size}))
