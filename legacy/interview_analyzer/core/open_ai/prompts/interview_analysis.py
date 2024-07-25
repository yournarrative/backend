interview_analysis_system_prompt: str = """
I am giving you an interview transcript that consists of a list of utterances. Please analyse it and determine the following information for each utterance in context of the interview.

You will receive a $500 tip if you fill out ALL of these fields properly:

1. "position" - The order in which the utterance was spoken. This should be a monotonically increasing integer starting with 0.
2. "speaker" - The name of the speaker as given
3. "speaker_type" - Which speaker is the \"interviewer\" and which speaker is the \"interviewee\". Label these as \"Interviewer\" and \"Interviewee\" respectively.
4. "text" - The text of the utterance.
5. "speech_type" - Which utterances are questions and which utterances are answers, and which utterances are
                    continuations of the current question/answer, and which utterances are irrelevant to the
                    interview entirely (such as a greeting, brief personal introduction, miscellaneous remark, or off
                    topic discussion). Label these as \"Question\", \"Answer\", \"Continuation\",
                    and \"Irrelevant\" respectively.
6. "question_type" - When a new question is identified, determine if it is a \"Behavioral\" question or
                    a \"Technical\" question. Label these as \"Behavioral\" and \"Technical\" respectively.
                    \"General\" and \"Open-Ended\" questions should be labelled as \"Behavioral\".
                    If it is not a new question, return the label \"None\" for the question type.
7. "question_number" - This is a monotonically increasing integer that represents the number of the question that
                    is being asked. This number should be incremented each time a new question is identified.
                    If it is not a new question, assign the number of the previous question. If it is a new
                    question, return the number of the new question.

Please return your answer as JSON that confirms to this schema.
"""
