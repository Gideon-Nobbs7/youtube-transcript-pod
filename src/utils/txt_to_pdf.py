from io import BytesIO

from fpdf import FPDF


def generate_pdf_bytes(transcript_text: str) -> BytesIO:
    """ "
    Create a pdf version of the transcript and store it in memory
    Args:
        transcript_text: a youtbe video's transcript
    Returns:
        Transcript pdf stored in memory
    """

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in transcript_text.splitlines():
        pdf.multi_cell(0, 10, line)

    pdf_output = pdf.output(dest="S").encode("latin1")
    return BytesIO(pdf_output)
