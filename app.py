from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/invoice-form")
def invoice_form():
    return render_template("invoice_form.html")

@app.route("/quotation-form")
def quotation_form():
    return render_template("quotation_form.html")


# =========================
# INVOICE
# =========================
@app.route("/generate-invoice", methods=["POST"])
def generate_invoice():
    client_name = request.form["client_name"]
    invoice_no = request.form["invoice_no"]

    desc = request.form.getlist("desc[]")
    qty = request.form.getlist("qty[]")
    price = request.form.getlist("price[]")

    items = []
    subtotal = 0

    for i in range(len(desc)):
        q = float(qty[i])
        p = float(price[i])
        total = q * p
        subtotal += total

        items.append({
            "description": desc[i],
            "qty": q,
            "price": p,
            "total": total
        })

    date = datetime.now().strftime("%d-%m-%Y")

    rendered = render_template(
        "invoice.html",
        client_name=client_name,
        invoice_no=invoice_no,
        items=items,
        subtotal=f"{subtotal:.2f}",
        date=date
    )

    pdf_path = "invoice.pdf"
    HTML(string=rendered, base_url=request.base_url).write_pdf(pdf_path)

    return send_file(pdf_path, as_attachment=True)


# =========================
# QUOTATION
# =========================
@app.route("/generate-quotation", methods=["POST"])
def generate_quotation():
    client_name = request.form["client_name"]
    quote_no = request.form["quote_no"]

    desc = request.form.getlist("desc[]")
    qty = request.form.getlist("qty[]")
    price = request.form.getlist("price[]")

    items = []
    subtotal = 0

    for i in range(len(desc)):
        q = float(qty[i])
        p = float(price[i])
        total = q * p
        subtotal += total

        items.append({
            "description": desc[i],
            "qty": q,
            "price": p,
            "total": total
        })

    date = datetime.now().strftime("%d-%m-%Y")

    rendered = render_template(
        "quotation.html",
        client_name=client_name,
        quote_no=quote_no,
        items=items,
        subtotal=f"{subtotal:.2f}",
        date=date
    )

    pdf_path = "quotation.pdf"
    HTML(string=rendered, base_url=request.base_url).write_pdf(pdf_path)

    return send_file(pdf_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)