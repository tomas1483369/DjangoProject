from dataclasses import dataclass


@dataclass(frozen=True)
class ProductoService:
    """Servicios de negocio para productos."""

    def listar_productos(self):
        return []
