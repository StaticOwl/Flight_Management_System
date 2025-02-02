import os

# App Initialization
from __init__ import create_app # from __init__ file
from models import db, User, Airline, Flight, Booking, BookingDetail
from dotenv import load_dotenv
load_dotenv()
app = create_app(os.getenv("CONFIG_MODE"))

# Hello World!
@app.route('/')
def hello():
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, URL: {rule.rule}")
    return "Hello World!"

import urls
from urls import urls_bp  # Import Blueprint
app.register_blueprint(urls_bp)

if __name__ == "__main__":
    app.run()