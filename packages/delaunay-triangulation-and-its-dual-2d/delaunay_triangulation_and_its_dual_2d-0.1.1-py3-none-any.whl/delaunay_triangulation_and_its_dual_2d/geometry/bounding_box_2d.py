from __future__ import annotations

import dataclasses

import numpy as np
from numpy.typing import NDArray


@dataclasses.dataclass
class BoundingBox2d:
    min_: NDArray[np.float32]
    max_: NDArray[np.float32]

    def __post_init__(self) -> None:
        """

        Args:
            min_:
                A 2D point in the Cartesian coordinate system represented by an
                array of shape (2,).
            max_:
                See `min_`.
        """
        assert self.min_.shape == (2,), self.min_.shape
        assert self.max_.shape == (2,), self.max_.shape
        assert np.all(self.min_ <= self.max_)

    @property
    def min_x(self) -> float:
        return self.min_[0]

    @property
    def min_y(self) -> float:
        return self.min_[1]

    @property
    def max_x(self) -> float:
        return self.max_[0]

    @property
    def max_y(self) -> float:
        return self.max_[1]

    @property
    def dimensions(self) -> NDArray[np.float32]:
        return self.max_ - self.min_

    @property
    def area(self) -> float:
        return np.prod(self.dimensions)

    def get_vertices(self) -> NDArray[np.float32]:
        return np.array(
            [
                [self.min_x, self.min_y],
                [self.min_x, self.max_y],
                [self.max_x, self.max_y],
                [self.max_x, self.min_y],
            ]
        )

    def get_dilated_bounding_box(
        self, dilation: NDArray[np.float32] | float
    ) -> BoundingBox2d:
        return BoundingBox2d(
            min_=self.min_ - dilation, max_=self.max_ + dilation
        )
