import numpy as np
from numpy.typing import NDArray
import scipy.spatial


class MockedDelaunay(scipy.spatial.Delaunay):
    def __init__(
        self, points: NDArray[np.float32], simplices: NDArray[np.intc]
    ) -> None:
        self._points = points
        self.simplices = simplices


class MockedVoronoi(scipy.spatial.Delaunay):
    def __init__(
        self,
        points: NDArray[np.float32],
        vertices: NDArray[np.float32],
        ridge_points: NDArray[np.int32],
        ridge_vertices: list[list[int]],
        regions: list[list[int]],
        furthest_site: bool = False,
    ) -> None:
        self._points = points
        self.vertices = vertices
        self.ridge_points = ridge_points
        self.ridge_vertices = ridge_vertices
        self.regions = regions
        self.furthest_site = furthest_site
