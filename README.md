# supertonic-cli

On-device TTS from the command line. Super fast, 31 languages, no cloud.

Wraps [Supertone](https://github.com/supertone-inc/supertonic) (5.3k ⭐) — lightning-fast, on-device, multilingual TTS running natively via ONNX.

## Installation

```bash
pip install supertonic
pip install supertonic-cli
```

Or from source:

```bash
git clone https://github.com/javimosch/supertonic-cli.git
cd supertonic-cli
pip install -e .
```

## Usage

```bash
# List available voices
supertonic-cli voices

# List supported languages
supertonic-cli languages

# Synthesize speech
supertonic-cli synthesize "Hello, world!" --voice M1 --lang en -o hello.wav

# JSON output
supertonic-cli synthesize "Hello" --voice M1 --lang en --json

# Show engine info
supertonic-cli info
```

First run auto-downloads the ONNX model from Hugging Face (~300MB).

## Features

- **31 languages**: EN, KO, JA, AR, DE, FR, ES, IT, PT, RU, ZH, and more
- **10 voice styles**: M1-M5 (male), F1-F5 (female)
- **On-device**: No cloud, no API calls, no privacy concerns
- **Fast**: Real-time on CPU, ~99M parameter model
- **JSON output**: `--json` flag for automation

## License

MIT — Copyright (c) 2025 Javier Leandro Arancibia
