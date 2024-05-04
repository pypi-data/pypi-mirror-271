import os, shutil
import cv2
import numpy as np
import easyocr
import pandas as pd
import concurrent.futures
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

from .convertor import PDFConverter
from .rotate import ImageRotator
from .bordered import BorderedTableDetector
from .unbordered import UnborderedTableDetector
from .semibordered import SemiborderedTableDetector
from .consolidated import ConsolidatedTableDetector
from .extractor import TableExtractor



class TableDetector:
    def __init__(self, pdfPath, method="consolidated"):
        self.pdfPath = pdfPath
        self.method = method

    def processImage(self, eachImgPath, ocrEngine):

        try:
            rotator = ImageRotator(eachImgPath)
            rotateImgPath = rotator.rotateMain()

            if self.method == "bordered":
                bordered = BorderedTableDetector(rotateImgPath)
                bboxDtls, filename, cvImg = bordered.borderedMain()

            elif self.method == "unbordered":
                unbordered = UnborderedTableDetector(rotateImgPath)
                bboxDtls, filename, cvImg = unbordered.unborderedMain()

            elif self.method == "semibordered":
                semibordered = SemiborderedTableDetector(rotateImgPath)
                bboxDtls, filename, cvImg = semibordered.semiborderedMain()
            
            else:
                consolidated = ConsolidatedTableDetector(rotateImgPath)
                bboxDtls, filename, cvImg = consolidated.consolidatedMain()
            
        except:
            bboxDtls, filename= [], filename

        if len(bboxDtls) != 0:
            extracts = TableExtractor(ocrEngine, bboxDtls, cvImg)
            dataFrames = extracts.extractorMain()
        else:
            dataFrames = pd.DataFrame()

        return dataFrames

    def main(self):
        
        self.outImgFolder = './Images'

        if not os.path.exists(self.outImgFolder):
            os.makedirs(self.outImgFolder)
        
        reader = easyocr.Reader(['en'], gpu=False)

        try:
            if self.pdfPath.endswith('.PDF') or self.pdfPath.endswith('.pdf'):
                imagePath = PDFConverter.generateImage(self.pdfPath, self.outImgFolder)

            elif self.pdfPath.endswith('.jpg') or self.pdfPath.endswith('.JPG') or self.pdfPath.endswith('.png') or self.pdfPath.endswith('.PNG') or \
                self.pdfPath.endswith('.jpeg') or self.pdfPath.endswith('.JPEG'):

                img = cv2.imread(self.pdfPath)
                imgFolderPath = os.path.basename(self.pdfPath).replace('.jpg','').replace('.JPG','').replace('.jpeg','').replace('.JPEG','') \
                                            .replace('.png','').replace('.PNG','')
                if not os.path.exists(imgFolderPath):
                    os.makedirs(self.outImgFolder+"/"+imgFolderPath)
                
                cv2.imwrite(self.outImgFolder+"/"+imgFolderPath+"/"+os.path.basename(self.pdfPath), img)
                imagePath = [self.outImgFolder+"/"+imgFolderPath+"/"+os.path.basename(self.pdfPath)]
            
            else:
                print("Unsupported format")

        except Exception as e:
            print(e)
            imagePath = []
        
        results = []
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(imagePath)) as executor:
                futures = [executor.submit(self.processImage, eachImgPath, reader) for eachImgPath in imagePath]
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    results.append(result)
        except:
            results = []
            
        try:
            shutil.rmtree(self.outImgFolder)
        except:
            pass

        return results