import cv2
import numpy as np

from domino_algorithms.stone_processing import StoneProcessing

class StoneProjection:

    @staticmethod
    def DrawStone(cvOutputImage: np.ndarray, stones: list):
        """
        Draw projected stone on the output image.
        Stone get's colored either white, green or red.

        :param cvOutputImage: OpenCV output image.
        :type cvOutputImage: np.ndarray
        :param stones: List of all DominoStone objects to draw on image.
        :type stones: list
        """
        
        # find matching stones
        StoneProcessing.StoneMaches(stones)

        for stone in stones:
            
            # This ignore all stones which don't have a Eye Value.
            # Maybe the program detect a center line where no center line is
            if stone.EyeVal_Left == None and stone.EyeVal_Right == None:
                continue
            
            #
            # white: stone detected but not connected with another stone.
            # green: stone connected correctly.
            # red: stone connected incorrectly.
            stone_color = (255, 255, 255)
            for item in stone.Connected_Stones:
                if item['valid'] == False:
                    stone_color = (255, 0, 0)
                    break
                else:
                    stone_color = (0, 255, 0)


            # Draw Center line
            cv2.line(cvOutputImage, pt1=(stone.CenterLine_P1.X, stone.CenterLine_P1.Y), pt2=(stone.CenterLine_P2.X, stone.CenterLine_P2.Y), color=stone_color, thickness=3)
            
            # Calculate domino-stone edge points
            p0 = (np.int32(stone.StoneEdges[0].X), np.int32(stone.StoneEdges[0].Y))
            p1 = (np.int32(stone.StoneEdges[1].X), np.int32(stone.StoneEdges[1].Y))
            p2 = (np.int32(stone.StoneEdges[2].X), np.int32(stone.StoneEdges[2].Y))
            p3 = (np.int32(stone.StoneEdges[3].X), np.int32(stone.StoneEdges[3].Y))

            # draw the domino-stone
            cv2.line(cvOutputImage, pt1=p0, pt2=p1, color=stone_color, thickness=2)
            cv2.line(cvOutputImage, pt1=p0, pt2=p2, color=stone_color, thickness=2)
            cv2.line(cvOutputImage, pt1=p2, pt2=p3, color=stone_color, thickness=2)
            cv2.line(cvOutputImage, pt1=p3, pt2=p1, color=stone_color, thickness=2)

            # write the detected eye value for each side into the stone.
            cv2.putText(cvOutputImage, str(stone.EyeVal_Left), org=(np.int32(stone.CenterLeft.X), np.int32(stone.CenterLeft.Y)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=stone_color, fontScale=1, thickness=2)
            cv2.putText(cvOutputImage, str(stone.EyeVal_Right), org=(np.int32(stone.CenterRight.X), np.int32(stone.CenterRight.Y)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=stone_color, fontScale=1, thickness=2)          