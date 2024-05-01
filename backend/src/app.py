import os

# App Initialization
from . import create_app # from __init__ file
from src.models import db, User, Airline, Flight, Booking, BookingDetail
app = create_app(os.getenv("CONFIG_MODE"))

# Hello World!
@app.route('/')
def hello():
    return "Hello World!"
    
from src import urls

if __name__ == "__main__":
    app.run()