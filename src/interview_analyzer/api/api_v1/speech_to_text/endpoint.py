from typing import List

from pyannote.audio import Pipeline
from pydantic import BaseModel
from starlette.datastructures import State
import whisper


class AudioInput(BaseModel):
    audio_bytes: str


class TranscribedTextSingle(BaseModel):
    text: str


async def speech_to_text_single(audio_input: AudioInput, state: State) -> TranscribedTextSingle:
    print("Loading audio...")
    ## Should be
    # audio = audio_input.audio_bytes
    ## But is this for testing
    audio = whisper.load_audio("resources/test-audio.m4a")
    audio = whisper.pad_or_trim(audio)

    print("Transcribing audio...")
    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(state.whisper_model.device)

    # detect the spoken language
    _, probs = state.whisper_model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(state.whisper_model, mel, options)

    transcribed_text = TranscribedTextSingle(text=result.text)
    return transcribed_text


class Speech(BaseModel):
    speaker: str
    text: str


class TranscribedTextMultiple(BaseModel):
    test_list: List[Speech]


def speech_to_text_multiple(audio_input: AudioInput, state: State) -> TranscribedTextMultiple:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=state.app_config["hugging_face"]["api_key"],
    )

    # send pipeline to GPU (when available)
    import torch
    pipeline.to(torch.device("cuda"))

    # apply pretrained pipeline
    diarization = pipeline("resources/test_audio.m4a")

    # print the result
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    # start=0.2s stop=1.5s speaker_0
    # start=1.8s stop=3.9s speaker_1
    # start=4.2s stop=5.7s speaker_0
    # ...
    return TranscribedTextMultiple()
