import warnings
import os
from pathlib import Path
import shutil

warnings.filterwarnings("ignore", category=UserWarning)

import whisper


def main() -> int:
    audio_path = Path(__file__).parent / "audio" / "new.wav"
    ffmpeg_dir = Path(__file__).parent / "ffmpeg" / "bin"

    if not audio_path.exists():
        print(f"Грешка: аудиофайлът не е намерен: {audio_path}")
        return 1

    if not ffmpeg_dir.exists():
        print(f"Грешка: папката с ffmpeg не е намерена: {ffmpeg_dir}")
        return 1

    os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ.get("PATH", "")

    if shutil.which("ffmpeg") is None:
        print("Грешка: ffmpeg пак не е открит, провери дали ffmpeg.exe е вътре в папката bin.")
        return 1

    print("Зареждане на Whisper large model (CPU)...")
    model = whisper.load_model("large", device="cpu")

    print("Транскрибиране на аудио...")
    result = model.transcribe(
        str(audio_path),
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

    print("\n--- TRANSCRIPTION ---")
    print(result["text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

