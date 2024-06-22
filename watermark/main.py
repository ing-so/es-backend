import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfWriter, PdfReader

def create_qr_code_with_url(url, output_file):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(output_file)

def add_qr_to_pdf(input_pdf_path, output_pdf_path, qr_code_path):
    # Read the existing PDF
    input_pdf = PdfReader(open(input_pdf_path, "rb"))
    output_pdf = PdfWriter()

    qr_pdf_path = "temp_qr.pdf"
    c = canvas.Canvas(qr_pdf_path, pagesize=letter)
    
    # QR 코드 크기 및 위치 조정
    qr_code_size = 120  # QR 코드 크기 (너비와 높이)
    x_position = 420  # x 좌표 (좌측으로부터의 거리)
    y_position = 680  # y 좌표 (하단으로부터의 거리)
    
    c.drawImage(qr_code_path, x_position, y_position, width=qr_code_size, height=qr_code_size)
    c.save()

    qr_pdf = PdfReader(open(qr_pdf_path, "rb"))
    qr_page = qr_pdf.pages[0]

    # Add QR code to each page
    for i in range(len(input_pdf.pages)):
        page = input_pdf.pages[i]
        page.merge_page(qr_page)
        output_pdf.add_page(page)

    # Write the modified PDF to a file
    with open(output_pdf_path, "wb") as outputStream:
        output_pdf.write(outputStream)

# 경로를 여러분의 파일 경로로 변경하세요.
input_pdf_path = "/Users/sin-yunsig/epson/watermark/epson_scan.pdf"
output_pdf_path = "/Users/sin-yunsig/epson/watermark/out.pdf"
qr_code_path = "qr_code.png"  # QR 코드를 일시적으로 저장할 파일 경로

# QR 코드에 삽입할 이미지 URL을 지정하세요.
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTyneHDnNSk-r7ekZR4Qdhf1Nq7dsdOd3c7w&s"
create_qr_code_with_url(image_url, qr_code_path)
add_qr_to_pdf(input_pdf_path, output_pdf_path, qr_code_path)
