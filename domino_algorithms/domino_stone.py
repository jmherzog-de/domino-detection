

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

    def __init__(self, center_x: float = 0.0, center_y: float = 0.0, length: float = 0.0, width: float = 0.0, height: float = 0.0, angle_deg: float = 0.0, center_line_p1_x: float = 0.0, center_line_p1_y: float = 0.0, center_line_p2_x: float = 0.0, center_line_p2_y: float = 0.0) -> None:
        self.Center         = Point(center_x, center_y)
        self.CenterLine_P1  = Point(center_line_p1_x, center_line_p1_y)
        self.CenterLine_P2  = Point(center_line_p2_x, center_line_p2_y)
        self.CenterRight    = Point(0.0, 0.0)
        self.CenterLeft     = Point(0.0, 0.0)
        self.StoneEdges     = [Point(0.0, 0.0), Point(0.0, 0.0), Point(0.0, 0.0), Point(0.0, 0.0)]
        self.Length         = length
        self.Height         = height
        self.Width          = width
        self.Angle          = angle_deg
        self.ROI_Left       = ROI()
        self.ROI_Right      = ROI()
        self.Eyes_Left      = list()
        self.Eyes_Right     = list()
        self.EyeVal_Right   = 0
        self.EyeVal_Left    = 0