from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / 'mixxx' / 'AZ Touch'
sys.path.insert(0, str(ROOT / 'tools'))
from audit_mixxx_mapping import audit


class MixxxArtifacts(unittest.TestCase):
    def test_wave_touch_and_drop_are_locked(self):
        count = 0
        for file in SKIN.glob('*.xml'):
            for node in ET.parse(file).iter():
                if node.tag not in ('Visual', 'Overview'):
                    continue
                count += 1
                connections = {(c.findtext('ConfigKey'), c.findtext('BindProperty'))
                               for c in node.findall('Connection')}
                for prop in ('enabled', 'acceptDrops'):
                    self.assertIn(('[Skin],wave_touch_enabled', prop), connections)
        self.assertGreaterEqual(count, 6)
        attrs = ET.parse(SKIN / 'skin.xml').findall('.//attribute')
        self.assertEqual(next(a.text for a in attrs if a.get('config_key') == '[Skin],wave_touch_enabled'), '0')

    def test_views_show_correct_decks(self):
        pages = ET.parse(SKIN / 'wavebank.xml').findall('.//WidgetStack/Children/WidgetGroup')
        self.assertEqual(len(pages), 3)
        for page, expected in zip(pages, ([1, 2], [3, 4], [3, 1, 2, 4])):
            actual = [int(t.findtext('SetVariable')) for t in page.findall('.//Template')
                      if t.get('src') == 'skin:waveform_colored.xml']
            self.assertEqual(actual, expected)

    def test_all_four_summaries_survive_view_changes(self):
        for name in ('overview.xml', 'deckminimal.xml'):
            tree = ET.parse(SKIN / name)
            self.assertFalse(any(c.text == '[Skin],show_4decks' for c in tree.iter('ConfigKey')))
        summary = ET.parse(SKIN / 'overview.xml').findall('.//Template')
        channels = [int(t.findtext('SetVariable')) for t in summary if t.get('src') == 'skin:deck.xml']
        self.assertEqual(channels, [1, 2, 3, 4])

    def test_load_buttons_and_package(self):
        tree = ET.parse(SKIN / 'library.xml')
        loads = [c.text for c in tree.iter('ConfigKey') if c.text and 'LoadSelectedTrack' in c.text]
        self.assertEqual(loads, [f'[Channel{n}],LoadSelectedTrack' for n in range(1, 5)])
        with zipfile.ZipFile(ROOT / 'dist/mixxx/AZ-Touch-Mixxx.zip') as archive:
            names = archive.namelist()
            self.assertIn('AZ Touch/LICENSE', names)
            self.assertIn('AZ Touch/skin.xml', names)
            self.assertFalse(any(n.endswith(('.js', '.wav', '.mp3')) for n in names))

    def test_audit_detects_conflicting_bindings(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'bad.midi.xml'
            path.write_text('<MixxxControllerPreset><controller><controls>'
                '<control><status>0x90</status><midino>0x58</midino><group>[Channel1]</group><key>sync_enabled</key></control>'
                '<control><status>0x90</status><midino>0x58</midino><group>[Channel1]</group><key>sync_key</key></control>'
                '</controls></controller></MixxxControllerPreset>')
            self.assertEqual(len(audit(path)['duplicate_addresses']['90:58']), 2)


if __name__ == '__main__':
    unittest.main()
