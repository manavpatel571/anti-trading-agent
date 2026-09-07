import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Path to the ledger
LEDGER_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "ledger.json")

def load_ledger():
    try:
        with open(LEDGER_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load ledger: {e}")
        return None

def send_email(ledger_data):
    # Fetch credentials from Environment Variables (GitHub Secrets)
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_email = sender_email  # Sending to yourself
    
    if not sender_email or not sender_password:
        print("Error: EMAIL_ADDRESS or EMAIL_PASSWORD not found in environment.")
        return

    # Calculate basic stats (Assuming no price updates since we don't fetch yfinance here)
    # We will just report the dummy cash and open positions cost basis.
    cash = ledger_data.get("available_cash", 0.0)
    positions = ledger_data.get("positions", {})
    
    stock_value = 0.0
    positions_html = ""
    for sym, pos in positions.items():
        val = pos["quantity"] * pos["avg_price"]
        stock_value += val
        positions_html += f"<li><b>{sym}</b>: {pos['quantity']} shares @ ₹{pos['avg_price']:.2f} (Total: ₹{val:.2f})</li>"
        
    if not positions_html:
        positions_html = "<li>No open positions.</li>"
        
    total_value = cash + stock_value
    pnl = total_value - 50000.0
    pnl_color = "green" if pnl >= 0 else "red"
    
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Create HTML Email Content
    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #2c3e50;">📊 Daily Paper Trading Report - {date_str}</h2>
        <p>The market has closed! Here is the latest performance of your Anti-Trading Agent.</p>
        
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">💰 Portfolio Summary</h3>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><b>Available Cash:</b> ₹{cash:,.2f}</li>
                <li><b>Stock Value:</b> ₹{stock_value:,.2f}</li>
                <li><b>Total Portfolio Value:</b> ₹{total_value:,.2f}</li>
                <li><b>Total Profit/Loss:</b> <span style="color: {pnl_color}; font-weight: bold;">₹{pnl:,.2f}</span></li>
            </ul>
        </div>
        
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
            <h3 style="margin-top: 0;">📈 Open Positions</h3>
            <ul>
                {positions_html}
            </ul>
        </div>
        
        <p style="font-size: 12px; color: #777; margin-top: 20px;">
            <i>This report was generated automatically by GitHub Actions.</i>
        </p>
      </body>
    </html>
    """

    # Setup the email container
    msg = MIMEMultipart("alternative")
    msg['Subject'] = f"Anti-Trading Agent: EOD Report ({date_str})"
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Attach the HTML content
    msg.attach(MIMEText(html_content, "html"))

    try:
        # Send via Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Daily report email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    ledger = load_ledger()
    if ledger:
        send_email(ledger)
    else:
        print("Skipping email. Ledger not found.")
