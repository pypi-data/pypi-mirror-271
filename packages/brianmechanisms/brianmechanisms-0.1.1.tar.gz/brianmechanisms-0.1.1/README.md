# Brian Mechanisms Designer

# Brian Mechanisms

Brian Mechanisms is a Python module designed for engineers and developers to easily design and simulate various mechanical mechanisms and robots. It provides a collection of tools and algorithms for kinematic analysis, motion planning, and visualization of mechanical systems.

## Features

- Kinematic analysis for various types of mechanisms, including linkages, gears, and robotic arms.
- Motion planning algorithms for path generation and trajectory optimization.
- Visualization tools to create interactive plots and animations of mechanical systems.
- Integration with popular libraries such as NumPy and Matplotlib for scientific computing and visualization.

## Installation

You can install Brian Mechanisms using pip:

```bash
pip install brianmechanisms
```

## Quick Start
```python
import brianmechanisms as bm

# Create a simple 2-bar linkage
linkage = bm.Linkage(length1=3, length2=4)

# Plot the linkage
linkage.plot()
```