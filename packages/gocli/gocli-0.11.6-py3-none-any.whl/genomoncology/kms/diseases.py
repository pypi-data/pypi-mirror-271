from cytoolz.curried import curry

from genomoncology.pipeline.converters import obj_to_dict
import gosdk


@curry
def get_disease_by_oncotree_code(
        oncotree_code=None,
        fields=("is_solid", "is_heme")):
    response = gosdk.call_with_retry(
        gosdk.sdk.diseases.get_diseases,
        oncotree_code=oncotree_code,
        fields=fields
    )
    return obj_to_dict(None, response)
