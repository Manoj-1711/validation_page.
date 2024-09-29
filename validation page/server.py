from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__) 

# Email credentials and recipient
SENDER_EMAIL = "manumanojn2003@gmail.com"
RECEIVER_EMAIL = "nikilbonda420@gmail.com"
SENDER_PASSWORD = "vfpu ywym knay pwcw"

@app.route('/', methods=['GET'])
def index():
    # Render the form template
    return render_template('form.html', errors={}, success=None)

@app.route('/send-email', methods=['POST'])
def send_email():
    errors = {}
    success = None

    # Retrieve form data
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

   
    if not name or not name.isalpha():
        errors['name'] = 'Name is required and must only contain alphabetic characters.'
    if '@' not in email or '.' not in email:
        errors['email'] = 'A valid email address is required.'
    if not subject:
        errors['subject'] = 'Subject is required.'
    if not message or len(message) < 10:
        errors['message'] = 'Message must be at least 10 characters long.'

 
    if errors:
        return render_template('form.html', errors=errors, success=None)

  
    email_subject = f"Contact Form Submission: {subject}"
    email_body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

 
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = email_subject
    msg.attach(MIMEText(email_body, 'plain'))

    try:
      
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        success = "Your message has been sent successfully!"

    except Exception as e:
        errors['general'] = "Failed to send message. Please try again later."

 
    return render_template('form.html', errors=errors, success=success)

if __name__ == '__main__': 
    app.run(debug=True)
