"""Contains objects used to build a Cube.js query"""

__ALL__ = ["Cube"]


class CubeObject:
    """Base class for objects defined in a cube.

    An instance of this object represents a *reference* to an object in a cube.js
    configuration.
    """

    def __init__(self, cube: "Cube", name: str) -> None:
        """Init

        Args:
            cube: Cube factory object
            name: Name of the cube object

        """
        self._cube = cube
        self.name = name

    def __eq__(self, o: object) -> bool:
        """Checks equality between CubeObject instances"""
        return (
            isinstance(o, self.__class__)
            and o._cube == self._cube
            and o.name == self.name
        )

    def __str__(self) -> str:
        """String representation of the CubeObject"""
        return f"{self._cube.name}.{self.name}"

    def serialize(self) -> str:
        """Serialize the object in order to send a query"""
        return str(self)


class Measure(CubeObject):
    """Measure reference"""

    pass


class Dimension(CubeObject):
    """Dimension reference"""

    pass


class Segment(CubeObject):
    """Segment reference"""

    pass


class Cube:
    """Factory that aliases object references with the correct cube name"""

    def __init__(self, name: str) -> None:
        """Initializer

        Args:
            name: Cube configuration name

        """
        self.name = name

    def __eq__(self, o: object) -> bool:
        """Checks equality between Cube objects"""
        return isinstance(o, self.__class__) and o.name == self.name

    def __repr__(self) -> str:
        """REPR representation"""
        return f'{self.__class__.__name__}(name="{self.name}")'

    def __str__(self) -> str:
        """String representation"""
        return self.name

    def measure(self, name: str) -> Measure:
        """Factory method for building a measure field reference

        Args:
            name: Measure name

        Returns:
            measure object reference

        """
        return Measure(self, name)

    def dimension(self, name: str) -> Dimension:
        """Factory method for building a dimension field reference

        Args:
            name: Dimension name

        Returns:
            dimension object reference

        """
        return Dimension(self, name)

    def segment(self, name: str) -> Segment:
        """Factory method for building a segment field reference

        Args:
            name: Segment name

        Returns:
            segment object reference

        """
        return Segment(self, name)
