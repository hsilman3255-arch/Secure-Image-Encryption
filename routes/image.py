from flask import Blueprint, render_template, request, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from crypto.aes import generate_key, encrypt_file, decrypt_file
from crypto.rsa import (
    generate_keys,
    encrypt_aes_key,
    decrypt_aes_key
)

import os
import secrets

image = Blueprint("image", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@image.route("/encrypt", methods=["GET", "POST"])
@login_required
def encrypt():

    if request.method == "POST":

        file = request.files["image"]

        if file.filename == "":
            return render_template(
                "encrypt.html",
                error="Select an image."
            )

        if allowed_file(file.filename):

            extension = file.filename.rsplit(".", 1)[1].lower()

            filename = f"{secrets.token_hex(16)}.{extension}"

            upload_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )

            encrypted_path = os.path.join(
                current_app.config["ENCRYPTED_FOLDER"],
                filename + ".enc"
            )

            key_folder = current_app.config["KEY_FOLDER"]

            file.save(upload_path)

            generate_keys(key_folder)

            aes_key = generate_key()

            encrypt_file(
                upload_path,
                encrypted_path,
                aes_key
            )

            encrypted_key = encrypt_aes_key(
                aes_key,
                key_folder
            )

            with open(
                os.path.join(
                    key_folder,
                    filename + ".enc.key"
                ),
                "wb"
            ) as f:
                f.write(encrypted_key)

            return render_template(
                "encrypt.html",
                uploaded_image=filename,
                encrypted_file=filename + ".enc"
            )

    return render_template("encrypt.html")


@image.route("/decrypt", methods=["GET", "POST"])
@login_required
def decrypt():

    if request.method == "POST":

        file = request.files["file"]

        if file.filename == "":
            return render_template(
                "decrypt.html",
                error="Select encrypted file."
            )

        filename = secure_filename(file.filename)

        encrypted_path = os.path.join(
            current_app.config["ENCRYPTED_FOLDER"],
            filename
        )

        file.save(encrypted_path)

        encrypted_key_path = os.path.join(
            current_app.config["KEY_FOLDER"],
            filename.replace(".enc", ".enc.key")
        )

        with open(encrypted_key_path, "rb") as f:
            encrypted_key = f.read()

        aes_key = decrypt_aes_key(
            encrypted_key,
            current_app.config["KEY_FOLDER"]
        )

        output_name = filename.replace(".enc", "")

        decrypted_path = os.path.join(
            current_app.config["DECRYPTED_FOLDER"],
            output_name
        )

        decrypt_file(
            encrypted_path,
            decrypted_path,
            aes_key
        )

        return render_template(
            "decrypt.html",
            decrypted_file=output_name
        )

    return render_template("decrypt.html")