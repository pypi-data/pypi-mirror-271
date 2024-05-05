# TorchOptics

> Differentiable diffractive optics simulator using PyTorch.

## Usage
Field propagation example:

```python
import torch
from torchoptics.propagation import propagator

input_field = torch.ones(100, 100)
succeeding_shape = 200
propagation_distance = .3
wavelength = 780e-9
grid_size = 10e-6

output_field = propagator(input_field, succeeding_shape, propagation_distance, wavelength, grid_size)
```
