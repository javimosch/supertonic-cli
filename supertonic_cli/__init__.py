#!/usr/bin/env python3
"""supertonic-cli — On-device TTS from the command line using Supertonic."""

import argparse
import json
import sys
import time


def check_deps():
    try:
        from supertonic import TTS
        return TTS
    except ImportError:
        print("error: supertonic not installed. Run: pip install supertonic", file=sys.stderr)
        sys.exit(1)


def cmd_voices(args):
    TTS = check_deps()
    tts = TTS(auto_download=True)
    styles = tts.get_voice_styles() if hasattr(tts, "get_voice_styles") else []
    if not styles:
        styles = [tts.get_voice_style(v) for v in ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"] if v]
    if args.json:
        print(json.dumps([{"name": v.name if hasattr(v, "name") else str(v)} for v in styles], indent=2))
        return
    print("Available voices:")
    for v in styles:
        name = v.name if hasattr(v, "name") else str(v)
        lang = v.language if hasattr(v, "language") else "?"
        print(f"  {name} [{lang}]")


def cmd_languages(args):
    langs = {
        "en": "English", "ko": "Korean", "ja": "Japanese", "ar": "Arabic",
        "bg": "Bulgarian", "cs": "Czech", "da": "Danish", "de": "German",
        "el": "Greek", "es": "Spanish", "et": "Estonian", "fi": "Finnish",
        "fr": "French", "hi": "Hindi", "hr": "Croatian", "hu": "Hungarian",
        "id": "Indonesian", "it": "Italian", "lt": "Lithuanian", "lv": "Latvian",
        "nl": "Dutch", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian",
        "ru": "Russian", "sk": "Slovak", "sl": "Slovenian", "sv": "Swedish",
        "tr": "Turkish", "uk": "Ukrainian", "vi": "Vietnamese",
    }
    if args.json:
        print(json.dumps(langs, indent=2))
        return
    print("Supported languages (31):")
    for code, name in sorted(langs.items()):
        print(f"  {code} — {name}")


def save_wav(path, samples, samplerate=24000):
    import struct
    import numpy as np
    if hasattr(samples, "numpy"): samples = samples.numpy()
    if hasattr(samples, "cpu"): samples = samples.cpu()
    samples = np.asarray(samples)
    if samples.dtype != np.int16:
        samples = np.clip(samples * 32767, -32768, 32767).astype(np.int16)
    data = samples.tobytes()
    n = len(data)
    with open(path, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + n))
        f.write(b"WAVE")
        f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, samplerate, samplerate * 2, 2, 16))
        f.write(b"data")
        f.write(struct.pack("<I", n))
        f.write(data)

def cmd_synthesize(args):
    TTS = check_deps()
    tts = TTS(auto_download=True)
    style = tts.get_voice_style(voice_name=args.voice)
    start = time.time()
    wav, duration = tts.synthesize(args.text, voice_style=style, lang=args.lang)
    elapsed = time.time() - start
    try:
        tts.save_audio(wav, args.output)
    except ImportError:
        save_wav(args.output, wav)
    dur = float(duration)
    if args.json:
        print(json.dumps({"ok": True, "output": args.output, "duration_s": round(dur, 2), "real_time_s": round(elapsed, 2), "rtf": round(elapsed / max(dur, 0.001), 3), "voice": args.voice, "lang": args.lang}, indent=2))
    else:
        print(f"synthesized {dur:.2f}s of audio -> {args.output} ({elapsed:.2f}s real, RTF={elapsed/max(dur,0.001):.3f})")


def cmd_info(args):
    TTS = check_deps()
    tts = TTS(auto_download=True)
    info = {
        "engine": "supertonic",
        "version": getattr(tts, "version", "unknown"),
        "languages": 31,
        "model": "supertonic-3",
        "runtime": "ONNX",
        "auto_download": True,
    }
    if args.json:
        print(json.dumps(info, indent=2))
    else:
        for k, v in info.items():
            print(f"  {k}: {v}")


def main():
    p = argparse.ArgumentParser(prog="supertonic-cli", description="On-device TTS from the command line")
    p.add_argument("--json", action="store_true", help="JSON output")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("voices", help="List available voices")
    sp.add_argument("--json", action="store_true", dest="json", help="JSON output")
    sp.set_defaults(func=cmd_voices)

    sp = sub.add_parser("languages", help="List supported languages")
    sp.add_argument("--json", action="store_true", dest="json", help="JSON output")
    sp.set_defaults(func=cmd_languages)

    sp = sub.add_parser("synthesize", help="Synthesize speech from text")
    sp.add_argument("text", help="Text to synthesize")
    sp.add_argument("--voice", default="M1", help="Voice name (default: M1)")
    sp.add_argument("--lang", default="en", help="Language code (default: en)")
    sp.add_argument("-o", "--output", default="output.wav", help="Output WAV file path")
    sp.add_argument("--json", action="store_true", dest="json", help="JSON output")
    sp.set_defaults(func=cmd_synthesize)

    sp = sub.add_parser("info", help="Show engine info")
    sp.add_argument("--json", action="store_true", dest="json", help="JSON output")
    sp.set_defaults(func=cmd_info)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
