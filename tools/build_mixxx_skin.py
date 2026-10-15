"""Package the GPL Mixxx skin from its editable source, deterministically."""
from pathlib import Path
import hashlib
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def build():
    source = ROOT / 'mixxx' / 'AZ Touch'
    for file in source.glob('*.xml'):
        ET.parse(file)
    destination = ROOT / 'dist' / 'mixxx' / 'AZ-Touch-Mixxx.zip'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(source.rglob('*')):
            if file.is_file():
                info = zipfile.ZipInfo(str(file.relative_to(source.parent)).replace('\\', '/'), (2026, 10, 15, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, file.read_bytes())
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    (destination.parent / 'SHA256SUMS.txt').write_text(f'{digest}  {destination.name}\n')
    print(destination.name, digest)


if __name__ == '__main__':
    build()
