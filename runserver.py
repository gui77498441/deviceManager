from app import create_app,mail
from config import *
from app.models import db

app = create_app()
app.config.from_object(config['pro'])
print(app.config.get('MAIL_USERNAME'))
print(app.config.get('MAIL_PASSWORD'))

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()


if __name__=='__main__':
    app.run(use_reloader=False,debug=True) 

