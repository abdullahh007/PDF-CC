from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
from datetime import datetime, timedelta
import random, io

app = Flask(__name__)

CREATORS = ["Adobe Acrobat Pro DC","Microsoft Word 365","LibreOffice Writer"]
PRODUCERS = ["Adobe PDF Library 17.0","Microsoft Print To PDF"]
SUBJECTS = ["Internal Report","Business Documentation","Technical Report","Official Document"]
SAFE_NAMES = ["Project_Report","Internal_Report","Business_Documentation","Technical_Report","Financial_Statement"]

def gmail_safe_metadata():
    now = datetime.now()
    created = now - timedelta(days=random.randint(30,1500))
    return {
        "/Title": random.choice(SUBJECTS),
        "/Author": "Operations Team",
        "/Subject": random.choice(SUBJECTS),
        "/Creator": random.choice(CREATORS),
        "/Producer": random.choice(PRODUCERS),
        "/Keywords": "internal documentation",
        "/CreationDate": created.strftime("D:%Y%m%d%H%M%S"),
        "/ModDate": now.strftime("D:%Y%m%d%H%M%S")
    }

def safe_filename():
    name = random.choice(SAFE_NAMES)
    if random.choice([True, False]):
        name += f"_{random.randint(100,999)}"
    return name + ".pdf"

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        file = request.files["pdf"]
        reader = PdfReader(file)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata(gmail_safe_metadata())
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        return send_file(output,as_attachment=True,download_name=safe_filename(),mimetype="application/pdf")
    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
