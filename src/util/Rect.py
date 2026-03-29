class Rect:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @property
    def rect(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.width, self.height)
    
    @property
    def position(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)
    
    @property
    def bounds(self) -> tuple[int, int, int, int]:
        return (self.x, self.y, self.x + self.width, self.y + self.height)
    
    def __add__(self, other):
        x, y = other
        return Rect(
            self.x + x,
            self.y + y,
            self.width,
            self.height
        )
    
    def __repr__(self):
        return f"Rect(x={self.x}, y={self.y}, width={self.width}, height={self.height})"