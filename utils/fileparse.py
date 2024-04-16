import PyPDF2
from docx import Document
import pandas as pd

def read_file(file_path):
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'pdf':
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text

    elif file_extension in ['txt', 'text', 'csv']:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    elif file_extension in ['doc', 'docx']:
        doc = Document(file_path)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        return text

    elif file_extension in ['xls', 'xlsx']:
        df = pd.read_excel(file_path)
        return df.to_string(index=False)

    else:
        raise ValueError(f"Unsupported file type: {file_extension}")



# @app.route("/uploadfile",methods = ['POST'])
# def upload_file():
#     if request.method == 'POST':
#         uploaded_file = request.files['file']
#         if uploaded_file:
#             file_content = read_file(uploaded_file)
#             bucket = storage_client.bucket(bucket_name)
#             blob = bucket.blob(file_name)
#             blob.upload_from_string(content)
#             return 'File successfully uploaded to GCP bucket!'
#     return jsonify({"status":"success"})