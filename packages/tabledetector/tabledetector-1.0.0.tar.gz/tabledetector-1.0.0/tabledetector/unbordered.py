import cv2
import numpy as np
from PIL import Image, ImageStat
Image.MAX_IMAGE_PIXELS = None
import os

class UnborderedTableDetector:
    def __init__(self, imgPath):
        self.imgPath = imgPath

    @staticmethod
    def isColorImage(numpy_image, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
        pil_img = Image.fromarray(np.uint8(numpy_image)).convert('RGB')
        bands = pil_img.getbands()
        if bands == ('R','G','B') or bands== ('R','G','B','A'):
            thumb = pil_img.resize((thumb_size,thumb_size))
            SSE, bias = 0, [0,0,0]
            if adjust_color_bias:
                bias = ImageStat.Stat(thumb).mean[:3]
                bias = [b - sum(bias)/3 for b in bias ]
            for pixel in thumb.getdata():
                mu = sum(pixel)/3
                SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
            MSE = float(SSE)/(thumb_size*thumb_size)
            
            if MSE <= MSE_cutoff:
                return False, MSE
            else:
                return True, MSE
        elif len(bands)==1:
            return False, MSE
        else:
            return False, MSE

    @staticmethod
    def isLineLntersectingBox(startPoint, endPoint, box):
        x, y, w, h = box
        rect1 = [(startPoint[0], startPoint[1]), (endPoint[0], endPoint[1])]
        rect2 = [(x, y), (x + w, y + h)]

        if (rect1[0][0] > rect2[1][0] or rect1[1][0] < rect2[0][0] or
            rect1[0][1] > rect2[1][1] or rect1[1][1] < rect2[0][1]):
            return False
        else:
            return True

    @staticmethod
    def omitLines(img):
        
        res = img.copy()
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        vKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        rmVertical = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, vKernel, iterations=2)

        hKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        rmHorizontal = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, hKernel, iterations=2)

        cnts = cv2.findContours(rmVertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        cnts1 = cv2.findContours(rmHorizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = cnts1[0] if len(cnts1) == 2 else cnts1[1]

        for c in cnts:
            cv2.drawContours(res, [c], -1, (255,255,255), 12)

        for c1 in cnts1:
            cv2.drawContours(res, [c1], -1, (255,255,255), 12)
        
        return res

    @staticmethod
    def filterBoxes(boxes, table_width, limit=100):

        widthThreshold=table_width*.05
        return [box for box in boxes if (abs(box[2] - table_width*.75) > widthThreshold) and round(abs(box[2] - table_width) > limit)]

    def imageProcess(self):
        cvImg = cv2.imread(self.imgPath)
        colored, MSE = self.isColorImage(cvImg)
        if colored == False:
            cvImg = self.omitLines(cvImg)
        res = cvImg.copy()
        grayImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = np.ones((5, 80), np.uint8)
        dilateImg = cv2.dilate(thresh, kernel, iterations=1)
        contours = cv2.findContours(dilateImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        allBoxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if h > 20:
                x, y, w, h = x, y - 2, w, h + 4
                allBoxes.append([x, y, w, h])

        x_min = [min([box[0] - 5 for box in allBoxes]), min([box[1] - 5 for box in allBoxes])]
        y_max = [max([box[0] + box[2] + 5 for box in allBoxes]), max([box[1] + box[3] + 5 for box in allBoxes])]
        w_table = y_max[0] - x_min[0]
        
        filterd_boxes = self.filterBoxes(allBoxes, w_table)

        x_min_new = [min([box[0] - 5 for box in filterd_boxes]), min([box[1] - 5 for box in filterd_boxes])]
        y_max_new = [max([box[0] + box[2] + 5 for box in filterd_boxes]), max([box[1] + box[3] + 5 for box in filterd_boxes])]

        tableArea = x_min_new + y_max_new
        x1, y1, w1, h1 = tableArea
        cv2.rectangle(res, (x1, y1), (w1, h1), (0, 0, 0), 4)

        x_new = x_min_new[0]
        y_new = x_min_new[1]
        w_new = y_max_new[0] - x_min_new[0]
        h_new = y_max_new[1] - x_min_new[1]
        
        rowBoxes = filterd_boxes.copy()
        remainRowBoxes = []
        columnBoxes = filterd_boxes.copy()
        remainColBoxes = []

        while columnBoxes:

            min_x = min(colBox[0] for colBox in columnBoxes)
            minSublistCol = next(colBox for colBox in columnBoxes if colBox[0] == min_x)

            startPointCol = (minSublistCol[0]+ 2 + minSublistCol[2], y_new)
            endPointCol = (minSublistCol[0] + minSublistCol[2]+ 2, y_new + h_new)

            isIntersectCol = any(self.isLineLntersectingBox(startPointCol, endPointCol, colBox) for colBox in filterd_boxes)
            if not isIntersectCol:
                cv2.line(res, startPointCol, endPointCol, (0, 0, 0), 4)
                remainColBoxes.append(minSublistCol)
            columnBoxes.remove(minSublistCol)

        while rowBoxes:
            max_y = max(rowBox[1] + rowBox[3] for rowBox in rowBoxes)
            minSublistRow = next(rowBox for rowBox in rowBoxes if rowBox[1] + rowBox[3] == max_y)

            startPointRow = (x_new, minSublistRow[1] + minSublistRow[3] + 2)
            end_point_row = (x_new + w_new, minSublistRow[1] + minSublistRow[3] + 2)

            isIntersectRow = any(self.isLineLntersectingBox(startPointRow, end_point_row, rowBox) for rowBox in filterd_boxes)
            if not isIntersectRow:
                cv2.line(res, startPointRow, end_point_row, (0, 0, 0), 4)
                remainRowBoxes.append(minSublistRow)
            rowBoxes.remove(minSublistRow)

        cv2.imwrite(self.imgPath, res)

        return self.imgPath
    

    @staticmethod
    def sortContours(cnts, method='left-to-right'):

        reverse = False
        i = 0
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                            key=lambda b: b[1][i], reverse=reverse))
        
        return (cnts, boundingBoxes)


    def getProperTable(self, img):

        tableData = []
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        threshImg = 255 - threshImg
        kernel = np.ones((5,191), np.uint8)
        morphImg = cv2.morphologyEx(threshImg, cv2.MORPH_CLOSE, kernel)
        contours = cv2.findContours(morphImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        contours, boundingBoxes = self.sortContours(contours, method='top-to-bottom')
        res = img.copy()
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (h>300):
                image = cv2.rectangle(res, (x,y), (x+w, y+h), (0,0,0), 12)
                tableData.append((x, y, w, h))
        
        return image, tableData
    
    @staticmethod
    def drawLines(img):
        
        res = img.copy()
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        threshImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        vKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        rmVertical = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, vKernel, iterations=2)

        hKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        rmHorizontal = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, hKernel, iterations=2)

        cnts = cv2.findContours(rmVertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        cnts1 = cv2.findContours(rmHorizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = cnts1[0] if len(cnts1) == 2 else cnts1[1]

        for c in cnts:
            cv2.drawContours(res, [c], -1, (0,0,0), 4)

        for c1 in cnts1:
            cv2.drawContours(res, [c1], -1, (0,0,0), 4)
        
        return res
    
    @staticmethod
    def preProcess(img):
        
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh, imgBin = cv2.threshold(grayImg, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        imgBin = 255 - imgBin

        return imgBin

    @staticmethod
    def verticalLineDetect(invertedImg):

        kernel_len = np.array(invertedImg).shape[1] // 100
        vKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        vLines = cv2.dilate(cv2.erode(invertedImg, vKernel, iterations=3), vKernel, iterations=3)

        return vLines

    @staticmethod
    def horizonalLineDetect(invertedImg):
    
        kernel_len = np.array(invertedImg).shape[1] // 100
        hKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        hLines = cv2.dilate(cv2.erode(invertedImg, hKernel, iterations=3), hKernel, iterations=3)

        return hLines
    
    @staticmethod
    def combineLines(img, vLines, hLines):

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        imgVH = cv2.addWeighted(vLines, 0.5, hLines, 0.5, 0.0)
        thresh, imgVH = cv2.threshold(imgVH, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # bitNOT = cv2.bitwise_not(cv2.bitwise_xor(grayImg, imgVH))
        
        return imgVH

    def getBboxDtls(self, img, imgVH, tableDtls, imgPath):
        
        contours, hierarchy = cv2.findContours(imgVH, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, boundingBoxes = self.sortContours(contours, method="top-to-bottom")

        boxes = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (h>30) and (h<500):
                boxes.append([x, y, w, h])

        bboxDtls = {}
        for tableBox1 in tableDtls:
            key = tableBox1
            values = []

            for tableBox2 in boxes:
                x2, y2, w2, h2 = tableBox2
                if tableBox1[0] <= x2 <= tableBox1[0] + tableBox1[2] and tableBox1[1] <= y2 <= tableBox1[1] + tableBox1[3]:
                    values.append(tableBox2)
            bboxDtls[key] = values
        
        for key, values in bboxDtls.items():
            x_tab, y_tab, w_tab, h_tab = key
            cv2.rectangle(img, (x_tab, y_tab), (x_tab + w_tab, y_tab + h_tab), (255, 0, 0), 8)
            for box in values:
                x_box, y_box, w_box, h_box = box
                cv2.rectangle(img, (x_box, y_box), (x_box + w_box, y_box + h_box), (0, 255, 0), 4)

        cv2.imwrite(imgPath.replace('_rotated.jpg','_detected.jpg'),img)

        return bboxDtls
    
    def unborderedMain(self):
        try:
            unborderedPath = self.imageProcess()
            cvImg = cv2.imread(unborderedPath)
            fileName = os.path.basename(self.imgPath).replace('_rotated.jpg', '')
            tableImg, tableRect = self.getProperTable(cvImg)
            tableImg = self.drawLines(tableImg)
            res = tableImg.copy()
            preImg = self.preProcess(tableImg)
            vLineImg = self.verticalLineDetect(preImg)
            hLineImg = self.horizonalLineDetect(preImg)
            combineLineImg = self.combineLines(res, vLineImg, hLineImg)
            bboxDtls = self.getBboxDtls(tableImg, combineLineImg, tableRect, self.imgPath)
        except Exception as e:
            print(e)
            bboxDtls, fileName, res = [], fileName, None

        return bboxDtls, fileName, res