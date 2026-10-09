import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import validate
class TournamentTests(unittest.TestCase):
    def test_structural_integrity(self):validate.main()
    def test_unique_positive_scores(self):
        x=json.loads((ROOT/"tournament/S000/data.json").read_text())
        self.assertEqual(len(x),10)
        self.assertTrue(all(c["score"]>0 for c in x))
    def test_separate_handoffs(self):
        self.assertIn("P001-S000", (ROOT/"papers/P001_S000_KICKOFF_PROMPT.md").read_text())
        self.assertIn("S001", (ROOT/"sessions/NEXT_SESSION.md").read_text())
if __name__=="__main__":unittest.main()
