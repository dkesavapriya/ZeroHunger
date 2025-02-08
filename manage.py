from app.models import  db
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click
from app.app import create_app

app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Flask CLI migration commands (no need for MigrateCommand)
@app.cli.command("db_init")
@with_appcontext
def db_init():
    """Initialize the migrations folder."""
    from flask_migrate import init
    init()

@app.cli.command("db_migrate")
@with_appcontext
def db_migrate():
    """Generate a migration file."""
    from flask_migrate import migrate
    migrate()

@app.cli.command("db_upgrade")
@with_appcontext
def db_upgrade():
    """Apply the migrations to the database."""
    from flask_migrate import upgrade
    upgrade()

if __name__ == '__main__':
    app.run(debug=True)
