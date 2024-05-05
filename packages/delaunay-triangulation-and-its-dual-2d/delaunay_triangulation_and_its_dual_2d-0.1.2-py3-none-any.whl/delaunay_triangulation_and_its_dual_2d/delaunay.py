from abc import ABC, abstractmethod
from collections import defaultdict, deque
import logging

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import scipy
from scipy.spatial import voronoi_plot_2d

from . import exceptions, util
from .geometry import BoundingBox2d, CentroidHelper, CircumcircleHelper


logger = logging.getLogger(__name__)


class Base(ABC):
    def __init__(self, *, points: NDArray[np.float_]) -> None:
        """

        Args:
            points:
                A collection of "n" 2D points arranged in the Cartesian
                coordinate system with the axis order (x, y) and having a shape
                of (n, 2).
        """
        assert self._check_points_validity(points=points)

        self._points: NDArray[np.float_] = points
        self._delaunay_triangulation_computed: bool = False
        self._ridges_and_regions_computed: bool = False
        self._voronoi_tessellation_computed: bool = False
        self._barycentric_dual_computed: bool = False

        self._bounding_box: BoundingBox2d = self._compute_bounding_box(
            points=points
        )

        self._triangles: NDArray[np.intc]
        self._ridge_points: NDArray[np.int32]
        self._ridge_vertices: list[list[int]]
        self._regions: list[list[int]]
        self._voronoi_vertices: NDArray[np.float_]
        self._barycentric_dual_vertices: NDArray[np.float_]

    @property
    def points(self) -> NDArray[np.float_]:
        return self._points

    @property
    def bounding_box(self) -> BoundingBox2d:
        return self._bounding_box

    @property
    def triangles(self) -> NDArray[np.intc]:
        self.compute_delaunay_triangulation()
        return self._triangles

    @property
    def ridge_points(self) -> NDArray[np.int32]:
        self._compute_ridges_and_regions()
        return self._ridge_points

    @property
    def ridge_vertices(self) -> list[list[int]]:
        self._compute_ridges_and_regions()
        return self._ridge_vertices

    @property
    def regions(self) -> list[list[int]]:
        self._compute_ridges_and_regions()
        return self._regions

    @property
    def voronoi_vertices(self) -> NDArray[np.float_]:
        self.compute_voronoi_tessellation()
        return self._voronoi_vertices

    @property
    def barycentric_dual_vertices(self) -> NDArray[np.float_]:
        self.compute_barycentric_dual()
        return self._barycentric_dual_vertices

    @staticmethod
    def _check_points_validity(points: NDArray[np.float_]) -> bool:
        return (
            points.ndim == 2 and points.shape[0] > 2 and points.shape[1] == 2
        )

    @staticmethod
    def _compute_bounding_box(points: NDArray[np.float_]) -> BoundingBox2d:
        return BoundingBox2d(
            min_=np.min(points, axis=0), max_=np.max(points, axis=0)
        )

    @staticmethod
    def _duplicated_points_exist(points: NDArray[np.float32]) -> bool:
        _, count = np.unique(points, axis=0, return_counts=True)
        return np.any(count > 1).item()

    @staticmethod
    def _plot_voronoi_diagram(
        voronoi_diagram: scipy.spatial._qhull.Voronoi,
        bounding_box: BoundingBox2d,
    ):
        fig = voronoi_plot_2d(
            voronoi_diagram,
            show_vertices=False,
            line_colors="orange",
            line_alpha=0.6,
            point_size=2,
        )
        ax = fig.axes[0]
        lower_lim, upper_lim = np.min(bounding_box.min_), np.max(
            bounding_box.max_
        )
        ax.set_xlim(lower_lim, upper_lim)
        ax.set_ylim(lower_lim, upper_lim)
        plt.show()

    @classmethod
    def _jitter_points_on_overlap(
        cls,
        points: NDArray[np.float_],
        rng: np.random.Generator,
        scale: float | None = None,
    ) -> NDArray[np.float_]:
        """Apply a slight jittering to all points in case there are points
        with identical coordinates.

        This process guarantees that no two points share the same coordinates.

        Args:
            points:
                See `__init__`.
            rng:
                numpy random number generator.
            scale:
                The magnitude of movement used for jittering the points. If
                set to None, the scale is automatically determined based on
                the bounding box size of the points.

        Returns:
            Original points if no jittering is made. Otherwise, return the
            jittered points.
        """
        bounding_box = cls._compute_bounding_box(points=points)
        if np.isclose(bounding_box.area, 0.0):
            raise ValueError("Points must span a non-zero area")
        if scale is None:
            scale = (
                np.max(bounding_box.max_) - np.min(bounding_box.min_)
            ) * 1e-6
        while cls._duplicated_points_exist(points=points):
            logger.debug("Jitter points as identical points are found")
            is_addition = (
                points
                <= bounding_box.min_
                + (bounding_box.max_ - bounding_box.min_) / 2
            )
            offset = rng.random(size=points.shape) * scale
            points = np.where(is_addition, points + offset, points - offset)
        return points

    @staticmethod
    def _compute_centroid_of_vertices(
        polygon: NDArray[np.float_],
    ) -> NDArray[np.float_]:
        """Find the centroid of vertices.

        The formula used by this method is given here: https://en.wikipedia.org/wiki/Centroid#Of_a_polygon

        Args:
            polygon:
                NDArray of shape (n, 2) for the `n` vertices of the polygon.

        Returns:
            NDArray of shape (2,) representing the x, y coordinates of the
            centroid.
        """
        if len(polygon) <= 3:
            raise ValueError("Polygon must have at least 3 vertices.")
        area = 0
        centroid = np.zeros((2,), dtype=polygon.dtype)
        for i in range(len(polygon) - 1):
            step = (polygon[i, 0] * polygon[i + 1, 1]) - (
                polygon[i + 1, 0] * polygon[i, 1]
            )
            area += step
            centroid[0] += (polygon[i, 0] + polygon[i + 1, 0]) * step
            centroid[1] += (polygon[i, 1] + polygon[i + 1, 1]) * step
        area /= 2
        centroid *= 1.0 / (6.0 * area)
        return centroid

    @classmethod
    def _compute_centroids_of_voronoi_diagram(
        cls,
        voronoi_diagram: scipy.spatial._qhull.Voronoi,
        target_regions_indices: list[int] | None = None,
    ) -> NDArray[np.float_]:
        centroids: list[NDArray[np.float_]] = []
        if target_regions_indices is None:
            target_regions_indices = voronoi_diagram.point_region
        target_regions = [
            voronoi_diagram.regions[i] for i in target_regions_indices
        ]
        for region in target_regions:
            if len(region) == 0 or -1 in region:
                raise ValueError("Unexpected value in region")
            # Enclose the polygon
            polygon_vertices_indices = region + [region[0]]
            # Get the polygon (represented by a list of vertices coordinates)
            # of this region
            polygon = voronoi_diagram.vertices[polygon_vertices_indices]
            # Find the centroid of those vertices
            centroids.append(
                cls._compute_centroid_of_vertices(polygon=polygon)
            )
        return np.array(centroids)

    @abstractmethod
    def compute_delaunay_triangulation(self) -> None:
        pass

    @abstractmethod
    def compute_voronoi_tessellation(self) -> None:
        pass

    @abstractmethod
    def compute_barycentric_dual(self) -> None:
        pass

    @abstractmethod
    def _compute_ridges_and_regions(self) -> None:
        pass

    def get_mocked_scipy_spatial_delaunay(self) -> util.MockedDelaunay:
        """Get an object to be used as the argument in
        `scipy.spatial.delaunay_plot_2d`.
        """
        self.compute_delaunay_triangulation()
        return util.MockedDelaunay(
            points=self._points, simplices=self._triangles
        )

    def get_mocked_scipy_spatial_voronoi(self) -> util.MockedVoronoi:
        """Get an object to be used as the argument in
        `scipy.spatial.voronoi_plot_2d`.
        """
        self.compute_voronoi_tessellation()
        return util.MockedVoronoi(
            points=self._points,
            vertices=self._voronoi_vertices,
            ridge_points=self._ridge_points,
            ridge_vertices=self._ridge_vertices,
            regions=self._regions,
        )

    def get_barycentric_dual_as_mocked_scipy_spatial_voronoi(
        self,
    ) -> util.MockedVoronoi:
        """Get an object to be used as the argument in
        `scipy.spatial.voronoi_plot_2d`.
        """
        self.compute_barycentric_dual()
        return util.MockedVoronoi(
            points=self._points,
            vertices=self._barycentric_dual_vertices,
            ridge_points=self._ridge_points,
            ridge_vertices=self._ridge_vertices,
            regions=self._regions,
        )

    @classmethod
    def voronoi_iteration(
        cls,
        points: NDArray[np.float_],
        rng: np.random.Generator,
        debug: bool = False,
    ) -> NDArray[np.float_]:
        assert cls._check_points_validity(points=points)

        # Make sure there is no overlapping points as it would result in a
        # reduced number of regions compared to the initial number of input
        # points after the Voronoi iteration.
        points = cls._jitter_points_on_overlap(points=points, rng=rng)
        bounding_box = cls._compute_bounding_box(points=points)
        dilated_bounding_box = bounding_box.get_dilated_bounding_box(
            dilation=bounding_box.dimensions
        )
        dilated_bounding_box_vertices = dilated_bounding_box.get_vertices()
        points_with_dilated_bounding_box_vertices = np.append(
            arr=points,
            values=dilated_bounding_box_vertices,
            axis=0,
        )
        # NOTE: Not sure whether qhull_options should be changed
        voronoi_diagram = scipy.spatial.Voronoi(
            points_with_dilated_bounding_box_vertices,
            # qhull_options="Qbb Qc Qx",
        )
        if __debug__:
            if debug:
                cls._plot_voronoi_diagram(voronoi_diagram=voronoi_diagram)

        new_points = cls._compute_centroids_of_voronoi_diagram(
            voronoi_diagram=voronoi_diagram,
            target_regions_indices=voronoi_diagram.point_region[:-4],
        )
        new_points = np.clip(
            new_points, a_min=bounding_box.min_, a_max=bounding_box.max_
        )
        return new_points


class Delaunay(Base):
    def __init__(self, *, points: NDArray[np.float_]) -> None:
        super().__init__(points=points)

        self.compute_delaunay_triangulation()

    def _compute_ridges_and_regions(self) -> None:
        if self._ridges_and_regions_computed:
            return
        self.compute_delaunay_triangulation()
        triangles = self._triangles
        # Retrieve all the edges from triangles
        delaunay_edges = np.moveaxis(
            np.array(
                [
                    [triangles[:, 0], triangles[:, 1]],
                    [triangles[:, 1], triangles[:, 2]],
                    [triangles[:, 2], triangles[:, 0]],
                ]
            ),
            source=2,
            destination=0,
        )
        # Sort the vertices indices of each edge
        delaunay_edges.sort(axis=2)
        # Convert delaunay_edges to Tuple
        delaunay_edges = tuple(
            tuple(map(tuple, edges)) for edges in delaunay_edges
        )
        # Build a mapping from edge to triangles
        delaunay_edge_to_triangle_indices_mapping = defaultdict(list)
        for triangle_index, triangle_edges in enumerate(delaunay_edges):
            for edge in triangle_edges:
                delaunay_edge_to_triangle_indices_mapping[edge].append(
                    triangle_index
                )

        regions: list[list[int]] = [[] for _ in range(len(self._points))]
        indices_of_visited_triangles: set[int] = set()
        dfs_stack = deque()
        dfs_stack.append(0)
        while len(dfs_stack):
            triangle_index = dfs_stack.pop()
            if triangle_index in indices_of_visited_triangles:
                continue
            indices_of_visited_triangles.add(triangle_index)
            triangle = triangles[triangle_index]
            for point_index in triangle:
                regions[point_index].append(triangle_index)
            for edge in delaunay_edges[triangle_index]:
                for (
                    triangle_index
                ) in delaunay_edge_to_triangle_indices_mapping[edge]:
                    dfs_stack.append(triangle_index)

        def connect_triangles(triangles_indices: list[int]) -> list[int]:
            # Build a mapping from edge to triangles
            delaunay_edge_to_triangle_indices_mapping = defaultdict(list)
            for triangle_index in triangles_indices:
                for edge in delaunay_edges[triangle_index]:
                    delaunay_edge_to_triangle_indices_mapping[edge].append(
                        triangle_index
                    )
            # Connect the triangles
            result_reversed: bool = False
            result: list[int] = []
            result.append(triangles_indices[0])
            while len(result) != len(triangles_indices):
                common_edge_found = False
                for edge in delaunay_edges[result[-1]]:
                    for (
                        affiliated_triangle_index
                    ) in delaunay_edge_to_triangle_indices_mapping[edge]:
                        if affiliated_triangle_index not in result:
                            result.append(affiliated_triangle_index)
                            common_edge_found = True
                            break
                    if common_edge_found:
                        break
                if common_edge_found is False:
                    assert not result_reversed
                    result.reverse()
                    result_reversed = True
            # Check whether the head and the tail are connected
            # If not connected, append -1 to the result
            head_edges = set(edge for edge in delaunay_edges[result[0]])
            tail_edges = set(edge for edge in delaunay_edges[result[-1]])
            if len(head_edges.intersection(tail_edges)) == 0:
                result.append(-1)
            return result

        for index, region in enumerate(regions):
            if len(region) < 3:
                regions[index].append(-1)
                continue
            regions[index] = connect_triangles(triangles_indices=region)

        ridge_points = []
        ridge_vertices = []
        for (
            delaunay_edge,
            triangle_indices,
        ) in delaunay_edge_to_triangle_indices_mapping.items():
            assert len(triangle_indices) == 1 or len(triangle_indices) == 2
            ridge_points.append(delaunay_edge)
            ridge_vertices.append(
                triangle_indices
                if len(triangle_indices) == 2
                else [triangle_indices[0], -1]
            )
        ridge_points = np.array(ridge_points)

        self._ridge_points = ridge_points
        self._ridge_vertices = ridge_vertices
        self._regions = regions
        self._ridges_and_regions_computed = True

    def compute_delaunay_triangulation(self) -> None:
        if self._delaunay_triangulation_computed:
            return
        delaunay_graph = scipy.spatial.Delaunay(points=self._points)
        triangles = delaunay_graph.simplices
        self._triangles = triangles
        self._delaunay_triangulation_computed = True

    def compute_voronoi_tessellation(self) -> None:
        if self._voronoi_tessellation_computed:
            return
        self._compute_ridges_and_regions()
        # Compute the circumcenter for each triangle, which is a site in
        # voronoi diagram
        circumcenters = CircumcircleHelper.compute_circumcenters(
            points=self._points[self._triangles]
        )

        # Check for duplicated circumcenters
        unique_circumcenters = np.unique(
            circumcenters,
            axis=0,
            return_counts=False,
            return_index=False,
            return_inverse=False,
        )
        if len(unique_circumcenters) != len(circumcenters):
            raise exceptions.DuplicatedCircumcentersError(
                "Cannot compute voronoi diagram due to duplicated circumcenters"
            )

        self._voronoi_vertices = circumcenters
        self._voronoi_tessellation_computed = True

    def compute_barycentric_dual(self) -> None:
        if self._barycentric_dual_computed:
            return
        self._compute_ridges_and_regions()
        # Compute the centroid for each triangle
        triangles = self._triangles
        centroids = CentroidHelper.compute_centroids(
            points=self._points[triangles]
        )

        self._barycentric_dual_vertices = centroids
        self._barycentric_dual_computed = True
