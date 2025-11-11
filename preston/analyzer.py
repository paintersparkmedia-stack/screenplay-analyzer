"""Screenplay analyzer for generating insights and statistics"""

from typing import Dict, List, Tuple
from collections import Counter
from .parser import ScreenplayParser, Character, Scene


class ScreenplayAnalyzer:
    """Analyze screenplay for statistics and insights"""
    
    def __init__(self, parser: ScreenplayParser):
        self.parser = parser
    
    def get_character_statistics(self) -> Dict[str, Dict]:
        """Get statistics for each character"""
        stats = {}
        
        for name, character in self.parser.characters.items():
            stats[name] = {
                'name': name,
                'dialogue_lines': len(character.dialogue_lines),
                'total_words': character.total_words,
                'scenes': len(set(character.scene_appearances)),
                'scene_list': list(set(character.scene_appearances))
            }
        
        return stats
    
    def get_top_characters(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get top N characters by dialogue count"""
        char_counts = [
            (name, char.total_words) 
            for name, char in self.parser.characters.items()
        ]
        return sorted(char_counts, key=lambda x: x[1], reverse=True)[:n]
    
    def get_scene_count(self) -> int:
        """Get total number of scenes"""
        return len(self.parser.scenes)
    
    def get_dialogue_vs_action_ratio(self) -> Dict[str, int]:
        """Calculate ratio of dialogue to action lines"""
        dialogue_count = 0
        action_count = 0
        
        for element in self.parser.elements:
            if element.element_type == 'dialogue':
                dialogue_count += 1
            elif element.element_type == 'action':
                action_count += 1
        
        return {
            'dialogue_lines': dialogue_count,
            'action_lines': action_count,
            'total_lines': dialogue_count + action_count
        }
    
    def get_scenes_by_location(self) -> Dict[str, List[str]]:
        """Group scenes by INT/EXT"""
        int_scenes = []
        ext_scenes = []
        
        for scene in self.parser.scenes:
            heading = scene.heading.upper()
            if heading.startswith('INT'):
                int_scenes.append(scene.heading)
            elif heading.startswith('EXT'):
                ext_scenes.append(scene.heading)
        
        return {
            'interior': int_scenes,
            'exterior': ext_scenes,
            'int_count': len(int_scenes),
            'ext_count': len(ext_scenes)
        }
    
    def get_character_interactions(self) -> Dict[str, List[str]]:
        """Find which characters appear together in scenes"""
        interactions = {}
        
        for character_name in self.parser.characters.keys():
            interactions[character_name] = set()
        
        for scene in self.parser.scenes:
            characters_in_scene = list(set(scene.character_names))
            
            for char1 in characters_in_scene:
                for char2 in characters_in_scene:
                    if char1 != char2:
                        interactions[char1].add(char2)
        
        # Convert sets to sorted lists
        return {char: sorted(list(others)) for char, others in interactions.items()}
    
    def generate_report(self) -> str:
        """Generate a comprehensive analysis report"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("PRESTON SCREENPLAY ANALYSIS REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Scene statistics
        report_lines.append("SCENE STATISTICS")
        report_lines.append("-" * 60)
        scene_count = self.get_scene_count()
        report_lines.append(f"Total Scenes: {scene_count}")
        
        location_stats = self.get_scenes_by_location()
        report_lines.append(f"Interior Scenes: {location_stats['int_count']}")
        report_lines.append(f"Exterior Scenes: {location_stats['ext_count']}")
        report_lines.append("")
        
        # Character statistics
        report_lines.append("CHARACTER STATISTICS")
        report_lines.append("-" * 60)
        report_lines.append(f"Total Characters: {len(self.parser.characters)}")
        report_lines.append("")
        
        top_chars = self.get_top_characters(10)
        if top_chars:
            report_lines.append("Top Characters by Dialogue (word count):")
            for i, (name, word_count) in enumerate(top_chars, 1):
                char_stats = self.get_character_statistics()[name]
                report_lines.append(
                    f"  {i}. {name}: {word_count} words "
                    f"({char_stats['dialogue_lines']} lines, "
                    f"{char_stats['scenes']} scenes)"
                )
        report_lines.append("")
        
        # Dialogue vs Action
        report_lines.append("CONTENT BREAKDOWN")
        report_lines.append("-" * 60)
        ratio = self.get_dialogue_vs_action_ratio()
        total = ratio['total_lines']
        if total > 0:
            dialogue_pct = (ratio['dialogue_lines'] / total) * 100
            action_pct = (ratio['action_lines'] / total) * 100
            report_lines.append(f"Dialogue Lines: {ratio['dialogue_lines']} ({dialogue_pct:.1f}%)")
            report_lines.append(f"Action Lines: {ratio['action_lines']} ({action_pct:.1f}%)")
        report_lines.append("")
        
        # Character interactions
        report_lines.append("CHARACTER INTERACTIONS")
        report_lines.append("-" * 60)
        interactions = self.get_character_interactions()
        for char, others in sorted(interactions.items()):
            if others:
                report_lines.append(f"{char} appears with: {', '.join(others)}")
        report_lines.append("")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
