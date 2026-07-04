import pdfplumber

def extract_text_from_pdf(uploaded_file):

    if uploaded_file is None:
        return ""

    extracted_text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:

            if len(pdf.pages) == 0:
                return ""

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

        return extracted_text.strip()

    except Exception as e:
        print("PDF Parsing Error:", e)
        return ""