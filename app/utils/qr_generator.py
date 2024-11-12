import qrcode

def generate_qr(text):
    qr = qrcode.make(text)
    qr_path = "qr_code.png"
    qr.save(qr_path)
    return qr_path
