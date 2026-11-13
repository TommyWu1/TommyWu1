import unittest
from datetime import date
from generate import streaks, escape, room
class ProfileTests(unittest.TestCase):
 def test_gap_resets_best(self):
  self.assertEqual(streaks([{'date':'2026-11-08','contributionCount':1},{'date':'2026-11-09','contributionCount':2},{'date':'2026-11-10','contributionCount':0},{'date':'2026-11-11','contributionCount':1}],date(2026,11,12)),(1,2))
 def test_stale_data_has_no_current_streak(self):
  self.assertEqual(streaks([{'date':'2026-11-01','contributionCount':5}],date(2026,11,12)),(0,1))
 def test_xml_escape(self):self.assertEqual(escape('<tag>&'), '&lt;tag&gt;&amp;')
 def test_independent_room(self):
  svg=room(['fix: <issue> & test'],['Python'])
  self.assertNotIn('gitskins',svg.lower());self.assertIn('prefers-reduced-motion',svg)
  import xml.etree.ElementTree as ET
  ET.fromstring(svg)
if __name__=='__main__':unittest.main()

class RefreshTests(unittest.TestCase):
 def test_network_failure_preserves_existing_files(self):
  from unittest.mock import patch
  from pathlib import Path
  import refresh
  before={p:p.read_bytes() for folder in ['data','assets'] for p in (refresh.P/folder).glob('*') if p.is_file()}
  with patch.object(refresh,'api',side_effect=RuntimeError('network unavailable')):
   with self.assertRaises(RuntimeError):refresh.refresh()
  self.assertTrue(all(p.read_bytes()==data for p,data in before.items()))
 def test_deliverable_svg_is_self_contained(self):
  import xml.etree.ElementTree as ET
  from generate import A
  for file in A.glob('*.svg'):
   root=ET.parse(file).getroot()
   for element in root.iter():
    for attr,value in element.attrib.items():
     if attr.endswith('href'):self.assertTrue(value.startswith(('data:','#')))
   self.assertNotIn('gitskins',file.read_text().lower())
