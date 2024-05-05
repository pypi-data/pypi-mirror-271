import cProfile
import pstats

import numpy as np

import delaunay_triangulation_and_its_dual_2d


rng = np.random.default_rng()
points = rng.uniform(low=0.0, high=1.0, size=20000).reshape(-1, 2)
i = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
with cProfile.Profile() as profiler:
    i.compute_voronoi_tessellation()
    profiler_stat = pstats.Stats(profiler).sort_stats(
        pstats.SortKey.CUMULATIVE
    )
    profiler_stat.print_stats()
