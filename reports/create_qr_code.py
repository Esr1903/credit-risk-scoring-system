import qrcode
from pathlib import Path

app_url = "https://credit-risk-scoring-system-ypf2wbhqkzm5gtvmspkpm7.streamlit.app/"

output_path = Path(__file__).resolve().parent / "streamlit_app_qr.png"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

qr.add_data(app_url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save(output_path)

print(f"QR kod oluşturuldu: {output_path}")