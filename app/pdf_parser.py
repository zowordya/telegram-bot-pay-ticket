# pdf_parser.py
import PyPDF2


def extract_text_from_pdf(file_path):
    """Извлекает текст из PDF файла."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'  # Добавляем новую строку после каждой страницы
    return text


def get_line_from_text(text, line_number):
    """Возвращает строку по указанному номеру."""
    lines = text.split('\n')
    # Проверяем, существует ли строка с указанным номером
    if line_number <= len(lines):
        return lines[line_number - 1]  # -1, потому что индексация начинается с 0
    else:
        return "Строка не существует."
