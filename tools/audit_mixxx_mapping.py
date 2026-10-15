"""Audit MIDI-address collisions and missing script bindings in a downloaded mapping."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def audit(path):
    path = Path(path)
    tree = ET.parse(path)
    addresses = defaultdict(list)
    script = '\n'.join((path.parent / f.attrib['filename']).read_text(encoding='utf-8-sig')
                       for f in tree.findall('.//scriptfiles/file'))
    missing = set()
    for control in tree.findall('.//controls/control'):
        status = int(control.findtext('status'), 0)
        note = int(control.findtext('midino'), 0)
        key = control.findtext('key')
        addresses[f'{status:02X}:{note:02X}'].append([control.findtext('group'), key])
        if control.find('options/script-binding') is not None:
            if not re.search(re.escape(key) + r'\s*=\s*function', script):
                missing.add(key)
    return {
        'controls': sum(map(len, addresses.values())),
        'duplicate_addresses': {k: v for k, v in addresses.items() if len(v) > 1},
        'missing_script_functions': sorted(missing),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mapping', type=Path)
    args = parser.parse_args()
    result = audit(args.mapping)
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result['duplicate_addresses'] or result['missing_script_functions']))
