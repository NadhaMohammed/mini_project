import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app) # Allow cross-origin requests

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "root"),
            database=os.getenv("DB_NAME", "eventhub"),
            auth_plugin='mysql_native_password'
        )
        return db
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def init_db():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subscribers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status ENUM('active', 'unsubscribed') DEFAULT 'active'
                )
            """)
            db.commit()
            print("Subscribers table initialized successfully.")
        except Error as e:
            print(f"Error creating subscribers table: {e}")
        finally:
            cursor.close()
            db.close()

# Initialize DB tables on startup
init_db()

@app.route("/")
def home():
    return "EventHub Backend Running"

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
        
    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database connection error"}), 500
        
    try:
        cursor = db.cursor()
        query = "INSERT INTO subscribers (name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        db.commit()
        return jsonify({"success": True, "message": "Successfully subscribed to notifications!"})
    except Error as e:
        if e.errno == 1062: # Duplicate entry
            return jsonify({"error": "This email is already subscribed."}), 400
        print(f"Database error: {e}")
        return jsonify({"error": "An error occurred while subscribing."}), 500
    finally:
        if db.is_connected():
            db.close()

def send_new_event_email(event_name, event_date, event_description):
    """Retrieves all active subscribers and sends them an email about the new event."""
    with app.app_context():
        db = get_db_connection()
        if not db:
            print("Could not connect to database to fetch subscribers.")
            return False
            
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT email, name FROM subscribers WHERE status = 'active'")
            subscribers = cursor.fetchall()
            
            if not subscribers:
                print("No active subscribers found. Skipping emails.")
                return True
                
            recipients = [sub['email'] for sub in subscribers]
            
            msg = Message(
                subject=f"New Event Created: {event_name}!",
                sender=app.config.get("MAIL_USERNAME"),
                bcc=recipients
            )
            
            msg.html = f"""
            <h2>New Event: {event_name}</h2>
            <p><strong>Date:</strong> {event_date}</p>
            <p>{event_description}</p>
            <br>
            <p>Visit the EventHub website to learn more and register!</p>
            """
            
            mail.send(msg)
            print(f"Successfully sent event notification to {len(recipients)} subscribers.")
            return True
        except Exception as e:
            print(f"Error sending email notifications: {e}")
            return False
        finally:
            if db.is_connected():
                db.close()

def send_new_event_email(event_name, event_date, event_description):
    """Retrieves all active subscribers and sends them an email about the new event."""
    # We don't need app.app_context() here because this will be called within a request context from admin_login.py
    # or we can import app from admin_login and use it here. But to keep it modular, let's keep the logic simple.
    # We will import `app` and `mail` from admin_login.py instead later.
    pass # Wait, it's better to just leave app.py as is but remove the routing conflict, and mount app.py routes onto admin_login.py's app. Or, even simpler: move the mail config and routes into admin_login.py directly to have a true single monolithic backend as the user expects.
