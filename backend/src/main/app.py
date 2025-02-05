import os

# App Initialization
from dao.models import db, User, Airline, Flight, Booking, BookingDetail
import os
from __init__ import create_app # from __init__ file

app = create_app()

# Hello World!
@app.route('/')
def hello():
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, URL: {rule.rule}")
    return "Hello World!"

import service.urls as urls
from service.urls import urls_bp  # Import Blueprint
app.register_blueprint(urls_bp)

if __name__ == "__main__":
    app.run()