import cv2
import numpy as np
from scipy.ndimage import interpolation as inter

class ImageRotator:
    def __init__(self, imagePath):
        self.imagePath = imagePath

    def findScore(self, arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        hist = np.sum(data, axis=1)
        score = np.sum((hist[1:] - hist[:-1]) ** 2)
        return hist, score

    def findNormalRotation(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ht, wd = img.shape[:2]
        pix = ~img
        binImg = 1 - (pix.reshape((ht, wd)) / 255.0)
        delta = 0.5
        limit = 6
        angles = np.arange(-limit, limit + delta, delta)
        scores = []
        for angle in angles:
            hist, score = self.findScore(binImg, angle)
            scores.append(score)

        bestScore = max(scores)
        bestAngle = angles[scores.index(bestScore)]
        return bestAngle

    def rotateImage(self, img, angle):
        h, w = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def alignImage(self):
        cvImage = cv2.imread(self.imagePath)
        res = cvImage.copy()
        normRotation = self.findNormalRotation(cvImage)
        rotatedImage = self.rotateImage(res, normRotation)
        return rotatedImage

    def rotateMain(self):
        correctedImage = self.alignImage()
        rotatePath = self.imagePath.replace('.jpg', '_rotated.jpg')
        cv2.imwrite(rotatePath, correctedImage)
        return rotatePath