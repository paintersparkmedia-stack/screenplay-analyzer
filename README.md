# Preston - Screenplay Analyzer

Preston is a screenwriting program that analyzes screenplays written in Fountain format (or plain text screenplay format). It provides detailed statistics about characters, scenes, dialogue, and story structure.

## Features

- Parse screenplays in Fountain format
- Analyze character dialogue and screen time
- Track scene structure (INT/EXT, location, etc.)
- Calculate dialogue vs. action ratios
- Identify character interactions
- Generate comprehensive analysis reports

## Installation

```bash
pip install -e .
```

## Usage

Preston provides a command-line interface with several commands:

### Analyze (Full Report)

Generate a comprehensive analysis report:

```bash
preston analyze screenplay.fountain
```

### Statistics

Get quick statistics:

```bash
preston stats screenplay.fountain
```

### Character Report

Get detailed character information:

```bash
preston characters screenplay.fountain
```

### Scene Report

Get scene-by-scene breakdown:

```bash
preston scenes screenplay.fountain
```

### Save to File

All commands support saving output to a file:

```bash
preston analyze screenplay.fountain -o report.txt
```

## Example

An example screenplay is provided in `examples/sample_screenplay.fountain`.

Try it:

```bash
preston analyze examples/sample_screenplay.fountain
```

## Screenplay Format

Preston supports Fountain format, which is a plain-text screenplay format. Basic elements:

- **Scene Headings**: Start with INT., EXT., INT/EXT, or EXT/INT
- **Character Names**: ALL CAPS on their own line
- **Dialogue**: Text following a character name
- **Action**: Regular text describing action or scene description
- **Parentheticals**: Text in (parentheses) within dialogue

Example:

```
INT. COFFEE SHOP - DAY

SARAH enters and looks around.

SARAH
Is anyone here?

MIKE (O.S.)
Over here!
```

## Development

Run tests:

```bash
python -m unittest discover tests
```

## License

MIT License
