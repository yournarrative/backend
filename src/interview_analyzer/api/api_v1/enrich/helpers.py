import json
from collections import defaultdict
from typing import Dict, List

from starlette.datastructures import State

from interview_analyzer.api.api_v1.enrich.model import LabelledUtterance, EnrichedTranscript
from interview_analyzer.api.api_v1.shared.model import SimpleTranscript, SpeakerType
from interview_analyzer.utils.openai import get_completion
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def identify_and_assign_personas(transcript: SimpleTranscript, state: State):
    identified_personas = await _identify_personas(transcript, state)
    labelled_utterances = _assign_personas(transcript, identified_personas)
    return EnrichedTranscript(utterances=labelled_utterances)


async def _identify_personas(transcribed_text: SimpleTranscript, state: State) -> Dict[str, List[str]]:
    logger.debug(f"Identifying personas for {transcribed_text.utterances[:3]}")
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
    logger.debug(f"Identified personas response from OpenAI: {response}")
    return json.loads(response)


def _assign_personas(
        transcribed_text: SimpleTranscript,
        identified_personas: Dict[str, List[str]],
) -> List[LabelledUtterance]:
    logger.debug(f"Assigning personas {identified_personas}")
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
    logger.debug(f"Assigned personas into labelled utterances: {labelled_utterances[:4]}")
    return labelled_utterances
