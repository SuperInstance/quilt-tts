"""quilt-tts core — converts canon lore to speech via ElevenLabs."""

import os
import urllib.request
import json


def list_voices(api_key=None):
    """List available ElevenLabs voices."""
    api_key = api_key or os.environ.get("ELEVENLABS_TOKEN", "")
    if not api_key:
        return []
    url = "https://api.elevenlabs.io/v1/voices"
    req = urllib.request.Request(url, headers={"xi-api-key": api_key})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
            return [{"voice_id": v["voice_id"], "name": v["name"]} for v in data.get("voices", [])]
    except Exception as e:
        return [{"_error": str(e)}]


def speak_lore(lore_text, voice_id="21m00Tcm4TlvDq8ikWAM", output_path="lore.mp3", api_key=None):
    """Synthesize speech from canon lore. Returns the MP3 file path."""
    api_key = api_key or os.environ.get("ELEVENLABS_TOKEN", "")
    if not api_key:
        return {"_error": "ELEVENLABS_TOKEN not set"}
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    body = {
        "text": lore_text[:5000],  # ~5KB max for free tier
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            mp3_data = resp.read()
            with open(output_path, "wb") as f:
                f.write(mp3_data)
            return {
                "path": output_path,
                "size_bytes": len(mp3_data),
                "voice_id": voice_id,
                "lore_chars": len(lore_text),
            }
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.read().decode()[:200]}"}
    except Exception as e:
        return {"_error": str(e)}


def main():
    """CLI: list voices + speak a default lore."""
    import sys
    print("=== quilt-tts ===")
    print(f"Listing voices...")
    voices = list_voices()
    if voices and "_error" not in voices[0]:
        print(f"Found {len(voices)} voices:")
        for v in voices[:5]:
            print(f"  - {v.get('name', '?')} ({v.get('voice_id', '?')[:8]}...)")
    else:
        print(f"Could not list voices: {voices}")
        return

    if len(sys.argv) > 1:
        lore = " ".join(sys.argv[1:])
    else:
        lore = "A scar does not bar entry — it records that entry was already attempted. The substrate walks itself."

    print(f"\nSpeaking: {lore[:80]}...")
    result = speak_lore(lore)
    if "_error" in result:
        print(f"Error: {result['_error']}")
    else:
        print(f"OK: {result['size_bytes']} bytes at {result['path']}")


if __name__ == "__main__":
    main()
