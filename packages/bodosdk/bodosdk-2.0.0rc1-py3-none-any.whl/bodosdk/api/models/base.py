from enum import Enum


class BodoRole(Enum):
    ADMIN = "BodoAdmin"
    VIEWER = "BodoViewer"

    def __str__(self):
        return str(self.value)
