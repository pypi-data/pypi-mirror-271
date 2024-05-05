import numpy as np
from numpy.typing import NDArray
import pytest
import scipy
import scipy.spatial

import delaunay_triangulation_and_its_dual_2d
import delaunay_triangulation_and_its_dual_2d.exceptions


def _sort_rows(array: NDArray) -> NDArray:
    return array[np.lexsort(array.T[::-1])]


def _sort_columns_of_each_row_then_sort_rows(array: NDArray) -> NDArray:
    array_columns_sorted = np.sort(array, axis=1)
    return _sort_rows(array=array_columns_sorted)


def _process_num_list_representing_a_polygon_for_equality_check(
    list_: list,
) -> list:
    if len(list_) == 1:
        return list_
    min_index = list_.index(min(list_))
    result = list_[min_index:] + list_[:min_index]
    if result[1] > result[-1]:
        result = [result[0]] + result[1:][::-1]
    return result


@pytest.mark.parametrize(
    "num_of_points, dimensions_of_points, result",
    [
        (100, 2, True),
        (3, 2, True),
        (3, 3, False),
        (3, 1, False),
        (2, 2, False),
        (1, 2, False),
    ],
)
def test_check_points_validity_method(
    num_of_points: int, dimensions_of_points: int, result: bool
):
    points = np.zeros((num_of_points, dimensions_of_points), dtype=np.float32)
    assert (
        delaunay_triangulation_and_its_dual_2d.Delaunay._check_points_validity(
            points=points
        )
        is result
    )


@pytest.mark.parametrize(
    "value",
    [
        -1.0,
        0.0,
        1.0,
        100000.0,
    ],
)
def test_duplicated_points_exist(value: float):
    identical_points = np.full((3, 2), fill_value=value, dtype=np.float32)
    assert (
        delaunay_triangulation_and_its_dual_2d.Delaunay._duplicated_points_exist(
            points=identical_points
        )
        is True
    )
    random_points = np.random.rand(3, 2)
    assert (
        delaunay_triangulation_and_its_dual_2d.Delaunay._duplicated_points_exist(
            points=random_points
        )
        is False
    )
    mixed_points = np.concatenate(
        [identical_points, random_points], axis=0, dtype=np.float32
    )
    assert (
        delaunay_triangulation_and_its_dual_2d.Delaunay._duplicated_points_exist(
            points=mixed_points
        )
        is True
    )


@pytest.mark.parametrize(
    "num_of_points",
    [
        3,
        4,
        100000,
    ],
)
def test_jitter_points_on_overlap(num_of_points: int):
    num_of_points_0 = num_of_points // 2
    num_of_points_1 = num_of_points - num_of_points_0
    points = np.concatenate(
        [np.zeros((num_of_points_0, 2)), np.ones((num_of_points_1, 2))],
        axis=0,
        dtype=np.float32,
    )
    points = delaunay_triangulation_and_its_dual_2d.Delaunay._jitter_points_on_overlap(
        points=points, rng=np.random.default_rng()
    )


@pytest.mark.parametrize(
    "num_of_points, num_of_iterations",
    [
        (3, 1),
        (3, 1000),
        (4, 1),
        (4, 1000),
        (100000, 1),
    ],
)
def test_voronoi_iteration(num_of_points: int, num_of_iterations: int):
    points = np.random.uniform(low=0.0, high=100.0, size=(num_of_points, 2))
    for _ in range(num_of_iterations):
        points = (
            delaunay_triangulation_and_its_dual_2d.Delaunay.voronoi_iteration(
                points=points, rng=np.random.default_rng()
            )
        )


def test_compute_voronoi_diagram():
    good_points_found = False
    for _ in range(1000):
        points = np.random.uniform(low=0.0, high=100.0, size=(100, 2))
        delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(
            points=points
        )
        try:
            delaunay.compute_voronoi_tessellation()
        except (
            delaunay_triangulation_and_its_dual_2d.DuplicatedCircumcentersError
        ) as e:
            print(str(e))
        else:
            good_points_found = True
            break
    if not good_points_found:
        raise ValueError("Cannot find good points in reasonable iterations")

    expected_outputs = scipy.spatial.Voronoi(points=points)
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
    assert delaunay.voronoi_vertices.dtype == expected_outputs.vertices.dtype
    assert np.allclose(
        _sort_rows(array=delaunay.voronoi_vertices),
        _sort_rows(array=expected_outputs.vertices),
        atol=1e-6,
    )
    assert delaunay.ridge_points.dtype == expected_outputs.ridge_points.dtype
    assert np.array_equal(
        _sort_columns_of_each_row_then_sort_rows(array=delaunay.ridge_points),
        _sort_columns_of_each_row_then_sort_rows(
            array=expected_outputs.ridge_points
        ),
    )
    delaunay_ridge_vertices = np.array(delaunay.ridge_vertices, dtype=np.intc)
    expected_outputs_ridge_vertices = np.array(
        expected_outputs.ridge_vertices, dtype=np.intc
    )
    assert np.array_equal(
        _sort_columns_of_each_row_then_sort_rows(
            array=delaunay_ridge_vertices
        ),
        _sort_columns_of_each_row_then_sort_rows(
            array=expected_outputs_ridge_vertices
        ),
    )
    delaunay_regions = [
        _process_num_list_representing_a_polygon_for_equality_check(list_=r)
        for r in delaunay.regions
    ]
    delaunay_regions.sort(key=lambda x: tuple(x))
    expected_outputs_regions = [
        _process_num_list_representing_a_polygon_for_equality_check(list_=r)
        for r in expected_outputs.regions
        if len(r)
    ]
    expected_outputs_regions.sort(key=lambda x: tuple(x))
    assert delaunay_regions == expected_outputs_regions


def test_compute_voronoi_diagram_raises_duplicated_circumcenters_error():
    points = np.array(
        [[0, 0], [1, 0], [1, 1], [0, 1]],
        dtype=np.float32,
    )
    delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
    with pytest.raises(
        delaunay_triangulation_and_its_dual_2d.exceptions.DuplicatedCircumcentersError
    ):
        delaunay.compute_voronoi_tessellation()
