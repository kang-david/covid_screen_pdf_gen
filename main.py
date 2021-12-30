from fpdf import FPDF
from PIL import Image

def create_pdf(user_logo_file, qr_code_file):

    # Create FPDF object
    pdf = FPDF('P', 'mm', 'Letter')

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font('helvetica', 'B', 28)

    # Add page border
    pdf.set_line_width(2)
    pdf.line(x1=10, y1=10, x2=pdf.w-10, y2=10)
    pdf.line(x1=pdf.w-10, y1=10, x2=pdf.w-10, y2=pdf.h-10)
    pdf.line(x1=pdf.w-10, y1=pdf.h-10, x2=10, y2=pdf.h-10)
    pdf.line(x1=10, y1=pdf.h-10, x2=10, y2=10)

    # Add user-uploaded logo
    pixels_to_mm = 0.79375 / 3
    user_logo = Image.open(user_logo_file)
    max_width_pixels = (pdf.w-40)/pixels_to_mm

    if round(200*(user_logo.width/user_logo.height)) < max_width_pixels:
        height_pixels = 200
        user_logo = user_logo.resize((
            round(200*(user_logo.width/user_logo.height)),
            height_pixels
        ))
    else:
        height_pixels = round(max_width_pixels*(user_logo.height/user_logo.width))
        user_logo = user_logo.resize((
            round((pdf.w-40)/pixels_to_mm),
            height_pixels
        ))

    pdf.image(
        user_logo,
        x=(pdf.w/2)-(user_logo.width*pixels_to_mm/2),
        y=20,
        h=height_pixels*pixels_to_mm
    )

    # Add QR code
    qr_code = Image.open(qr_code_file)
    pdf.image(
        qr_code,
        x=(pdf.w/2)-40,
        y=80, w=80,
        h=80
    )

    # Add text
    text_lines = [
        'SCAN THE CODE',
        'PROVIDE CONTACT INFO',
        'ENTER & STAY SAFE',
    ]
    pdf.multi_cell(0, 160, '', align='C', ln=True)
    for line in text_lines:
        pdf.multi_cell(0, 15, line, align='C', ln=1)

    # Add Canatrace logo
    canatrace_logo = Image.open('images/canatracelogo.png')
    canatrace_logo = canatrace_logo.resize((401, 92))
    pdf.image(
        canatrace_logo,
        x=(pdf.w/2)-(canatrace_logo.width*pixels_to_mm/2),
        y=230,
        h=canatrace_logo.height*pixels_to_mm
    )

    # Create output file
    pdf.output('output.pdf')



create_pdf('images/userlogo.png', 'images/qrcode.png')