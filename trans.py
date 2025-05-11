from youtube_transcript_api import YouTubeTranscriptApi
import json

transcript = YouTubeTranscriptApi.get_transcript("SRi-fB_oprs", languages=["ja"])
with open("transcript.json", "w", encoding="utf-8") as f:
    json.dump(transcript, f, ensure_ascii=False, indent=2)
