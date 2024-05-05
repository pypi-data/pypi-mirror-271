import numpy as np
from numpy.typing import NDArray


class CentroidHelper:
    @staticmethod
    def compute_centroids(points: NDArray[np.float32]) -> NDArray[np.float32]:
        return np.mean(points, axis=1)
