"""Predeclared stronger inference prompt; original training inputs stay frozen."""

from .contracts import GeneratedStory, canonical, messages_for

SCHEMA_PROMPT_VERSION = "evidence-editor-v2-explicit-schema-v1"
SERVING_PROMPT_VERSION = "evidence-editor-v2-local-serving-v1"


def schema_messages_for(inputs):
    messages = messages_for(inputs)
    messages[0]["content"] += (
        " Use these exact JSON property names and types, including the numeric claim property named value. "
        "Output schema: " + canonical(GeneratedStory.model_json_schema())
    )
    return messages


def serving_messages_for(inputs):
    messages = schema_messages_for(inputs)
    messages[0]["content"] += (
        " Repeat only numeric values explicitly present in the supplied evidence or timing. "
        "Do not calculate new segment distances, durations, conversions, or other quantities. "
        "For the requested signal, report the supplied structured fact."
    )
    return messages
