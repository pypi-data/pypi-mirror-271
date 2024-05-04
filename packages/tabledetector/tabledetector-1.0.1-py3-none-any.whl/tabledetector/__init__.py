from .tabledetector import TableDetector

def detect(pdfPath, method="consolidated"):
    detector = TableDetector(pdfPath, method)
    return detector.main()