from utils import utils
import json


def entry(ordered: list, plus_codes: list):

    level2_selected = [kode[:4] for kode in plus_codes]

    level2_matrix = utils.create_level2_matrix(ordered)

    level2_ordered = utils.order_level2_selected(level2_matrix, level2_selected)

    # impute intermediate boxes
    level2_ordered_imputed = utils.impute_intermediate_level2(
        level2_matrix, level2_ordered
    )
    n_codes = len(str(len(level2_ordered_imputed)))

    return json.dumps(
        {
            f"{'0'*(n_codes - n_char) if (n_char:=len(str(idx+1))) else ''}{(idx + 1)}": pc
            for idx, pc in enumerate(level2_ordered_imputed)
        }
    )
