from utils import utils


def entry(ordered: list, plus_codes: list):

    level2_selected = [kode[:4] for kode in plus_codes]

    level2_matrix = utils.create_level2_matrix(ordered)

    level2_ordered = utils.order_level2_selected(level2_matrix, level2_selected)

    # impute intermediate boxes
    level2_ordered_imputed = utils.impute_intermediate_level2(
        level2_matrix, level2_ordered
    )

    return {
        (idx + 1): {"left_top": pc + "X2X2+X2", "right_button": pc + "2X2X+2X"}
        for idx, pc in enumerate(level2_ordered_imputed)
    }
