import os
import code

from flask_script import Manager
from flask_migrate import MigrateCommand

from dmLibrary import create_app

from dmLibrary.config import config
import logging


PORT = int(config.get('PORT', 5000))


def run():
    app = create_app()
    app.run(host='0.0.0.0', port=PORT)

def cli():
    """ Interactive CLI session entrypoint """
    app = create_app()
    with app.app_context():
        code.interact(local=locals())
        
def manage():
    from dmLibrary import migrate
    app = create_app()
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()

# Run entrypoint
if __name__ == '__main__':
    run()