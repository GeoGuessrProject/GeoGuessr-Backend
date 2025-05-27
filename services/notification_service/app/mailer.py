import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
def load_template(filename, **kwargs):
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, "r", encoding="utf-8") as file:
        template = file.read()
    return template.format(**kwargs)


def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

#send_email("simonbang1@hotmail.com", "Hello!", "This is a test email sent from Python.")
def send_registration_email(to_email, username):
    subject = "Tak for din registrering!"
    body = load_template("registration.txt", username=username)
    send_email(to_email, subject, body)

def send_dropped_out_email(to_email, username, rank):
    subject = "Du er røget ud af Top 10"
    body = load_template("dropped_out_of_top10.txt", username=username, rank=rank)
    send_email(to_email, subject, body)

def send_highscore_email(to_email, username, score):
    subject = "Ny highscore opnået!"
    body = load_template("new_highscore.txt", username=username, score=score)
    send_email(to_email, subject, body)
    
send_dropped_out_email("simonbang1@hotmail.com", username="Simon", rank=12)
send_highscore_email("simonbang1@hotmail.com", username="Simon", score=1000)