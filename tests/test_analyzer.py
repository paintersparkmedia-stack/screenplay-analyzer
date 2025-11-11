"""Tests for screenplay analyzer"""

import unittest
from preston.parser import ScreenplayParser
from preston.analyzer import ScreenplayAnalyzer


class TestScreenplayAnalyzer(unittest.TestCase):
    """Test cases for ScreenplayAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        screenplay = """INT. COFFEE SHOP - DAY

ALICE
Hello everyone.

BOB
Hi Alice.

ALICE
How are you doing?

EXT. PARK - NIGHT

CHARLIE
It's a nice evening.

ALICE
Yes, it is.
"""
        self.parser = ScreenplayParser()
        self.parser.parse(screenplay)
        self.analyzer = ScreenplayAnalyzer(self.parser)
    
    def test_get_character_statistics(self):
        """Test getting character statistics"""
        stats = self.analyzer.get_character_statistics()
        
        self.assertIn("ALICE", stats)
        self.assertIn("BOB", stats)
        self.assertIn("CHARLIE", stats)
        
        # Alice has 3 dialogue lines
        self.assertEqual(stats["ALICE"]["dialogue_lines"], 3)
        # Bob has 1 dialogue line
        self.assertEqual(stats["BOB"]["dialogue_lines"], 1)
    
    def test_get_top_characters(self):
        """Test getting top characters by dialogue"""
        top_chars = self.analyzer.get_top_characters(2)
        
        self.assertEqual(len(top_chars), 2)
        # Alice should be first (most dialogue)
        self.assertEqual(top_chars[0][0], "ALICE")
    
    def test_get_scene_count(self):
        """Test getting scene count"""
        count = self.analyzer.get_scene_count()
        self.assertEqual(count, 2)
    
    def test_get_dialogue_vs_action_ratio(self):
        """Test calculating dialogue vs action ratio"""
        ratio = self.analyzer.get_dialogue_vs_action_ratio()
        
        self.assertIn("dialogue_lines", ratio)
        self.assertIn("action_lines", ratio)
        self.assertGreater(ratio["dialogue_lines"], 0)
    
    def test_get_scenes_by_location(self):
        """Test grouping scenes by location"""
        locations = self.analyzer.get_scenes_by_location()
        
        self.assertEqual(locations["int_count"], 1)
        self.assertEqual(locations["ext_count"], 1)
        self.assertEqual(len(locations["interior"]), 1)
        self.assertEqual(len(locations["exterior"]), 1)
    
    def test_get_character_interactions(self):
        """Test finding character interactions"""
        interactions = self.analyzer.get_character_interactions()
        
        # Alice appears with Bob in scene 1 and Charlie in scene 2
        self.assertIn("BOB", interactions["ALICE"])
        self.assertIn("CHARLIE", interactions["ALICE"])
        
        # Bob only appears with Alice
        self.assertIn("ALICE", interactions["BOB"])
        self.assertEqual(len(interactions["BOB"]), 1)
    
    def test_generate_report(self):
        """Test generating full report"""
        report = self.analyzer.generate_report()
        
        self.assertIn("PRESTON SCREENPLAY ANALYSIS REPORT", report)
        self.assertIn("SCENE STATISTICS", report)
        self.assertIn("CHARACTER STATISTICS", report)
        self.assertIn("CONTENT BREAKDOWN", report)


if __name__ == '__main__':
    unittest.main()
