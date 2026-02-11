import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import whisper
from pathlib import Path

audio_path = Path(__file__).parent / "audio" / "new.wav"

print("Loading Whisper large model (CPU)...")
model = whisper.load_model("large", device="cpu")

print("Transcribing audio...")

result = model.transcribe(str(audio_path), language="bg", task="transcribe", beam_size=1, temperature=0.0,
                          initial_prompt="Това е разговор на български език. Моля, транскрибирай внимателно думите.",
                          compression_ratio_threshold=2.2, logprob_threshold=-0.6, no_speech_threshold=0.5,
                          condition_on_previous_text=False, word_timestamps=False, fp16=False)

print("\n--- TRANSCRIPTION ---")
print(result["text"])

