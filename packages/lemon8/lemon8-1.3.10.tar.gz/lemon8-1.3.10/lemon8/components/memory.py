import importlib.resources as ilr

__all__ = ("Memory",)


class Memory:
    """
    Primary Memory of the CPU.
    """

    __slots__ = ("space",)

    def __init__(self) -> None:
        """
        Memory Constructor.

        Attributes:
            space (bytearray): A bytearray of size 4096 virtually representing CHP-8 memory.
        """
        self.space: bytearray = bytearray(4096)

    def load_binary(self, binary: bytes, offset: int = 0) -> None:
        """
        Load file onto the RAM.

        Arguments:
            binary: Path to the binary.
            offset: From where to start loading the elements of the binary.
        """
        for i, data in enumerate(binary):
            self.space[i + offset] = data
