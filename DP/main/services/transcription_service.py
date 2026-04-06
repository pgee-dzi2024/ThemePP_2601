from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List

import whisper

FFMPEG_DIR = Path(__file__).resolve().parent.parent / "test" / "ffmpeg" / "bin"


def ensure_ffmpeg_available() -> None:
    if FFMPEG_DIR.exists():
        os.environ["PATH"] = str(FFMPEG_DIR) + os.pathsep + os.environ.get("PATH", "")

    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            f"ffmpeg не е намерен в PATH. Потърсен е и в локалната папка: {FFMPEG_DIR}"
        )


def load_whisper_model():
    ensure_ffmpeg_available()
    return whisper.load_model("large", device="cpu")


def format_srt_timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{ms:03}"


def build_srt(segments: List[Dict[str, Any]]) -> str:
    lines: list[str] = []
    for index, segment in enumerate(segments, start=1):
        start = format_srt_timestamp(float(segment["start"]))
        end = format_srt_timestamp(float(segment["end"]))
        text = str(segment["text"]).strip()
        lines.append(f"{index}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines).strip() + "\n"


def build_txt(segments: List[Dict[str, Any]]) -> str:
    return "\n".join(str(segment["text"]).strip() for segment in segments).strip() + "\n"


def transcribe_media_file(file_path: Path) -> Dict[str, Any]:
    model = load_whisper_model()

    result = model.transcribe(
        str(file_path),
        language="bg",
        task="transcribe",
        beam_size=1,
        temperature=0.0,
        initial_prompt="Това е разговор на български език. Моля, транскрибирай внимателно думите.",
        compression_ratio_threshold=2.2,
        logprob_threshold=-0.6,
        no_speech_threshold=0.5,
        condition_on_previous_text=False,
        word_timestamps=False,
        fp16=False,
    )

    segments = result.get("segments", [])
    text = str(result.get("text", "")).strip()
    srt = build_srt(segments)
    txt = build_txt(segments)

    return {
        "text": text,
        "srt": srt,
        "txt": txt,
    }