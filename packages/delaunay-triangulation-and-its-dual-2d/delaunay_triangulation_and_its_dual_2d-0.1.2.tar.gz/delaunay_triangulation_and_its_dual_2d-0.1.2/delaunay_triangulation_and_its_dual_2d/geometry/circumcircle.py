import dataclasses

import numpy as np
from numpy.typing import NDArray


@dataclasses.dataclass
class Circumcircle:
    center: tuple[float, float]
    radius: float


class CircumcircleHelper:
    @staticmethod
    def compute_circumcenters(
        points: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Compute the circumcenters of triangles.

        Args:
            points:
                An array of shape (n, 3, 2). The first dimension "n"
                refers to the number of batches. The second dimension refers to
                the three vertices of a triangle used for calculating the
                circumcenter. The third dimension represents the (x, y)
                Cartesian coordinates of the points.
        """
        return CircumcircleHelper.compute_circumcenters_v4(points=points)

    @staticmethod
    def compute_circumcenters_v3(
        points: NDArray[np.float32],
    ) -> NDArray[np.float32]:  # pragma: no cover
        """Compute the circumcenters of triangles.

        Args:
            points:
                See method `compute_circumcenters`.
        """
        midpoints = (points[:, :2] + points[:, 1:]) / 2
        slopes = (points[:, 1:, 1] - points[:, :2, 1]) / (
            points[:, 1:, 0] - points[:, :2, 0]
        )
        orthogonal_slopes = -1 / slopes

        # Solve Ax = b for the circumcenter
        matrix_a = np.stack(
            [orthogonal_slopes, -np.ones_like(orthogonal_slopes)], axis=-1
        )
        b = np.sum(midpoints * matrix_a, axis=-1)
        circumcenter = np.linalg.solve(matrix_a, b)
        return circumcenter

    @staticmethod
    def compute_circumcenters_v4(
        points: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Compute the circumcenters of triangles.

        Args:
            points:
                See method `compute_circumcenters`.

        References:
            - How do I find the circumcenter of the triangle using python
                without external libraries?
                [link](https://stackoverflow.com/a/56225021)
        """
        A, B, C = points[:, 0], points[:, 1], points[:, 2]
        Ax, Ay = A[:, 0], A[:, 1]
        Bx, By = B[:, 0], B[:, 1]
        Cx, Cy = C[:, 0], C[:, 1]

        D = 2 * (Ax * (By - Cy) + Bx * (Cy - Ay) + Cx * (Ay - By))
        Ux = (
            (Ax**2 + Ay**2) * (By - Cy)
            + (Bx**2 + By**2) * (Cy - Ay)
            + (Cx**2 + Cy**2) * (Ay - By)
        ) / D
        Uy = (
            (Ax**2 + Ay**2) * (Cx - Bx)
            + (Bx**2 + By**2) * (Ax - Cx)
            + (Cx**2 + Cy**2) * (Bx - Ax)
        ) / D

        return np.stack((Ux, Uy), axis=-1)
