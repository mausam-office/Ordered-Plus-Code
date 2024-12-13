import numpy as np
from utils.configs import ROWS, COLUMNS, LEVEL2_ROWS, LEVEL2_COLUMNS


def create_level1_matrix():
    return [[str(r) + str(c) for c in COLUMNS] for r in ROWS]


def order_level1_selected(selected, prefix_matrix):
    ordered = []
    numbered_order, count = {}, 0
    for idx_col in range(len(COLUMNS) - 1, -1, -1):
        for idx_row in range(len(ROWS) - 1, -1, -1):
            ele = prefix_matrix[idx_row][idx_col]
            if ele in selected:
                ordered.append(ele)
                count += 1
                numbered_order[ele] = count

    return ordered, numbered_order


def create_level2_matrix(ordered: list):
    first_unique_char = set()
    second_unique_char = set()

    for ele in ordered:
        if len(ele) != 2:
            raise Exception("The length of substring must be 2")

        first_unique_char.add(ele[0])
        second_unique_char.add(ele[1])

    num_selected_prefix_rows = len(first_unique_char)
    num_selected_prefix_cols = len(second_unique_char)

    matrix = [
        [f"{r}{c}" for c in COLUMNS if c in second_unique_char]
        for r in ROWS
        if r in first_unique_char
    ]

    placeholder_array = np.empty(
        (num_selected_prefix_rows * 20, num_selected_prefix_cols * 20), dtype=np.object_
    )

    for idx_row, row in enumerate(matrix):
        for idx_c, c in enumerate(row):
            if c not in ordered:
                continue
            level2_matrix = []
            for r_sec in LEVEL2_ROWS:
                level2_rows = []
                for c_sec in LEVEL2_COLUMNS:
                    level2_rows.append(f"{c}{r_sec}{c_sec}")
                level2_matrix.append(level2_rows)
            placeholder_array[
                idx_row * 20 : (idx_row + 1) * 20, idx_c * 20 : (idx_c + 1) * 20
            ] = level2_matrix

    placeholder_array = np.where(placeholder_array != None, placeholder_array, "")

    return placeholder_array


def order_level2_selected(level2_matrix: np.ndarray, level2_selected: list):
    r, c = level2_matrix.shape
    level2_ordered = []
    for idx_col in range(c - 1, -1, -1):
        for idx_row in range(r - 1, -1, -1):
            ele = level2_matrix[idx_row][idx_col]
            if ele in level2_selected:
                level2_ordered.append(ele)
    return level2_ordered


def impute_intermediate_level2(level2_matrix: np.ndarray, level2_ordered: list):
    level2_ordered_indices = {}
    for pc in level2_ordered:
        indices = np.where(level2_matrix == pc)
        if level2_ordered_indices.get(indices[1].item()):
            level2_ordered_indices[indices[1].item()].append(indices[0].item())
        else:
            level2_ordered_indices[indices[1].item()] = [indices[0].item()]

    max_min_rows = {}
    for k, v in level2_ordered_indices.items():
        max_min_rows[k] = {}
        max_min_rows[k]["max"] = max(v)
        max_min_rows[k]["min"] = min(v)

    for k, v in max_min_rows.items():
        level2_ordered_indices[k] = list(
            range(max_min_rows[k]["max"], max_min_rows[k]["min"] - 1, -1)
        )
    dim2_indices = list(level2_ordered_indices.keys())

    level2_ordered_imputed = []
    for pc in level2_ordered:
        indices = np.where(level2_matrix == pc)
        dim2_idx = indices[1].item()

        if dim2_idx in dim2_indices:
            for dim1_idx in level2_ordered_indices[dim2_idx]:
                level2_ordered_imputed.append(level2_matrix[dim1_idx, dim2_idx])
            dim2_indices.remove(dim2_idx)

    return level2_ordered_imputed


def get_larger_polygon_index(data):
    num_polygons = len(data["features"][0]["geometry"]["coordinates"])

    larger_polygon_idx = None
    max_points = 0
    for i in range(num_polygons):
        n_pts = len(data["features"][0]["geometry"]["coordinates"][i][0])
        if n_pts > max_points:
            larger_polygon_idx = i
            max_points = n_pts

    return larger_polygon_idx


def include_all_coordinates(data):
    num_polygons = len(data["features"][0]["geometry"]["coordinates"])
    all_coordinates = [[]]
    for i in range(num_polygons):
        all_coordinates[0].extend(data["features"][0]["geometry"]["coordinates"][i][0])
    return all_coordinates
