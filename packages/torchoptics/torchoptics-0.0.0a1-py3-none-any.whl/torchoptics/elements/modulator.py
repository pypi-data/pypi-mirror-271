from torch.nn import Module


class Modulator(Module):
    def __init__(self, modulation_profile):
        super().__init__()
        if modulation_profile.dim() != 2:
            raise ValueError(
                f"Expected modulation_profile to be a 2D tensor, but got {modulation_profile.dim()}D"
            )
        self.modulation_profile = modulation_profile

    def forward(self, field):
        return self.modulation_profile * field
