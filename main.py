from flask import Flask, request, redirect, url_for, flash, render_template
import qrcode
import pyotp
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = "2factorauth"

# Generate a random base32 key
key_gen = pyotp.random_base32()
totp = pyotp.TOTP(key_gen)

# Generate a QR code for the provisioning URI
qr = totp.provisioning_uri(name="2fa", issuer_name="Hareshwhar")
print(f"URI: {qr}")

qr_image = qrcode.make(qr)
buffer = BytesIO()
qr_image.save(buffer)
qr_data = base64.b64encode(buffer.getvalue()).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        otp = request.form['otp']
        if totp.verify(otp):
            flash("OTP is Correct", "success")
            return redirect(url_for('success'))
        else:
            flash("Invalid OTP", "danger")

    return render_template('index.html', qr_data=qr_data)

# Ensure this route is correctly defined and not inside another function or class
@app.route('/success')
def success():
    return "OTP verified successfully!"

if __name__ == '__main__':
    app.run(debug=True)
