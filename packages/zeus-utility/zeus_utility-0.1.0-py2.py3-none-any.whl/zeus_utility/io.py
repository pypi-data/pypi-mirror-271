import json

def read_txt(file_path):
    with open(file_path, 'r',encoding="utf-8") as f:
        return f.read()
def write_txt(file_path, data):
    with open(file_path, 'w',encoding="utf-8") as f:
        f.write(data)
def read_json(file_path):
    with open(file_path, 'r',encoding="utf-8") as f:
        return json.load(f)
def write_json(file_path, data):
    with open(file_path, 'w',encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii=False, indent=4)
def read_pdf(file_path):
    from pypdf import PdfReader
    pdf = PdfReader(file_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text