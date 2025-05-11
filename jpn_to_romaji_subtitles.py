#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
jpn_to_romaji_subtitles.py

Usage:
    pip install pykakasi
    python jpn_to_romaji_subtitles.py <input_json> <output_json>

Description:
    指定した日本語字幕JSONファイルを読み込み、
    textフィールドをすべてローマ字に変換して新たなJSONを出力します。

Input JSON format (example):
[
  { "text": "こんにちは", "start": 1.0, "duration": 2.0 },
  { "text": "世界", "start": 4.0, "duration": 2.0 }
]

Output JSON format:
[
  { "text": "konnichiwa", "start": 1.0, "duration": 2.0 },
  { "text": "sekai", "start": 4.0, "duration": 2.0 }
]
"""

import sys
import json
from pykakasi import kakasi

def convert_to_romaji(input_file, output_file):
    # Read input JSON
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # Set up kakasi converter
    kakasi_inst = kakasi()
    kakasi_inst.setMode("J", "a")  # Japanese to ascii (romaji)
    kakasi_inst.setMode("H", "a")  # Hiragana to ascii
    kakasi_inst.setMode("K", "a")  # Katakana to ascii
    converter = kakasi_inst.getConverter()

    # Process each entry
    output = []
    for entry in data:
        text = entry.get("text", "")
        start = entry.get("start", 0.0)
        duration = entry.get("duration", 0.0)
        if not isinstance(text, str):
            continue
        romaji = converter.do(text).strip()
        output.append({
            "text": romaji,
            "start": start,
            "duration": duration
        })

    # Write output JSON
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print(f"Successfully wrote {len(output)} entries to '{output_file}'")

def main():
    if len(sys.argv) != 3:
        print("Usage: python jpn_to_romaji_subtitles.py <input_json> <output_json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_to_romaji(input_file, output_file)

if __name__ == "__main__":
    main()
