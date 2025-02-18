import imaplib
import email
import json
from bs4 import BeautifulSoup

EMAIL_USER = "xxx@gmail.com"
EMAIL_PASS = "password"
IMAP_SERVER = "imap.gmail.com"


mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_USER, EMAIL_PASS)
mail.select("inbox")

result, data = mail.search(None, '(UNSEEN FROM "notificacion@notificacionesbaccr.com")')
transactions = []

for num in data[0].split():
    result, msg_data = mail.fetch(num, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    email_body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                email_body = part.get_payload(decode=True).decode()
                break 
    else:
        email_body = msg.get_payload(decode=True).decode()

    soup = BeautifulSoup(email_body, "html.parser")
    rows = soup.find_all("tr")
    comercio, fecha, monto = None, None, None

    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)

            if "Comercio" in key:
                comercio = value
            elif "Fecha" in key:
                fecha = value
            elif "Monto" in key:
                monto = value
    
    if comercio and fecha and monto:
        transactions.append({
            "fecha": fecha,
            "comercio": comercio,
            "monto": monto
        })
print(transactions)

    
mail.logout()