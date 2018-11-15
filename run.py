import os

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*', omit='app/util/*')
    COV.start()

import sys
import click
from flask_migrate import Migrate, upgrade
from app.auth.model.user import User
from app import create_app, db


app = create_app(os.environ.get('FLASK_CONFIG') or 'development')

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if COV:
        COV.stop()
        COV.save()

        print('Coverage Summary:')
        COV.report()

        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)

        COV.erase()


@app.cli.command()
def create_db():
    """Creates the db tables."""
    db.create_all()


@app.cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@app.cli.command()
def deploy():
    upgrade()

    admin_username = app.config['ADMIN_USERNAME']
    admin_password = app.config['ADMIN_PASSWORD']

    if admin_username and admin_password:
        if not User.is_unique(id=0, username=admin_username):
            print("Admin user with username '{}' already exists".format(admin_username))
        else:
            user = User(admin_username, admin_password, admin=True)
            db.session.add(user)
            db.session.commit()
            print("Admin user '{}' created.".format(admin_username))


if __name__ == '__main__':
    app.run()
