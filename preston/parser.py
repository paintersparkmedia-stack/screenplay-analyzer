"""Screenplay parser for Fountain format"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ScreenplayElement:
    """Represents a screenplay element"""
    element_type: str
    content: str
    line_number: int
    raw_text: str = ""


@dataclass
class Character:
    """Represents a character in the screenplay"""
    name: str
    dialogue_lines: List[str] = field(default_factory=list)
    scene_appearances: List[str] = field(default_factory=list)
    
    @property
    def total_words(self) -> int:
        """Calculate total words spoken by this character"""
        return sum(len(line.split()) for line in self.dialogue_lines)


@dataclass
class Scene:
    """Represents a scene in the screenplay"""
    heading: str
    elements: List[ScreenplayElement] = field(default_factory=list)
    line_number: int = 0
    
    @property
    def character_names(self) -> List[str]:
        """Get all character names in this scene"""
        return [elem.content for elem in self.elements if elem.element_type == "character"]


class ScreenplayParser:
    """Parse screenplays in Fountain format"""
    
    def __init__(self):
        self.elements: List[ScreenplayElement] = []
        self.scenes: List[Scene] = []
        self.characters: Dict[str, Character] = {}
        
    def parse(self, text: str) -> None:
        """Parse screenplay text"""
        lines = text.split('\n')
        current_scene = None
        current_character = None
        line_num = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            line_num = i + 1
            
            # Skip empty lines
            if not line.strip():
                i += 1
                continue
            
            # Scene heading (INT. or EXT. at start of line)
            if self._is_scene_heading(line):
                scene = Scene(heading=line.strip(), line_number=line_num)
                self.scenes.append(scene)
                current_scene = scene
                element = ScreenplayElement("scene", line.strip(), line_num, line)
                self.elements.append(element)
                if current_scene:
                    current_scene.elements.append(element)
            
            # Character name (all caps, centered-ish)
            elif self._is_character_name(line):
                char_name = self._clean_character_name(line.strip())
                current_character = char_name
                
                if char_name not in self.characters:
                    self.characters[char_name] = Character(name=char_name)
                
                element = ScreenplayElement("character", char_name, line_num, line)
                self.elements.append(element)
                if current_scene:
                    self.characters[char_name].scene_appearances.append(current_scene.heading)
                    current_scene.elements.append(element)
            
            # Dialogue (comes after character name)
            elif current_character and line.strip() and not self._is_scene_heading(line):
                dialogue = line.strip()
                
                # Handle parenthetical
                if dialogue.startswith('(') and dialogue.endswith(')'):
                    element = ScreenplayElement("parenthetical", dialogue, line_num, line)
                else:
                    element = ScreenplayElement("dialogue", dialogue, line_num, line)
                    self.characters[current_character].dialogue_lines.append(dialogue)
                
                self.elements.append(element)
                if current_scene:
                    current_scene.elements.append(element)
                
                # Continue dialogue until we hit an empty line
                i += 1
                while i < len(lines) and lines[i].strip():
                    dialogue_line = lines[i].strip()
                    line_num = i + 1
                    
                    if self._is_character_name(lines[i]) or self._is_scene_heading(lines[i]):
                        i -= 1
                        break
                    
                    if dialogue_line.startswith('(') and dialogue_line.endswith(')'):
                        element = ScreenplayElement("parenthetical", dialogue_line, line_num, lines[i])
                    else:
                        element = ScreenplayElement("dialogue", dialogue_line, line_num, lines[i])
                        self.characters[current_character].dialogue_lines.append(dialogue_line)
                    
                    self.elements.append(element)
                    if current_scene:
                        current_scene.elements.append(element)
                    i += 1
                
                current_character = None
            
            # Action/description
            else:
                if line.strip():
                    element = ScreenplayElement("action", line.strip(), line_num, line)
                    self.elements.append(element)
                    if current_scene:
                        current_scene.elements.append(element)
                current_character = None
            
            i += 1
    
    def _is_scene_heading(self, line: str) -> bool:
        """Check if line is a scene heading"""
        line = line.strip().upper()
        return (line.startswith('INT.') or 
                line.startswith('EXT.') or 
                line.startswith('INT/EXT') or
                line.startswith('EXT/INT'))
    
    def _is_character_name(self, line: str) -> bool:
        """Check if line is a character name (all caps, no leading whitespace for action)"""
        stripped = line.strip()
        if not stripped:
            return False
        
        # Must be all uppercase (allowing for parentheticals like (O.S.) or (V.O.))
        base_name = re.sub(r'\s*\([^)]*\)\s*$', '', stripped)
        if not base_name:
            return False
        
        # Exclude common screenplay elements that are all caps
        excluded_elements = ['FADE IN:', 'FADE OUT.', 'FADE TO:', 'CUT TO:', 
                           'DISSOLVE TO:', 'THE END', 'END', 'CONTINUED:']
        if base_name in excluded_elements:
            return False
        
        # Must be uppercase letters, spaces, and common punctuation
        if not re.match(r'^[A-Z][A-Z\s\.\'\-]+$', base_name):
            return False
        
        # Should be reasonably short (character names are typically short)
        if len(base_name) > 50:
            return False
        
        # Not a scene heading
        if self._is_scene_heading(line):
            return False
        
        return True
    
    def _clean_character_name(self, name: str) -> str:
        """Clean character name by removing extensions like (V.O.) or (O.S.)"""
        # Remove parenthetical extensions
        cleaned = re.sub(r'\s*\([^)]*\)\s*$', '', name)
        return cleaned.strip()
    
    def get_character_names(self) -> List[str]:
        """Get list of all character names"""
        return list(self.characters.keys())
    
    def get_scene_headings(self) -> List[str]:
        """Get list of all scene headings"""
        return [scene.heading for scene in self.scenes]
