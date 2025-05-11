#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
youtube_transcript_to_romaji_json.py

Usage:
    pip install youtube-transcript-api pykakasi
    python youtube_transcript_to_romaji_json.py <YouTube URL or ID> [output.json]

指定動画の日本語字幕を取得し、ローマ字に変換して JSON ファイルに出力します。
"""

import sys
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi
import pykakasi

def extract_video_id(url_or_id: str) -> str:
    """YouTube URL または動画ID から 11文字の動画ID を抽出"""
    m = re.search(r'(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})', url_or_id)
    return m.group(1) if m else url_or_id

def fetch_transcript(video_id: str):
    """動画ID から日本語字幕を取得"""
    # languages に 'ja' を指定。ない場合は自動生成字幕を拾うこともあります。
    return YouTubeTranscriptApi.get_transcript(video_id, languages=['ja'])

def kana_to_romaji(text: str, kakasi_converter) -> str:
    """ひらがな・カタカナ・漢字混じりの日本語テキストをローマ字に変換"""
    return kakasi_converter.do(text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript_to_romaji_json.py <YouTube URL or ID> [output.json]")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else "transcript.json"

    video_id = extract_video_id(input_arg)
    try:
        entries = fetch_transcript(video_id)
    except Exception as e:
        print(f"[Error] 字幕取得に失敗しました: {e}")
        sys.exit(1)

    kakasi = pykakasi.kakasi()
    converter = kakasi.getConverter()

    result = []
    for entry in entries:
        start = entry.get("start", 0.0)
        duration = entry.get("duration", 0.0)
        text = entry.get("text", "").strip()
        if not text:
            continue
        romaji = kana_to_romaji(text, converter)
        result.append({
            "text": romaji,
            "start": round(start, 2),
            "duration": round(duration, 2)
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ '{output_file}' を生成しました（{len(result)} フレーズ）")

if __name__ == "__main__":
    main()
