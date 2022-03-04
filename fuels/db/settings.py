# Database info
DB_DIALECT = "postgresql"
DB_HOSTNAME = "127.0.0.1:5433"
DB_USERNAME = "fuel"
DB_PASSWORD = "fuel"
DB_DATABASE = "fueldb"

DB_URL = "%s://%s:%s@%s/%s" % (
    DB_DIALECT,
    DB_USERNAME,
    DB_PASSWORD,
    DB_HOSTNAME,
    DB_DATABASE
)