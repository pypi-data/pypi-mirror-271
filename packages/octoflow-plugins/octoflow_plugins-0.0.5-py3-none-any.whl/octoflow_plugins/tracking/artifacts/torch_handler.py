from typing import Any

try:
    import torch
    from torch.nn import Module
except ImportError:
    torch = None
    Module = None

from octoflow.tracking.artifact.handler import ArtifactHandler

__all__ = [
    "TorchModuleHandler",
]


class TorchModuleHandler(ArtifactHandler, name="torch.nn.Module"):
    @classmethod
    def can_handle(cls, obj: Any) -> bool:
        if Module is None:
            return False
        return isinstance(obj, Module)

    def exists(self) -> bool:
        return (self.path / "model.pth").exists()

    def load(self) -> Module:
        return torch.load(self.path / "model.pth")

    def save(self, obj: Module):
        torch.save(obj, self.path / "model.pth")
