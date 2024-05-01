# Short explanation

Figurify is a Python library that allows you to perform various calculations related to geometric figures. With Figurify, you can quickly and easily calculate properties such as perimeter, area, angles, and more for various geometric shapes.

## Installation

You can easily install Figurify using pip:

    pip install figurify

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

And there are many functions in every Python file.<br>
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

Here's a simple example of how to use Figurify in your Python project:

```python
import figurify

print(figurify.material_properties.volume(20, 1.4),
      figurify.units.cubic_centimetres)

print(figurify.plane_metrics.circle.area(5))
print(figurify.plane_metrics.circle.radius(2.5))

print(figurify.plane_metrics.trapezoid.area(2, 4, 8))
print(figurify.plane_metrics.trapezoid.height(20, 2, 4))

print(figurify.geometric_solids.cube.volume(5), figurify.units.cubic_centimetres)

area = figurify.plane_metrics.parallelogram.area(5, 10)

print(figurify.units.square_cm_to_square_dm(area), figurify.units.square_decimetres)

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

# Documentation

Welcome to the documentation for Figurify. It is a large library for Python with which you can perform calculations for figures, surfaces and also physics calculations. 
## Importing

You can easily import figurify using:

```python
import figurify
```

## Funktions

As you can see above,
with figurify you can do a lot of calculations on
figures, surfaces and physics calculations,
but what you see above are only the
files in which the functions are.
So you have a lot of functions to choose from and here
they are explained step by step.

### _plane_metrics_

#### circle

###### Funktions:

    circumference
    area
    diameter
    radius
    arc_length
    sector_area
    inscribed_angle
    central_angle
    sector_radius
    sector_angle
    arc_angle
    segment_area

A code example:

```python
import figurify

figurify.plane_metrics.circle.area(4)
```

#### ellipse

###### Funktions:

    area
    perimeter
    focal_distance
    eccentricity
    vertex_distance
    semi_latus_rectum
    linear_eccentricity
    co_vertex_distance
    focus_distance
    major_axis_length
    minor_axis_length
    semi_major_axis_length
    semi_minor_axis_length

A code example:

```python
import figurify

figurify.plane_metrics.ellipse.area(5, 6)
```

#### parallelogram

###### Funktions:

    area
    perimeter
    diagonal
    height
    side_from_area
    side_from_perimeter
    angle_between_diagonals
    acos_safe
    sin

A code example:

```python
import figurify

figurify.plane_metrics.parallelogram.area(4, 9)
```

#### polygon

###### Funktions:

    perimeter
    interior_angle
    apothem
    area
    side_length
    exterior_angle
    diagonal

A code example:

```python
import figurify

figurify.plane_metrics.polygon.area(4, 8)
```

#### quadrilateral

###### Funktions:

    perimeter
    area
    diagonal_length
    interior_angle
    semiperimeter
    height
    is_parallelogram
    is_rhombus
    is_rectangle
    is_square

A code example:

```python
import figurify

figurify.plane_metrics.quadrilateral.area(5, 5, 90)
```

#### rectangle

###### Funktions:

    perimeter
    area
    diagonal_length
    is_square
    is_golden_rectangle
    interior_angle
    is_regular
    is_oblong

A code example:

```python
import figurify

figurify.plane_metrics.rectangle.area(2, 4)
```

#### trapezoid

###### Funktions:

    area
    perimeter
    height
    side_length
    base_midline
    side_from_perimeter
    base_from_perimeter
    side_from_area
    angle_at_base
    angle_at_top
    diagonal
    side_diagonal
    base_diagonal
    interior_angle
    apothem

A code example:

```python
import figurify

figurify.plane_metrics.trapezoid.area(2, 2, 4)
```

#### triangle

###### Funktions:

    perimeter
    area
    is_equilateral
    is_isosceles
    is_scalene
    is_right
    is_acute
    is_obtuse
    height
    semiperimeter

A code example:

```python
import figurify

figurify.plane_metrics.triangle.area(2, 4)
```

### _geometric_solids_

#### cone

###### Funktions:

    volume
    surface_area
    lateral_area
    base_area
    slant_height
    surface_area_with_slant_height
    volume_with_slant_height
    lateral_area_with_slant_height
    half_angle
    half_angle_degrees

A code example:

```python
import figurify

figurify.geometric_solids.cone.volume(4, 12)
```

#### cube

###### Funktions:

    volume
    surface_area
    diagonal_length
    face_diagonal_length
    space_diagonal_length
    inner_surface_area
    edge_length
    total_edge_length
    inner_volume
    inner_diagonal_length

A code example:

```python
import figurify

figurify.geometric_solids.cube.volume(7)
```

#### cuboid

###### Funktions:

    volume
    surface_area
    diagonal_length
    face_diagonal_length
    space_diagonal_length
    inner_surface_area
    edge_length
    total_edge_length
    inner_volume
    inner_diagonal_length

A code example:

```python
import figurify

figurify.geometric_solids.cuboid.volume(4, 5, 9)
```

#### cylinder

###### Funktions:

    volume
    lateral_area
    surface_area
    base_area
    curved_surface_area
    total_area
    diagonal_length
    lateral_surface_area_with_diagonal
    total_area_with_diagonal

A code example:

```python
import figurify

figurify.geometric_solids.cylinder.volume(4, 5)
```

#### prism

###### Funktions:

    volume
    surface_area
    lateral_area
    base_area
    total_area
    diagonal_length
    lateral_surface_area_with_diagonal
    total_area_with_diagonal

A code example:

```python
import figurify

figurify.geometric_solids.prism.volume(30, 8)
```

#### pyramid

###### Funktions:

    volume
    surface_area
    lateral_area
    base_area
    total_area
    apothem
    surface_area_with_apothem
    total_area_with_apothem
    slant_height
    total_edge_length
    inner_surface_area
    inner_volume
    inner_diagonal_length

A code example:

```python
import figurify

figurify.geometric_solids.pyramid.volume(20, 9)
```

#### sphere

###### Funktions:

    volume
    surface_area
    circumference
    cross_sectional_area
    spherical_cap_volume
    spherical_cap_surface_area
    spherical_sector_volume
    spherical_sector_surface_area
    chord_length
    great_circle_distance

A code example:

```python
import figurify

figurify.geometric_solids.sphere.volume(7)
```

#### torus

###### Funktions:

    volume
    surface_area
    major_circumference
    minor_circumference
    mean_radius
    cross_sectional_area
    ring_volume
    ring_surface_area
    inner_radius
    inner_circumference

A code example:

```python
import figurify

figurify.geometric_solids.torus.volume(5, 4)
```

### _figure_physics_

#### dynamics

###### Funktions:

    velocity
    acceleration
    displacement
    force
    momentum
    impulse
    kinetic_energy
    gravitational_potential_energy
    work
    power

A code example:

```python
import figurify

figurify.figure_physics.dynamics.velocity(30, 3.6)
```

#### energy

###### Funktions:

    kinetic_energy
    gravitational_potential_energy
    elastic_potential_energy
    mechanical_energy
    thermal_energy
    electrical_energy
    sound_energy

A code example:

```python
import figurify

figurify.figure_physics.energy.sound_energy(400, 800)
```

#### forces

###### Funktions:

    force
    weight
    tension
    friction_coefficient
    gravitational_force
    spring_force
    buoyant_force
    magnetic_force

A code example:

```python
import figurify

figurify.figure_physics.forces.force(20, 7)
```

#### gravity

###### Funktions:

    gravitational_force
    gravitational_acceleration
    gravitational_potential_energy
    escape_velocity
    orbital_period

A code example:

```python
import figurify

figurify.figure_physics.gravity.orbital_period(3, 70)
```

#### kinematics

###### Funktions:

    average_speed
    average_velocity
    acceleration
    final_velocity
    displacement
    final_velocity_squared

A code example:

```python
import figurify

figurify.figure_physics.kinematics.acceleration(20, 50, 80)
```

#### momentum

###### Funktions:

    momentum
    impulse
    kinetic_energy
    velocity
    collision_velocity
    recoil_velocity

A code example:

```python
import figurify

figurify.figure_physics.momentum.momentum(30, 12)
```

### material_properties

###### Funktions:

    density
    mass
    volume
    flexibility
    strength
    melting_point
    boiling_point
    conductivity
    refractive_index

A code example:

```python
import figurify

figurify.material_properties.density(20, 40)
```

### units

###### Funktions:

    milimetres_to_centimetres
    centimetres_to_decimetres
    decimetres_to_metres
    metres_to_kilometres
    centimetres_to_milimetres
    decimetres_to_centimetres
    metres_to_decimetres
    kilometres_to_metres
    square_mm_to_square_cm
    square_cm_to_square_dm
    square_dm_to_square_m
    square_m_to_square_km
    square_cm_to_square_mm
    square_dm_to_square_cm
    square_m_to_square_dm
    square_km_to_square_m
    cubic_mm_to_cubic_cm
    cubic_cm_to_cubic_dm
    cubic_dm_to_cubic_m
    cubic_m_to_cubic_km
    cubic_cm_to_cubic_mm
    cubic_dm_to_cubic_cm
    cubic_m_to_cubic_dm
    cubic_km_to_cubic_m

A code example:

```python
import figurify

figurify.units.square_cm_to_square_dm(30)
```

###### Variables:

    milimetres
    square_milimetres
    cubic_milimetres
    centimetres
    square_centimetres
    cubic_centimetres
    decimetres
    square_decimetres
    cubic_decimetres
    metres
    square_metres
    cubic_metres
    kilometres
    square_kilometres
    cubic_kilometres
    grams
    litres

A code example:

```python
import figurify

centimetres = (figurify.units.decimetres_to_centimetres(400), figurify.units.centimetres)
```
