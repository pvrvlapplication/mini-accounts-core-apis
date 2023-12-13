from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue, black
from reportlab.lib.units import inch


class PDFGenarator():
    def __init__(self, fileName, font, fontColor):
        self.canvas = Canvas(fileName, pagesize=A4)
        self.font = font
        self.fontColor = fontColor

    def setFont(self):
        self.canvas.setFont(self.font if self.font else "Times-Roman", 12)

    def setFillColor(self):
        self.canvas.setFillColor(self.fontColor if self.fontColor else black)

    def drawString(self):
        pass

    def save(self):
        self.setFont()
        self.setFillColor()
        self.drawString()
        self.canvas.save()


class SaleReportGenerator(PDFGenarator):
    """This class is used to generate PDF Report for sale bills."""

    def __init__(self):
        PDFGenarator.__init__(self, "SaleReport.pdf", "Times-Roman", "black")

    def drawString(self):
        self.canvas.drawString(1 * inch, 10 * inch, "Sale Report.")