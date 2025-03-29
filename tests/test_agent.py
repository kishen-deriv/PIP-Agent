#!/usr/bin/env python3
"""
Test script for the Leo.
This script allows testing Leo without running it.
"""

import os
import sys
from pathlib import Path
import argparse
from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agent import Leo
from prompts.output_format import pip_output_format

# Load environment variables
load_dotenv()

def main():
    """Main function to test Leo."""
    parser = argparse.ArgumentParser(description='Test Leo')
    parser.add_argument('--input', '-i', type=str, help='Path to input file containing PIP details')
    parser.add_argument('--output', '-o', type=str, default='output/test_pip_document.txt',
                        help='Path to output file for the generated PIP document')
    parser.add_argument('--method', '-m', type=str, choices=['pipeline', 'simple'],
                        default='pipeline', help='Generation method to use')
    args = parser.parse_args()

    # Initialize the PIP generator
    generator = Leo()

    # Get input from file or stdin
    if args.input:
        with open(args.input, 'r') as f:
            pip_input = f.read()
    else:
        print("Enter PIP details (press Ctrl+D when finished):")
        pip_input = ""
        try:
            while True:
                line = input()
                pip_input += line + "\n"
        except EOFError:
            pass

    # Generate the PIP document
    use_pipeline = args.method == 'pipeline'
    print(f"Generating PIP document using {args.method} approach...")
    pip_document = generator.generate_pip(
        pip_input_form=pip_input,
        pip_output_format=pip_output_format,
        use_pipeline=use_pipeline
    )

    # Save the document
    generator.save_pip(pip_document, args.output)
    print(f"PIP document generated and saved to {args.output}")

    # Print a preview
    preview_length = min(500, len(pip_document))
    print("\nPreview of generated document:")
    print("-" * 80)
    print(pip_document[:preview_length] + ("..." if len(pip_document) > preview_length else ""))
    print("-" * 80)

if __name__ == "__main__":
    main()
