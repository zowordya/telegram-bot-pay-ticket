import PyPDF2


def extract_text_from_pdf(file_path):
    """Извлекает текст из PDF файла."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n' 
    return text


def get_line_from_text(text, line_number):
    """Возвращает строку по указанному номеру."""
    lines = text.split('\n')
    if line_number <= len(lines):
        return lines[line_number - 1]
    else:
        return "Строка не существует."
