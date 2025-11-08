"""Tests for screenplay parser"""

import unittest
from preston.parser import ScreenplayParser


class TestScreenplayParser(unittest.TestCase):
    """Test cases for ScreenplayParser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = ScreenplayParser()
        
    def test_parse_scene_heading(self):
        """Test parsing scene headings"""
        screenplay = """INT. COFFEE SHOP - DAY

Some action here.
"""
        self.parser.parse(screenplay)
        
        self.assertEqual(len(self.parser.scenes), 1)
        self.assertEqual(self.parser.scenes[0].heading, "INT. COFFEE SHOP - DAY")
    
    def test_parse_character_dialogue(self):
        """Test parsing character dialogue"""
        screenplay = """INT. ROOM - DAY

JOHN
Hello, how are you?

JANE
I'm doing well, thanks.
"""
        self.parser.parse(screenplay)
        
        self.assertIn("JOHN", self.parser.characters)
        self.assertIn("JANE", self.parser.characters)
        self.assertEqual(len(self.parser.characters["JOHN"].dialogue_lines), 1)
        self.assertEqual(len(self.parser.characters["JANE"].dialogue_lines), 1)
    
    def test_parse_multiline_dialogue(self):
        """Test parsing multi-line dialogue"""
        screenplay = """INT. ROOM - DAY

JOHN
This is a longer piece
of dialogue that spans
multiple lines.
"""
        self.parser.parse(screenplay)
        
        self.assertIn("JOHN", self.parser.characters)
        self.assertEqual(len(self.parser.characters["JOHN"].dialogue_lines), 3)
    
    def test_parse_character_with_extension(self):
        """Test parsing character names with extensions like (V.O.)"""
        screenplay = """INT. ROOM - DAY

JOHN (V.O.)
Can you hear me?

JANE (O.S.)
Yes, I can.
"""
        self.parser.parse(screenplay)
        
        # Extensions should be stripped
        self.assertIn("JOHN", self.parser.characters)
        self.assertIn("JANE", self.parser.characters)
    
    def test_parse_multiple_scenes(self):
        """Test parsing multiple scenes"""
        screenplay = """INT. ROOM - DAY

Action here.

EXT. STREET - NIGHT

More action.

INT. ANOTHER ROOM - DAY

Even more action.
"""
        self.parser.parse(screenplay)
        
        self.assertEqual(len(self.parser.scenes), 3)
        self.assertEqual(self.parser.scenes[0].heading, "INT. ROOM - DAY")
        self.assertEqual(self.parser.scenes[1].heading, "EXT. STREET - NIGHT")
        self.assertEqual(self.parser.scenes[2].heading, "INT. ANOTHER ROOM - DAY")
    
    def test_get_character_names(self):
        """Test getting list of character names"""
        screenplay = """INT. ROOM - DAY

ALICE
Hello.

BOB
Hi there.

ALICE
How are you?
"""
        self.parser.parse(screenplay)
        
        names = self.parser.get_character_names()
        self.assertIn("ALICE", names)
        self.assertIn("BOB", names)
        self.assertEqual(len(names), 2)
    
    def test_get_scene_headings(self):
        """Test getting list of scene headings"""
        screenplay = """INT. COFFEE SHOP - DAY

Action.

EXT. PARK - NIGHT

More action.
"""
        self.parser.parse(screenplay)
        
        headings = self.parser.get_scene_headings()
        self.assertEqual(len(headings), 2)
        self.assertIn("INT. COFFEE SHOP - DAY", headings)
        self.assertIn("EXT. PARK - NIGHT", headings)
    
    def test_character_total_words(self):
        """Test calculating total words for character"""
        screenplay = """INT. ROOM - DAY

JOHN
Hello world.

JOHN
This is a test.
"""
        self.parser.parse(screenplay)
        
        john = self.parser.characters["JOHN"]
        self.assertEqual(john.total_words, 6)  # "Hello world" (2) + "This is a test" (4)


if __name__ == '__main__':
    unittest.main()
