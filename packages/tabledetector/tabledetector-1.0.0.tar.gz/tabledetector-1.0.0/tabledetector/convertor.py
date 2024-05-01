import os, glob
from pdf2image import convert_from_path

class PDFConverter:
    def __init__(self, pdfFile, imageDir):
        self.pdfFile = pdfFile
        self.imageDir = imageDir

    def generateImage(pdfFile, imageDir):
        imgPaths = []
        pdfImgPath = os.path.join(imageDir, os.path.basename(pdfFile).replace('.pdf', '').replace('.PDF', ''))
        
        if not os.path.exists(pdfImgPath):
            os.makedirs(pdfImgPath)

        pdfImages = convert_from_path(pdfFile, dpi=500)
        imgName = os.path.basename(pdfFile).replace('.pdf', '').replace('.PDF', '')

        for i, img in enumerate(pdfImages):
            imgPath = os.path.join(pdfImgPath, f'{imgName}_page{i}.jpg')
            img.save(imgPath, 'JPEG')
            imgPaths.append(imgPath)

        return imgPaths