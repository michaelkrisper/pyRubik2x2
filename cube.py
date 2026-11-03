# ANSI-colored stickers: yellow, red, white, purple, blue, green.
Y, R, W, P, B, G = ("\x1b[1;33;43m Y \x1b[0m", "\x1b[1;31;41m R \x1b[0m", "\x1b[1;37;47m W \x1b[0m",
                    "\x1b[1;35;45m P \x1b[0m", "\x1b[1;34;44m B \x1b[0m", "\x1b[1;32;42m G \x1b[0m")
COLORS = {"Y": Y, "R": R, "W": W, "P": P, "B": B, "G": G}


class RubikCube:
    """
    Represents a 2x2 Rubik's Cube.

    This class encapsulates the state of the cube and provides methods for
    manipulating it. The cube's state is represented as a 3D list, where
    the first dimension represents the faces of the cube, and the next two
    dimensions represent the 2x2 grid of colors on each face.
    """
    def __init__(self, initial_state=None):
        """
        Initializes the Rubik's Cube.

        Args:
            initial_state (str, optional): A string representing the initial
                state of the cube. If not provided, the cube is initialized
                to its solved state. Defaults to None.
        """
        if initial_state:
            self.cube = self._read_cube(initial_state)
        else:
            self.cube = self.default_cube()

    def default_cube(self):
        """
        Creates a new cube in its default (solved) state.

        Returns:
            list: A 3D list representing the solved cube.
        """
        return [
            [[Y, Y], [Y, Y]],
            [[R, R], [R, R]],
            [[W, W], [W, W]],
            [[P, P], [P, P]],
            [[B, B], [B, B]],
            [[G, G], [G, G]]
        ]

    def copy_cube(self):
        """
        Creates a deep copy of the current cube state.

        Returns:
            list: A new 3D list that is a copy of the current cube.
        """
        return [[row[:] for row in side] for side in self.cube]

    def copy(self):
        """
        Creates an independent copy of this cube.

        Returns:
            RubikCube: A new cube with the same state.
        """
        new_cube = RubikCube()
        new_cube.cube = self.copy_cube()
        return new_cube

    def _read_cube(self, input_text):
        """
        Parses a string to create a cube state.

        Args:
            input_text (str): A string of 24 characters representing the
                              colors of the cube's faces.

        Returns:
            list: A 3D list representing the parsed cube state.

        Raises:
            ValueError: If the text is not 24 valid color letters.
        """
        if len(input_text) != 24 or not set(input_text.upper()) <= set(COLORS):
            raise ValueError("A cube state needs exactly 24 color letters out of Y, R, W, P, B, G.")
        input_cube = self.default_cube()
        char_position = 0
        for side in range(6):
            for row in [0, 1]:
                for pos in [0, 1]:
                    input_cube[side][row][pos] = COLORS[input_text[char_position].upper()]
                    char_position += 1
        return input_cube

    def get_key(self):
        """
        Generates a unique string key for the current cube state.

        Returns:
            str: A string representing the flattened state of the cube.
        """
        return "".join([pos for side in self.cube for row in side for pos in row])

    def print_cube(self):
        """Prints a visual representation of the cube to the console."""
        c = self.cube
        print("        ╔═══╤═══╗")
        print("        ║%s│%s║" % (c[0][0][0], c[0][0][1]))
        print("        ╟───┼───╢")
        print("        ║%s│%s║" % (c[0][1][0], c[0][1][1]))
        print("╔═══╤═══╬═══╪═══╬═══╤═══╦═══╤═══╗")
        print("║%s│%s║%s│%s║%s│%s║%s│%s║" % (
        c[4][0][0], c[4][0][1], c[1][0][0], c[1][0][1], c[5][0][0], c[5][0][1], c[3][1][1], c[3][1][0]))
        print("╫───┼───╫───┼───╫───┼───╫───┼───╢")
        print("║%s│%s║%s│%s║%s│%s║%s│%s║" % (
        c[4][1][0], c[4][1][1], c[1][1][0], c[1][1][1], c[5][1][0], c[5][1][1], c[3][0][1], c[3][0][0]))
        print("╚═══╧═══╬═══╪═══╬═══╧═══╩═══╧═══╝")
        print("        ║%s│%s║" % (c[2][0][0], c[2][0][1]))
        print("        ╟───┼───╢")
        print("        ║%s│%s║" % (c[2][1][0], c[2][1][1]))
        print("        ╚═══╧═══╝")

    def move_left_down(self):
        """Rotates the left face of the cube downwards."""
        (self.cube[0][0][0], self.cube[0][1][0],
         self.cube[1][0][0], self.cube[1][1][0],
         self.cube[2][0][0], self.cube[2][1][0],
         self.cube[3][0][0], self.cube[3][1][0],
         self.cube[4][0][0], self.cube[4][0][1],
         self.cube[4][1][0], self.cube[4][1][1]) = (self.cube[3][0][0], self.cube[3][1][0],
                                                   self.cube[0][0][0], self.cube[0][1][0],
                                                   self.cube[1][0][0], self.cube[1][1][0],
                                                   self.cube[2][0][0], self.cube[2][1][0],
                                                   self.cube[4][1][0], self.cube[4][0][0],
                                                   self.cube[4][1][1], self.cube[4][0][1])

    def move_right_down(self):
        """Rotates the right face of the cube downwards."""
        (self.cube[0][0][1], self.cube[0][1][1],
         self.cube[1][0][1], self.cube[1][1][1],
         self.cube[2][0][1], self.cube[2][1][1],
         self.cube[3][0][1], self.cube[3][1][1],
         self.cube[5][0][0], self.cube[5][0][1],
         self.cube[5][1][0], self.cube[5][1][1]) = (self.cube[3][0][1], self.cube[3][1][1],
                                                   self.cube[0][0][1], self.cube[0][1][1],
                                                   self.cube[1][0][1], self.cube[1][1][1],
                                                   self.cube[2][0][1], self.cube[2][1][1],
                                                   self.cube[5][0][1], self.cube[5][1][1],
                                                   self.cube[5][0][0], self.cube[5][1][0])

    def move_right_up(self):
        """Rotates the right face of the cube upwards."""
        self.move_right_down()
        self.move_right_down()
        self.move_right_down()

    def move_left_up(self):
        """Rotates the left face of the cube upwards."""
        self.move_left_down()
        self.move_left_down()
        self.move_left_down()

    def move_top_left(self):
        """Rotates the top face of the cube to the left."""
        (self.cube[1][0][0], self.cube[1][0][1],
         self.cube[4][0][0], self.cube[4][0][1],
         self.cube[3][1][0], self.cube[3][1][1],
         self.cube[5][0][0], self.cube[5][0][1],
         self.cube[0][0][0], self.cube[0][0][1],
         self.cube[0][1][0], self.cube[0][1][1]) = (self.cube[5][0][0], self.cube[5][0][1],
                                                   self.cube[1][0][0], self.cube[1][0][1],
                                                   self.cube[4][0][1], self.cube[4][0][0],
                                                   self.cube[3][1][1], self.cube[3][1][0],
                                                   self.cube[0][1][0], self.cube[0][0][0],
                                                   self.cube[0][1][1], self.cube[0][0][1])

    def move_top_right(self):
        """Rotates the top face of the cube to the right."""
        self.move_top_left()
        self.move_top_left()
        self.move_top_left()

    def move_bottom_left(self):
        """Rotates the bottom face of the cube to the left."""
        (self.cube[1][1][0], self.cube[1][1][1],
         self.cube[4][1][0], self.cube[4][1][1],
         self.cube[3][0][0], self.cube[3][0][1],
         self.cube[5][1][0], self.cube[5][1][1],
         self.cube[2][0][0], self.cube[2][0][1],
         self.cube[2][1][0], self.cube[2][1][1]) = (self.cube[5][1][0], self.cube[5][1][1],
                                                   self.cube[1][1][0], self.cube[1][1][1],
                                                   self.cube[4][1][1], self.cube[4][1][0],
                                                   self.cube[3][0][1], self.cube[3][0][0],
                                                   self.cube[2][0][1], self.cube[2][1][1],
                                                   self.cube[2][0][0], self.cube[2][1][0])

    def move_bottom_right(self):
        """Rotates the bottom face of the cube to the right."""
        self.move_bottom_left()
        self.move_bottom_left()
        self.move_bottom_left()

    def move_front_clockwise(self):
        """Rotates the front face of the cube clockwise."""
        (self.cube[0][1][0], self.cube[0][1][1],
         self.cube[4][0][1], self.cube[4][1][1],
         self.cube[2][0][0], self.cube[2][0][1],
         self.cube[5][0][0], self.cube[5][1][0],
         self.cube[1][0][0], self.cube[1][0][1],
         self.cube[1][1][0], self.cube[1][1][1]) = (self.cube[4][1][1], self.cube[4][0][1],
                                                   self.cube[2][0][0], self.cube[2][0][1],
                                                   self.cube[5][1][0], self.cube[5][0][0],
                                                   self.cube[0][1][0], self.cube[0][1][1],
                                                   self.cube[1][1][0], self.cube[1][0][0],
                                                   self.cube[1][1][1], self.cube[1][0][1])

    def move_front_anti_clockwise(self):
        """Rotates the front face of the cube anti-clockwise."""
        self.move_front_clockwise()
        self.move_front_clockwise()
        self.move_front_clockwise()

    def move_back_clockwise(self):
        """Rotates the back face of the cube clockwise."""
        (self.cube[0][0][0], self.cube[0][0][1],
         self.cube[4][0][0], self.cube[4][1][0],
         self.cube[2][1][0], self.cube[2][1][1],
         self.cube[5][0][1], self.cube[5][1][1],
         self.cube[3][0][0], self.cube[3][0][1],
         self.cube[3][1][0], self.cube[3][1][1]) = (self.cube[4][1][0], self.cube[4][0][0],
                                                   self.cube[2][1][0], self.cube[2][1][1],
                                                   self.cube[5][1][1], self.cube[5][0][1],
                                                   self.cube[0][0][0], self.cube[0][0][1],
                                                   self.cube[3][0][1], self.cube[3][1][1],
                                                   self.cube[3][0][0], self.cube[3][1][0])

    def move_back_anti_clockwise(self):
        """Rotates the back face of the cube anti-clockwise."""
        self.move_back_clockwise()
        self.move_back_clockwise()
        self.move_back_clockwise()
