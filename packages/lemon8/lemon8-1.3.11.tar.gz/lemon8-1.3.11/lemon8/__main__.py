import argparse
import logging
from importlib.resources import files

import pygame

from .components import (CPU, INIT_LOC_CONSTANT, TICK, WAVE, Display, Keypad,
                         Memory)

logging.basicConfig(
    format="%(asctime)s:%(msecs)03d (%(levelname)s/%(module)s): %(message)s",
    level=logging.DEBUG,
    encoding="utf-8",
    datefmt="%M:%S",
)


class Lemon:
    """
    As the main entry point for lemon emulator,
    this class takes care of interfacing with the user and
    the internal devices.
    """

    __slots__ = ("cpu", "display", "keypad", "memory")

    def __init__(self, rom: str, mul: int) -> None:
        """
        Lemon Constructor.
        The constructor is responsible for loading font and rom, and also initializing other
        devices.

        Args:
            rom: Path to the ROM file.
            mul: The screen size multiplier.

        Attributes:
            memory (Memory): Primary Memory of size 4096 bytes.
            display (Display): Display Handler for rendering sprites.
            keypad (Keypad): 16-key hexadecimal keypad for taking input.
            cpu (CPU): Object representing Central Processing Unit of the emulator.
        """
        self.memory: Memory = Memory()
        self.load_font()
        self.load_rom(rom)
        self.display: Display = Display.create(multiplier=mul)
        self.keypad: Keypad = Keypad()
        self.cpu: CPU = CPU(
            display=self.display, memory=self.memory, keypad=self.keypad
        )

    def load_font(self) -> None:
        """
        Load Font from the `/bin/FONT` file in memory from location `0x0`
        """
        self.memory.load_binary(files("lemon8.bin").joinpath("FONT").read_bytes())
        logging.info(f"{TICK} Successfully loaded Fontset at location 0x0")

    def load_rom(self, rom: str) -> None:
        """
        Load ROM in memory from location `0x200` (512)

        Args:
            rom: Path to the ROM file.
        """
        self.memory.load_binary(open(rom, "rb").read(), offset=INIT_LOC_CONSTANT)
        logging.info(
            f"{TICK} Successfully loaded ROM at location {hex(INIT_LOC_CONSTANT)}"
        )

    def tick(self) -> None:
        """
        Method representing a single tick from the emulator.
        """
        for ic in range(10):
            if not self.cpu.halt:
                self.cpu.cycle()
                self.cpu.sync = not ic
            self.display.render()

        self.cpu.handle_timers()

    def run(self) -> None:
        """
        Step through the emulation indefinitely.
        """
        is_running = True
        while is_running:
            self.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    self.keypad.handle(event)
                if event.type == pygame.KEYUP:
                    if event.key in self.keypad.keymap:
                        key = self.cpu.keypad.keymap[event.key]
                        if self.cpu.halt:
                            self.cpu.V[self.cpu.op.x] = key
                            self.cpu.halt = False
                        self.keypad.unset(key)

        self.display.destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Lemon", description="Chip-8 Virtual Machine."
    )
    parser.add_argument("rom", help="Path to the rom file.")
    parser.add_argument(
        "-S",
        "--scale",
        help="Scale up or down the display window.",
        type=int,
        default=10,
    )
    args = parser.parse_args()

    lemon = Lemon(args.rom, args.scale)

    try:
        lemon.run()
    except KeyboardInterrupt:
        logging.info(f"bye {WAVE}")
