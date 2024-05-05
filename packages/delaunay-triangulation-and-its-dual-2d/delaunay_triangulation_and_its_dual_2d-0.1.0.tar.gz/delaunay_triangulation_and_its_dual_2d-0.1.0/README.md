# delaunay-triangulation-and-its-dual-2d

The `scipy.spatial` module has data structures to construct Delaunay tessellation and Voronoi diagram, given a set of points. However, it does not link the attributes of the two diagrams even though duality exists between them. For example, each simplex in Delaunay diagram corresponds to a vertex in Voronoi diagram and there are cases that we may want to make use of this relationship.

Therefore, this small extension is written to blend the attributes of the dual. In current version, it only provides the `Delaunay` class to construct a 2D Delaunay diagram at initialization. Afterwards, you can call corresponding functions to get its dual. See section [Usage](#usage) for examples.

## Installation
```bash
$ pip install delaunay-triangulation-and-its-dual-2d
```

## Usage

Import packages and prepare points as a numpy array of shape (n, 2), where `n` is the number of points and `2` are the Cartesian coordinates of the point.

```python
import numpy as np
import scipy.spatial

import delaunay_triangulation_and_its_dual_2d

points = np.array([[0, 0], [1, 0], [2, 0], [1, 1]], dtype=np.float32)
```

### Voronoi iteration

If points are not well-distributed, the Voronoi graph of the points will contain lots of non-uniform polygons. Voronoi iteration, also called Lloyd's algorithm, could be used to offset the points so that the Voronoi graph generated from the new points are more uniformly sized.

```python
rng = np.random.default_rng()
delaunay_triangulation_and_its_dual_2d.voronoi_iteration(
    points=points, rng=rng
)
```

### Delaunay triangulation

Below is an example to initialize the `delaunay_triangulation_and_its_dual_2d.Delaunay` object and then plot the diagram using the `scipy.spatial.delaunay_plot_2d` function.

```python
delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
scipy.spatial.delaunay_plot_2d(delaunay.get_mocked_scipy_spatial_delaunay())
```

### Voronoi tessellation (Circumcentric mesh)

Below is an example to initialize the `delaunay_triangulation_and_its_dual_2d.Delaunay` object and then plot the Voronoi diagram using the `scipy.spatial.voronoi_plot_2d` function.

```python
delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
scipy.spatial.voronoi_plot_2d(delaunay.get_mocked_scipy_spatial_voronoi())
```

### Barycentric mesh

Below is an example to initialize the `delaunay_triangulation_and_its_dual_2d.Delaunay` object and then plot the Barycentric mesh diagram using the `scipy.spatial.voronoi_plot_2d` function.

```python
delaunay = delaunay_triangulation_and_its_dual_2d.Delaunay(points=points)
scipy.spatial.voronoi_plot_2d(
    delaunay.get_barycentric_dual_as_mocked_scipy_spatial_voronoi()
)
```

### Relationships between attributes

Attributes which have a one-to-one mapping with the given points have the same order as the points. FOr example, `delaunay.points` are the points provided at initialization. This first point `delaunay.points[0]` corresponds to the first delaunay triangle `delaunay.triangles[0]`, which in turn corresponds to the first Voronoi vertex `delaunay.voronoi_vertices[0]`.

## Styles of codes and comments
- Google Python Style Guide [link](https://google.github.io/styleguide/pyguide.html)

## References
- How do I derive a Voronoi diagram given its point set and its Delaunay triangulation? [link](https://stackoverflow.com/q/85275)
- duhaime/lloyd. [link](https://github.com/duhaime/lloyd/tree/master)

## Remarks

Construction of the Delaunay diagram at initialization of `delaunay_triangulation_and_its_dual_2d.Delaunay` object is fast as it just calls `scipy.spatial.Delaunay` to get the attributes. Yet, the conversions to its dual is written in Python codes in this package so it is 3 - 5 times slower than calling `scipy.spatial.Voronoi` directly. You can make the comparison yourself using the "tests\delaunay\performance.py" script.

## License

This project is licensed under the terms of the MIT license.
