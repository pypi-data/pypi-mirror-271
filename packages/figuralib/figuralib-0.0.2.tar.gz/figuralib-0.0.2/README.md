FiguraLib is a Python library that allows you to perform various calculations related to geometric figures. With FiguraLib, you can quickly and easily calculate properties such as perimeter, area, angles, and more for various geometric shapes.

## Installation

You can easily install FiguraLib using pip:

    pip install figuralib

## All files

    material_properties
    units

Geometric Solids

    Cube
    Cuboid
    Cylinder
    Cone
    Sphere
    Torus
    Prism
    Pyramid

Plane Metrics

    Circle
    Rectangle
    Triangle
    Square
    Trapezoid
    Polygon
    Ellipse
    Parallelogram
    Quadrilateral

Figure Physics

    Dynamics
    Forces
    Energy
    Gravity
    Kinematics
    Momentum  

What you see above, are only the
files in which the functions are.<br>
So you have a lot of functions to choose from.
For more information about the available functions and figures, see the documentation.

## Bugs

We welcome contributions from other developers! If you've found a bug or want to add a new feature, feel free to create an issue or submit a pull request.<br>

## License

This project is licensed under the MIT License. See the license file for more information.

**Permissions:**

* Commercial use
* Modification
* Distribution
* Private use

**Limitations**:

* Liability
* Warranty

**Conditions**:

* License and copyright notice

**_It is licensed under Copyright (c) 2024 Julian Hess_**


## Usage

Here is a simple example of how to use FiguraLib in your Python project:

### Importing

You can easily import FiguraLib using:

```python
import figuralib
```

A code example:

```python
import figuralib

print(figuralib.material_properties.volume(20, 1.4),
      figuralib.units.cubic_centimetres)

print(figuralib.plane_metrics.circle.area(5))
print(figuralib.plane_metrics.circle.radius(2.5))

print(figuralib.plane_metrics.trapezoid.area(2, 4, 8))
print(figuralib.plane_metrics.trapezoid.height(20, 2, 4))

print(figuralib.geometric_solids.cube.volume(5), figuralib.units.cubic_centimetres)

area = figuralib.plane_metrics.parallelogram.area(5, 10)

print(figuralib.units.square_cm_to_square_dm(area), figuralib.units.square_decimetres)

# And there's much more, see above.
```

### Output:

    14.285714285714286 cm³
    78.53975
    1.25
    24.0
    6.666666666666667
    125 cm³
    0.5 dm²