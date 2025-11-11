"""Command-line interface for Preston screenplay analyzer"""

import sys
import argparse
from pathlib import Path
from .parser import ScreenplayParser
from .analyzer import ScreenplayAnalyzer


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Preston - Screenplay Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  preston analyze script.fountain
  preston analyze script.txt
  preston stats script.fountain
  preston characters script.fountain
        """
    )
    
    parser.add_argument(
        'command',
        choices=['analyze', 'stats', 'characters', 'scenes'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'screenplay_file',
        type=str,
        help='Path to screenplay file (Fountain format or plain text)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output file for report (default: print to stdout)'
    )
    
    args = parser.parse_args()
    
    # Read screenplay file
    screenplay_path = Path(args.screenplay_file)
    if not screenplay_path.exists():
        print(f"Error: File '{args.screenplay_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(screenplay_path, 'r', encoding='utf-8') as f:
            screenplay_text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse screenplay
    screenplay_parser = ScreenplayParser()
    screenplay_parser.parse(screenplay_text)
    
    # Create analyzer
    analyzer = ScreenplayAnalyzer(screenplay_parser)
    
    # Execute command
    output = ""
    
    if args.command == 'analyze':
        output = analyzer.generate_report()
    
    elif args.command == 'stats':
        output = generate_stats_report(analyzer)
    
    elif args.command == 'characters':
        output = generate_character_report(analyzer)
    
    elif args.command == 'scenes':
        output = generate_scene_report(analyzer)
    
    # Output result
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Report saved to {args.output}")
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


def generate_stats_report(analyzer: ScreenplayAnalyzer) -> str:
    """Generate quick statistics report"""
    lines = []
    lines.append("SCREENPLAY STATISTICS")
    lines.append("=" * 60)
    lines.append(f"Total Scenes: {analyzer.get_scene_count()}")
    lines.append(f"Total Characters: {len(analyzer.parser.characters)}")
    
    ratio = analyzer.get_dialogue_vs_action_ratio()
    lines.append(f"Dialogue Lines: {ratio['dialogue_lines']}")
    lines.append(f"Action Lines: {ratio['action_lines']}")
    
    location_stats = analyzer.get_scenes_by_location()
    lines.append(f"Interior Scenes: {location_stats['int_count']}")
    lines.append(f"Exterior Scenes: {location_stats['ext_count']}")
    
    return "\n".join(lines)


def generate_character_report(analyzer: ScreenplayAnalyzer) -> str:
    """Generate character-focused report"""
    lines = []
    lines.append("CHARACTER REPORT")
    lines.append("=" * 60)
    
    char_stats = analyzer.get_character_statistics()
    
    # Sort by total words
    sorted_chars = sorted(
        char_stats.items(),
        key=lambda x: x[1]['total_words'],
        reverse=True
    )
    
    for name, stats in sorted_chars:
        lines.append(f"\n{name}")
        lines.append("-" * 40)
        lines.append(f"  Dialogue Lines: {stats['dialogue_lines']}")
        lines.append(f"  Total Words: {stats['total_words']}")
        lines.append(f"  Scenes: {stats['scenes']}")
    
    return "\n".join(lines)


def generate_scene_report(analyzer: ScreenplayAnalyzer) -> str:
    """Generate scene-focused report"""
    lines = []
    lines.append("SCENE REPORT")
    lines.append("=" * 60)
    
    for i, scene in enumerate(analyzer.parser.scenes, 1):
        lines.append(f"\nScene {i}: {scene.heading}")
        lines.append(f"  Line: {scene.line_number}")
        
        char_names = list(set(scene.character_names))
        if char_names:
            lines.append(f"  Characters: {', '.join(sorted(char_names))}")
        
        # Count element types in scene
        dialogue_count = sum(1 for e in scene.elements if e.element_type == 'dialogue')
        action_count = sum(1 for e in scene.elements if e.element_type == 'action')
        lines.append(f"  Dialogue Lines: {dialogue_count}")
        lines.append(f"  Action Lines: {action_count}")
    
    return "\n".join(lines)


if __name__ == '__main__':
    main()
