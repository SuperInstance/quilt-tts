# quilt-tts

> **Canon to speech.**
> The canon gate is a chord. This repo gives the chord a voice.

## TL;DR

```bash
export ELEVENLABS_TOKEN=...
python3 -c "from quilt_tts.core import speak_lore; print(speak_lore('Hello world'))"
```

## Quick start

```bash
export ELEVENLABS_TOKEN=...
PYTHONPATH=. python3 -m quilt_tts.core

# Or use a specific lore
python3 -c "from quilt_tts.core import speak_lore; speak_lore('A scar does not bar entry — it records that entry was already attempted.')"
```

## Architecture

```
lore → ElevenLabs API → MP3 file
       (33 voices available)
       (5KB max lore length per request)
```

## What this is

The canon gate is a chord. The chord can be heard silently (text-only)
or spoken aloud (via ElevenLabs). This repo gives the canon a voice.

## License

MIT — Casey / SuperInstance, Sept 23, 2026
