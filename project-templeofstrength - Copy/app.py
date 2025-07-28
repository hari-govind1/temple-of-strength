from flask import Flask, render_template, request, flash, redirect, url_for
from email_utils import send_payment_email  # Assuming this is your modular email file

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/classes')
def classes():
    classes = [
        {'name': 'Yoga', 'time': 'Mon/Wed, 6 PM', 'description': 'Relax and strengthen.', 'image': '/static/images/yoga.jpg'},
        {'name': 'CrossFit', 'time': 'Tue/Thu, 7 PM', 'description': 'High-intensity training.', 'image': '/static/images/crossfit.jpg'},
        {'name': 'Weightlifting', 'time': 'Fri/Sat, 5 PM', 'description': 'Build strength.', 'image': '/static/images/weightlifting.jpg'}
    ]
    return render_template('classes.html', classes=classes)

@app.route('/trainers')
def trainers():
    trainers = [
        {'name': 'John Doe', 'bio': 'Certified CrossFit Coach.', 'image': '/static/images/trainer1.jpg'},
        {'name': 'Jane Smith', 'bio': 'Yoga Instructor.', 'image': '/static/images/trainer2.jpg'}
    ]
    return render_template('trainers.html', trainers=trainers)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        program = request.form['program']
        message = request.form['message']
        
        # Log the submission (as before)
        print(f"Contact form submitted: {name}, {email}, Program: {program}, Message: {message}")
        
        # Send personalized welcome email to user
        try:
            send_payment_email(email, name, program, 0)  # Reuse function; price=0 since no payment here
            flash('Message sent successfully! Check your email for a welcome note.')
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            flash('Message sent, but email failed. We\'ll follow up soon.')
        
    return render_template('contact.html')


@app.route('/send-payment-email', methods=['POST'], endpoint='payment_email_endpoint')
def send_payment_email_route():
    name = request.form['name']
    email = request.form['email']
    program_name = request.form['programName']
    program_price = request.form['programPrice']
    
    try:
        send_payment_email(email, name, program_name, program_price)
        print("Email sent - Redirecting with success=true")  # Terminal log
        # Explicitly build URL with param (fixes any url_for issues)
        return redirect('/programs?success=true')  # Change to '/plans?success=true' if your route is /plans
    except Exception as e:
        print(f"Error sending email: {e}")
        flash('Error sending email. Please try again.', 'error')
        return redirect('/programs')  # Or '/plans'
    
if __name__ == '__main__':
    app.run(debug=True)  # Reloader enabled; if issues persist, set use_reloader=False temporarily
