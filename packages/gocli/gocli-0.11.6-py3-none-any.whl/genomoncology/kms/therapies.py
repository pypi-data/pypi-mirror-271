from cytoolz.curried import curry, unique, concat
from glom import Coalesce

from genomoncology.kms.match import (
    calls_to_alterations,
    transform_match_response,
)
from genomoncology.parse import DocType, __TYPE__
from genomoncology.parse.ensures import ensure_collection
import gosdk


@curry
def match_therapies(calls, diseases=None):
    diseases = ensure_collection(diseases or ["ANY"])

    alterations = calls_to_alterations(calls)

    response = gosdk.call_with_retry(
        gosdk.sdk.therapies.match_therapies_post,
        alterations=alterations,
        diseases=diseases,
    )

    return transform_match_response(response, DEFAULT_SPEC)


DEFAULT_SPEC = {
    __TYPE__: Coalesce(default=DocType.THERAPY.value),
    "drugs": "drugs",
    "response": "response",
    "other_condition": Coalesce("other_condition", default=None),
    "setting": "setting_source_pairs",
    "trigger_alterations": (
        "detected_alterations",
        ["trigger_alterations"],
        lambda x: list(unique(concat(x))),
    ),
    "trigger_diseases": (
        "matched_diseases",
        ["matched_disease"],
        lambda x: list(unique(x)),
    ),
}
