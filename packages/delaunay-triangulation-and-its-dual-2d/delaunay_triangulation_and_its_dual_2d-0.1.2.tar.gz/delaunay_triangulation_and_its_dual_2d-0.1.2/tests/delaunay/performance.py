import timeit

import matplotlib.pyplot as plt


POINT_COUNT_TEST_CASES = [100, 1000, 10000, 100000, 1000000]
NUM_REPEATS_PER_TEST_CASE = [16, 8, 4, 2, 1]
GENERATE_RANDOM_POINTS_SETUP_CODE = r"""
import numpy as np
import scipy.spatial

import delaunay_triangulation_and_its_dual_2d

rng = np.random.default_rng()
points = rng.uniform(low=0.0, high=1.0, size=({}, 2))
"""
DELAUNAY_CLASS_COMPUTE_VORONOI_TESSELLATION_STATEMENT = r"""
i = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
i.compute_voronoi_tessellation()
"""
SCIPY_SPATIAL_VORONOI_CLASS_COMPUTE_VORONOI_TESSELLATION_STATEMENT = (
    r"scipy.spatial.Voronoi(points=points)"
)

if __name__ == "__main__":
    delaunay_class_compute_voronoi_tessellation_time_results = []
    scipy_spatial_voronoi_class_compute_voronoi_tessellation_time_results = []
    for point_count, num_repeats in zip(
        POINT_COUNT_TEST_CASES, NUM_REPEATS_PER_TEST_CASE
    ):
        generate_random_points_setup_code = (
            GENERATE_RANDOM_POINTS_SETUP_CODE.format(point_count)
        )
        delaunay_class_compute_voronoi_tessellation_time = timeit.timeit(
            stmt=DELAUNAY_CLASS_COMPUTE_VORONOI_TESSELLATION_STATEMENT,
            setup=generate_random_points_setup_code,
            number=num_repeats,
        )
        delaunay_class_compute_voronoi_tessellation_time_results.append(
            delaunay_class_compute_voronoi_tessellation_time
        )
        scipy_spatial_voronoi_class_compute_voronoi_tessellation_time = timeit.timeit(
            stmt=SCIPY_SPATIAL_VORONOI_CLASS_COMPUTE_VORONOI_TESSELLATION_STATEMENT,
            setup=generate_random_points_setup_code,
            number=num_repeats,
        )
        scipy_spatial_voronoi_class_compute_voronoi_tessellation_time_results.append(
            scipy_spatial_voronoi_class_compute_voronoi_tessellation_time
        )

    plt.plot(
        POINT_COUNT_TEST_CASES,
        delaunay_class_compute_voronoi_tessellation_time_results,
        label="compute_voronoi_tessellation",
    )
    plt.plot(
        POINT_COUNT_TEST_CASES,
        scipy_spatial_voronoi_class_compute_voronoi_tessellation_time_results,
        label="scipy.spatial.Voronoi",
    )
    plt.xlabel("Num of Points")
    plt.ylabel("Time (s)")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Time to compute Voronoi tessellation")
    plt.legend()
    plt.grid()
    plt.show()
