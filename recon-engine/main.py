import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class HelloWorldMessage(BaseModel):
    message: str
class TransactionDetail(BaseModel):
    type: str
    amount: float
    description: str


class ReconciliationData(BaseModel):
    station_id: int
    date: str
    total_cash_in: float
    total_cash_out: float
    transaction_details: List[TransactionDetail]


def send_email(reconciliation_data: ReconciliationData):
    # Email configuration
    sender_email = "ntonsitemwamlima11@gmail.com"
    receiver_email = "tonyborady@gmail.com"
    password = "@!MAisho2022"

    # Create message container
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Reconciliation Data"

    # Create HTML message
    html = f"""
    <html>
      <body>
        <h2>Reconciliation Data:</h2>
        <p>Station ID: {reconciliation_data.station_id}</p>
        <p>Date: {reconciliation_data.date}</p>
        <p>Total Cash In: {reconciliation_data.total_cash_in}</p>
        <p>Total Cash Out: {reconciliation_data.total_cash_out}</p>
        <h3>Transaction Details:</h3>
        <ul>
    """
    for detail in reconciliation_data.transaction_details:
        html += f"<li>Type: {detail.type}, Amount: {detail.amount}, Description: {detail.description}</li>"
    html += """
        </ul>
      </body>
    </html>
    """

    # Attach HTML message
    msg.attach(MIMEText(html, 'html'))

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


@app.post("/")
async def receive_reconciliation_data(data: ReconciliationData):
    # Example: Just print received data
    print("Received reconciliation data:")
    print(data)

    # # Send reconciliation data via email
    #send_email(data)

    return {"message": "Reconciliation data received and sent via email successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=10000)
