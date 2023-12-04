import json
import os
import random
from collections import defaultdict
from typing import List, Dict

import assemblyai as aai
from fastapi import UploadFile
from starlette.datastructures import State

from interview_analyzer.api.api_v1.speech_to_text.endpoint import TranscribedText, Utterance, SpeakerType, \
    LabelledUtterance, LabelledTranscribedText
from interview_analyzer.utils.llm import get_completion
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


def write_to_temp_file(file: UploadFile) -> str:
    filetype = file.filename.split(".")[-1]
    while True:
        new_file_name = random.randint(0, 9999999999999999)
        filename = f"audio/tempfiles/{new_file_name}.{filetype}"
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(file.file.read())
            logger.debug(f"Successfully wrote file to {filename}")
            return filename


def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
        logger.debug(f"Successfully removed file {filepath}")
    else:
        logger.warning(f"File {filepath} does not exist")


async def transcribe_audio_to_text_single_speaker(audio_file_path: str, state: State):
    transcribed_text = ""
    try:
        transcript = state.transcriber.transcribe(audio_file_path, config=aai.TranscriptionConfig())
    except Exception as e:
        logger.error(f"Failed to transcribe audio from file {audio_file_path}: {e}")
    else:
        transcribed_text = transcript.text
    finally:
        return TranscribedText(utterances=[Utterance(speaker=SpeakerType.DEFAULT.value, text=transcribed_text)])


async def transcribe_audio_to_text_multiple_speakers(audio_file_path: str, state: State):
    utterances: List[Utterance] = []
    try:
        transcript = state.transcriber.transcribe(audio_file_path, config=aai.TranscriptionConfig(speaker_labels=True))
    except Exception as e:
        logger.error(f"Failed to transcribe audio from file {audio_file_path}: {e}")
    else:
        for u in transcript.utterances:
            utterances.append(Utterance(speaker=u.speaker, text=u.text))
    finally:
        return TranscribedText(utterances=utterances)


def identify_and_assign_personas(transcribed_text: TranscribedText, state: State):
    identified_personas = identify_personas(transcribed_text, state)
    labelled_utterances = assign_personas(transcribed_text, identified_personas)
    return LabelledTranscribedText(labelled_utterances=labelled_utterances)


def identify_personas(transcribed_text: TranscribedText, state: State) -> Dict[str, List[str]]:
    speakers_to_utterances_map: Dict[str, List] = defaultdict(list)
    for utterance in transcribed_text.utterances:
        speakers_to_utterances_map[utterance.speaker].append(utterance.text[:50])

    prompt = "Given the following list of speakers and things " \
             "they've said in a job interview labelled \"Utterances\", " \
             "Identify which speakers are an \"interviewer\" or \"interviewee\". " \
             "Format your answer as a python dictionary with the format Dict[str, List[str]], " \
             "with one key \"interviewer\" and one key \"interviewee\"" \
             "and each speaker as an element of the value list. " \
             "Here is the list of speakers and utterance examples:"

    for speaker in speakers_to_utterances_map.keys():
        prompt += f"\n\nSpeaker: {speaker}\nUtterances: {speakers_to_utterances_map[speaker][:3]}"

    response = await get_completion(prompt, state)
    return json.loads(response)


def assign_personas(
        transcribed_text: TranscribedText,
        identified_personas: Dict[str, List[str]],
) -> List[LabelledUtterance]:
    reverse_map = {}
    for persona, speakers in identified_personas.items():
        for speaker in speakers:
            reverse_map[speaker.upper()] = persona.upper()

    labelled_utterances: List[LabelledUtterance] = []
    for utterance in transcribed_text.utterances:
        if utterance.speaker.upper() in reverse_map:
            speaker_type_string = reverse_map[utterance.speaker.upper()]
            for speaker_type in SpeakerType:
                if speaker_type.value.upper() == speaker_type_string:
                    labelled_utterances.append(
                        LabelledUtterance(
                            speaker=utterance.speaker,
                            speaker_type=speaker_type.value,
                            text=utterance.text
                        )
                    )

    return labelled_utterances
