from dataclasses import dataclass


@dataclass(frozen=True)
class UsuarioService:
    """Servicios de negocio para usuarios."""

    def listar_usuarios(self):
        return []
