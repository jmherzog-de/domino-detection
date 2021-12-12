import cv2
import numpy as np

from domino_algorithms.stone_processing import StoneProcessing

class StoneProjection:

    @staticmethod
    def DrawStone(cvOutputImage: np.ndarray, stones: list):
        
        for stone in stones:

            # Draw Center line
            cv2.line(cvOutputImage, pt1=(stone.CenterLine_P1.X, stone.CenterLine_P1.Y), pt2=(stone.CenterLine_P2.X, stone.CenterLine_P2.Y), color=(255, 255, 255), thickness=3)
            
            # Draw Box
            p0 = (np.int32(stone.StoneEdges[0].X), np.int32(stone.StoneEdges[0].Y))
            p1 = (np.int32(stone.StoneEdges[1].X), np.int32(stone.StoneEdges[1].Y))
            p2 = (np.int32(stone.StoneEdges[2].X), np.int32(stone.StoneEdges[2].Y))
            p3 = (np.int32(stone.StoneEdges[3].X), np.int32(stone.StoneEdges[3].Y))

            cv2.circle(cvOutputImage, center=p0, radius=3, color=(0,0,255), thickness=3)
            cv2.circle(cvOutputImage, center=p1, radius=3, color=(0,0,255), thickness=3)
            cv2.circle(cvOutputImage, center=p2, radius=3, color=(0,0,255), thickness=3)
            cv2.circle(cvOutputImage, center=p3, radius=3, color=(0,0,255), thickness=3)

            cv2.line(cvOutputImage, pt1=p0, pt2=p1, color=(255,255,255), thickness=2)
            cv2.line(cvOutputImage, pt1=p0, pt2=p2, color=(255,255,255), thickness=2)
            cv2.line(cvOutputImage, pt1=p2, pt2=p3, color=(255,255,255), thickness=2)
            cv2.line(cvOutputImage, pt1=p3, pt2=p1, color=(255,255,255), thickness=2)

            cv2.putText(cvOutputImage, str(stone.EyeVal_Left), org=(np.int32(stone.CenterLeft.X), np.int32(stone.CenterLeft.Y)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(255, 255, 255), fontScale=1, thickness=2)
            cv2.putText(cvOutputImage, str(stone.EyeVal_Right), org=(np.int32(stone.CenterRight.X), np.int32(stone.CenterRight.Y)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(255, 255, 255), fontScale=1, thickness=2)

            StoneProcessing.StoneDistances(cvOutputImage, stones)