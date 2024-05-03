from cytoolz.curried import curry

from genomoncology.cli.const import GRCH37
from genomoncology.kms.annotations import convert_to_csra, to_csra
from genomoncology.parse import (
    is_call_or_variant,
    DocType,
    __CHILD__,
    __TYPE__,
)
import gosdk


@curry
def get_variant_interpretations(
    data, template_name=None, delete_if_exists=False, build=GRCH37
):
    csra_batch = convert_to_csra(
        [{**d, "build": build} for d in data], add_build=False
    )

    variant_interpretations_response = (
        gosdk.call_with_retry(
            gosdk.sdk.variant_interpretations.generate_variant_interpretations,
            batch=csra_batch,
            template_names=[template_name],
            delete_if_exists=delete_if_exists,
            build=build,
        )
        if csra_batch
        else None
    )

    variant_interpretations_calls = []
    for call in data:
        variant_interpretations_calls.append(
            add_interpretations_to_calls(
                variant_interpretations_response, call
            )
        )

    return variant_interpretations_calls


def add_interpretations_to_calls(
    interpretations_response, call: dict
):
    if interpretations_response and is_call_or_variant(call):
        csra = to_csra(call, add_build=False)
        variant_interpretation_data = getattr(interpretations_response, csra, {})
        call["variant_interpretations"] = variant_interpretation_data.get(
            "variant_interpretations", []
        )
        call["protein_effects"] = variant_interpretation_data.get(
            "protein_effects", []
        )
        call["annotations"] = variant_interpretation_data.get(
            "annotations", {}
        )
        call[__TYPE__] = f"ANNOTATED_{call.get(__TYPE__, 'CALL')}"

    elif DocType.HEADER.is_a(call):
        call[__CHILD__] = f"ANNOTATED_{call.get(__CHILD__, 'CALL')}"

    return call
