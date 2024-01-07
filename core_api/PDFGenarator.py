from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import blue, black
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


class PDFGenarator():
    def __init__(self, fileName, font, fontColor):
        self.buffer=BytesIO()
        self.canvas = Canvas(self.buffer, pagesize=A4)
        self.font = font
        self.fontColor = fontColor

    def setFont(self, fontName=None, fontSize=None):
        self.canvas.setFont(self.font if self.font else fontName if fontName else "Times-Roman", fontSize if fontSize else 12)

    def setFillColor(self):
        self.canvas.setFillColor(self.fontColor if self.fontColor else black)

    def drawString(self):
        pass

    def save(self):
        self.setFont()
        self.setFillColor()
        self.drawString()
        self.canvas.showPage()
        self.canvas.save()
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf


class SaleReportGenerator(PDFGenarator):
    """This class is used to generate PDF Report for sale bills."""

    def __init__(self, saleData, request):
        self.saleData = saleData.data
        self.company = request.user.company
        # {'id': 1, 'party_name': 'test', 'date': 'Dec/09/2023, 14:51', 'comment': 'testing', 'gst_type': 'I', 'invoice_no': '1122554477', 'party': 1, 'address': 2, 'shipping_address': 2, 
        #  'sale_items': [
        #      {'id': 1, 'product_name': 'Iron', 'price': '150.00', 'quantity': '100.00', 'sgst': '375.00', 'cgst': '375.00', 'igst': '0.00', 'taxble_value': '15000.00', 'invoice_value': '15000.00', 'sale': 1, 'product': 1}
        #      ], 
        # 'taxble_value': 15000.0, 
        # 'invoice_value': 15000.0}
        PDFGenarator.__init__(self, "SaleReport.pdf", "Helvetica", "black")

    def drawHeader(self):
        self.setFont(fontSize=18)
        self.canvas.drawCentredString(4.25 * inch, 800, "Sale Invoice")

    def companyDetails(self):
        self.setFont(fontSize=15)
        self.canvas.drawString(0.5 * inch, 10.5 * inch, self.company.name)
        self.setFont(fontSize=13)
        self.canvas.drawString(0.5 * inch, 10.3 * inch, "{dno}, {area}, {city},".format(dno=self.company.dno, area=self.company.area, city=self.company.city) )
        self.canvas.drawString(0.5 * inch, 10.1 * inch, "{district}, {state}, {country},".format(district=self.company.district, state=self.company.state, country=self.company.country))
        self.canvas.drawString(0.5 * inch, 9.9 * inch, "{mobile}, {phone}.".format(mobile=self.company.mobile, phone=self.company.phone))
        self.canvas.drawString(6 * inch, 10.1 * inch, "Invoice No: "+self.saleData.get('invoice_no'))
        self.canvas.drawString(6 * inch, 10.3 * inch, "Date: "+self.saleData.get('date'))

    def drawSaleInvoiceData(self):
        self.setFont(fontSize=12)
        self.canvas.drawString(0.5 * inch, 9.3 * inch, "Party name: "+self.saleData.get('party_name'))
        self.canvas.drawString(0.5 * inch, 9.1 * inch, "GST type: "+self.saleData.get('gst_type'))

    def drawProductsData(self):
        self.setFont(fontSize=12)
        data = []
        headers = list(self.saleData.get('sale_items')[0].keys())
        headers.remove('id')
        headers.remove('product')
        headers.remove('sale')
        data.append(headers)
        for product in self.saleData.get('sale_items'):
            product.pop('id')
            product.pop('product')
            product.pop('sale')
            d = list(product.values())
            data.append(d)
        width = 1800
        height = 200
        x = 1 * inch
        y = 8 * inch
        t=Table(data)
        t.wrapOn(self.canvas, width, height)
        t.drawOn(self.canvas, x, y)

    def drawString(self):
        self.drawHeader()
        self.companyDetails()
        self.drawSaleInvoiceData()
        self.drawProductsData()      



class PurchaseReportGenerator(PDFGenarator):
    """This class is used to generate PDF Report for sale bills."""

    def __init__(self, purchaseData):
        self.purchaseData = purchaseData.data
        # {'id': 1, 'party_name': 'test', 'date': 'Dec/09/2023, 14:51', 'comment': 'testing', 'gst_type': 'I', 'invoice_no': '1122554477', 'party': 1, 'address': 2, 'shipping_address': 2, 
        #  'purchase_items': [
        #      {'id': 1, 'product_name': 'Iron', 'price': '150.00', 'quantity': '100.00', 'sgst': '375.00', 'cgst': '375.00', 'igst': '0.00', 'taxble_value': '15000.00', 'invoice_value': '15000.00', 'sale': 1, 'product': 1}
        #      ], 
        # 'taxble_value': 15000.0, 
        # 'invoice_value': 15000.0}
        PDFGenarator.__init__(self, "PurchaseReport.pdf", "Times-Roman", "black")

    def drawHeader(self):
        self.setFont(fontSize=18)
        self.canvas.drawCentredString(4.25 * inch, 800, "Purchase Invoice")

    def companyDetails(self):
        self.setFont(fontSize=15)
        self.canvas.drawString(0.5 * inch, 10.5 * inch, self.company.name)
        self.setFont(fontSize=13)
        self.canvas.drawString(0.5 * inch, 10.3 * inch, "{dno}, {area}, {city},".format(dno=self.company.dno, area=self.company.area, city=self.company.city) )
        self.canvas.drawString(0.5 * inch, 10.1 * inch, "{district}, {state}, {country},".format(district=self.company.district, state=self.company.state, country=self.company.country))
        self.canvas.drawString(0.5 * inch, 9.9 * inch, "{mobile}, {phone}.".format(mobile=self.company.mobile, phone=self.company.phone))
        self.canvas.drawString(6 * inch, 10.1 * inch, "Invoice No: "+self.saleData.get('invoice_no'))
        self.canvas.drawString(6 * inch, 10.3 * inch, "Date: "+self.saleData.get('date'))

    def drawPurchaseInvoiceData(self):
        self.setFont(fontSize=12)
        self.canvas.drawString(1 * inch, 9.4 * inch, "Party name: "+self.purchaseData.get('vendor_name'))
        self.canvas.drawString(1 * inch, 9.1 * inch, "GST type: "+self.purchaseData.get('gst_type'))

    def drawProductsData(self):
        data = []
        headers = list(self.purchaseData.get('purchase_items')[0].keys())
        headers.remove('id')
        headers.remove('product')
        headers.remove('purchase')
        data.append(headers)
        for product in self.purchaseData.get('purchase_items'):
            product.pop('id')
            product.pop('product')
            product.pop('purchase')
            d = list(product.values())
            data.append(d)
        width = 1200
        height = 200
        x = 1 * inch
        y = 8 * inch
        t=Table(data)
        t.wrapOn(self.canvas, width, height)
        t.drawOn(self.canvas, x, y)

    def drawString(self):
        self.drawHeader()
        self.companyDetails()
        self.drawPurchaseInvoiceData()
        self.drawProductsData()      