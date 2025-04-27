import os
from main import create_app, db

app = create_app(config_mode=os.getenv('FLASK_ENV') or 'dev')


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