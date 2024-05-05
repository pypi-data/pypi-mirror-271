from torch.nn import Module
from torch.nn.functional import linear


class Detector(Module):
    def __init__(self, weight, grid_size):
        super().__init__()
        if weight.dim() != 3:
            raise ValueError(f"Expected weight to be a 3D tensor, but got {weight.dim()}D")
        self.weight = weight
        self.grid_size = grid_size

    def forward(self, intensity):
        intensity_flat, weight_flat = intensity.flatten(start_dim=-2), self.weight.flatten(start_dim=-2)
        return linear(intensity_flat, weight_flat) * self.grid_size**2
