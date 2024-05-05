import torch
from torch.fft import fft2, ifft2


def propagator(
    field,
    succeeding_shape,
    propagation_distance,
    wavelength,
    grid_size,
):
    if field.shape[-1] != field.shape[-2]:
        raise ValueError("Expected field to be a square matrix.")
    grid_extent = (field.shape[-1] + succeeding_shape) / 2
    coords = torch.arange(-grid_extent + 1, grid_extent, dtype=torch.double)
    x, y = torch.meshgrid(coords * grid_size, coords * grid_size, indexing="ij")

    r_squared = x**2 + y**2 + propagation_distance**2
    r = torch.sqrt(r_squared)
    impulse_response = (
        (propagation_distance / r_squared * (1 / (2 * torch.pi * r) - 1.0j / wavelength))
        * torch.exp(2j * torch.pi * r / wavelength)
        * grid_size**2
    )
    return conv2d_fft(fft2(impulse_response), field)


def conv2d_fft(H_fr, x):
    output_size = (H_fr.size(-2) - x.size(-2) + 1, H_fr.size(-1) - x.size(-1) + 1)
    x_fr = fft2(x.flip(-1, -2).conj(), s=(H_fr.size(-2), H_fr.size(-1)))
    output_fr = H_fr * x_fr.conj()
    output = ifft2(output_fr)[..., : output_size[0], : output_size[1]].clone()
    return output
