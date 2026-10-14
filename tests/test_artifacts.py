"""Useful regressions for packaging, deck routing, guards, and shield coverage."""
import contextlib
import hashlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_skin import package
from validate_skin import validate


class Artifacts(unittest.TestCase):
    def setUp(self):
        self.path=ROOT/'dist/AZ-Touch-3x2.zip'
        with ZipFile(self.path) as z: self.files={n:z.read(n) for n in z.namelist()}
        self.root=ET.fromstring(self.files['az-touch.xml'])

    def bad_archive(self, root):
        files=dict(self.files);files['az-touch.xml']=ET.tostring(root)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'bad.zip';package(p,files)
            with self.assertRaises(AssertionError): validate(p)

    def test_skin_and_spike_validate(self):
        for path in (ROOT/'dist').glob('*.zip'):
            with contextlib.redirect_stdout(io.StringIO()): validate(path)

    def test_repeat_build_is_identical(self):
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'dist').glob('*.zip')}
        subprocess.run([sys.executable,str(ROOT/'tools/build_skin.py')],check=True,stdout=subprocess.DEVNULL)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'dist').glob('*.zip')}
        self.assertEqual(before,after)

    def test_four_logical_decks(self):
        four=self.root.find(".//panel[@name='four']")
        self.assertEqual([d.get('deck') for d in four.findall('deck')],['1','2','3','4'])
        for d in four.findall('deck'):
            self.assertEqual(len(d.findall('scratchwave')),1)
            self.assertEqual(len(d.findall('songpos')),1)

    def test_modes_do_not_target_wrong_decks(self):
        for name,decks in [('two12',['1','2']),('two34',['3','4'])]:
            p=self.root.find(f".//panel[@name='{name}']")
            self.assertEqual([d.get('deck') for d in p.findall('deck')],decks)

    def test_unguarded_load_rejected(self):
        b=next(e for e in self.root.iter('button') if e.get('action','').endswith(' load'))
        b.set('action','deck 1 load');self.bad_archive(self.root)

    def test_wrong_guard_deck_rejected(self):
        b=next(e for e in self.root.iter('button') if e.get('action','').endswith(' load'))
        b.set('action','deck 1 play ? nothing : deck 2 load');self.bad_archive(self.root)

    def test_removed_input_shield_rejected(self):
        d=self.root.find(".//panel[@name='four']/deck")
        b=next(e for e in d.findall('button') if e.get('action')=='nothing')
        d.remove(b);self.bad_archive(self.root)

    def test_navigation_reference_rejected(self):
        self.root.find('button').set('action',"skin_panel 'missing' on")
        self.bad_archive(self.root)

    def test_off_canvas_geometry_rejected(self):
        self.root.find('.//scratchwave/pos').set('x','1360')
        self.bad_archive(self.root)

    def test_initialization_must_not_change_audio(self):
        self.root.find('oninit').set('action','master_volume 0%')
        self.bad_archive(self.root)

    def test_checksum_manifest_matches(self):
        for line in (ROOT/'dist/SHA256SUMS.txt').read_text().splitlines():
            expected,name=line.split()
            self.assertEqual(hashlib.sha256((ROOT/'dist'/name).read_bytes()).hexdigest(),expected)


if __name__=='__main__': unittest.main()
