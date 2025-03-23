import smtplib
from email.mime.text import MIMEText

# SMTPサーバの設定
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
USERNAME = 'your_username'
PASSWORD = 'your_password'

# メールの内容
from_addr = 'from@example.com'
to_addr = 'to@example.com'
subject = 'SMTPテスト'
body = 'これはSMTPサーバのテストメールです。'

msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = from_addr
msg['To'] = to_addr

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print("メールが正常に送信されました。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
