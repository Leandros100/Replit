from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
import io

def modify_pdf(protocolo_cliente):
    pdf_path = 'Manual de Instalação do Certificado A1 - Identité (4).pdf'
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    pagina_alvo = 0
    data = {'Número do Protocolo': [protocolo_cliente]}
    df = pd.DataFrame(data)

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]

        if page_num == pagina_alvo:
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=letter)
            c.setFont("Helvetica", 20)
            c.drawString(129, 660, df['Número do Protocolo'].iloc[0])
            c.save()

            packet.seek(0)
            overlay_pdf = PdfReader(packet)
            page2 = overlay_pdf.pages[0]
            page.merge_page(page2)

        pdf_writer.add_page(page)

    output_pdf_path = 'ficha_de_inscricao_preenchida.pdf'

    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    return output_pdf_path

def main():
    protocolo_cliente = input('Enter the protocolo: ')

    if not protocolo_cliente:
        print('Please provide a protocolo parameter.')
        return

    output_pdf_path = modify_pdf(protocolo_cliente)
    print(f'Modified PDF saved at: {output_pdf_path}')

    # Generate a direct download link
    download_link = f'<a href="{output_pdf_path}" download>Download Modified PDF</a>'
    print(f'Copy and paste the following link in your browser to download the modified PDF:\n{download_link}')

if __name__ == '__main__':
    main()
