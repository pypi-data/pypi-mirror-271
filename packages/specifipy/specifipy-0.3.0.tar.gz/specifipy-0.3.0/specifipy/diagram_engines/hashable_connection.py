from py_d2 import D2Connection


class D2HashableConnection(D2Connection):
    def __hash__(self):
        return hash((self.shape_1, self.shape_2, self.direction))

    def __eq__(self, other) -> bool:
        if (self.shape_1, self.shape_2, self.direction, self.label) == (
            other.shape_1,
            other.shape_2,
            other.direction,
            other.label,
        ):
            return True
        return False
