from app import app, db
from app.models import Commander, RecsText

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Commander': Commander, 'RecsText': RecsText}