POSTGRES_USER='postgres'
POSTGRES_PASSWORD='postgres'
POSTGRES_DB='flight_db'
POSTGRES_HOST='flight_db'
POSTGRES_PORT=5432
FLASK_ENV='dev'
DATABASE_URL=f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'