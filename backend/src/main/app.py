
import os
from . import create_app

app = create_app()

# Hello World!
@app.route('/')

def hello():
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"Endpoint: {rule.endpoint}, Methods: {rule.methods}, URL: {rule.rule}")
    return "Hello World!"

from service.urls import urls_bp
app.register_blueprint(urls_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)