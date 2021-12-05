

class Point:

    def __init__(self, x: float, y: float) -> None:
        self.X = x
        self.Y = y

class ROI:

    def __init__(self) -> None:
        self.Line1  = [ Point(0.0, 0.0), Point(0.0, 0.0) ]
        self.Line2  = [ Point(0.0, 0.0), Point(0.0, 0.0) ]
        self.Line3  = [ Point(0.0, 0.0), Point(0.0, 0.0) ]

class DominoStone:

    def __init__(self, center_x: float = 0.0, center_y: float = 0.0, length: float = 0.0, width: float = 0.0, height: float = 0.0, angle_deg: float = 0.0) -> None:
        self.Center     = Point(center_x, center_y)
        self.Length     = length
        self.Height     = height
        self.Width      = width
        self.Angle      = angle_deg
        self.ROI_Left   = ROI()
        self.ROI_Right  = ROI()
        self.Eyes       = list()