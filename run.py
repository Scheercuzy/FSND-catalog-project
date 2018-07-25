import sys
from catalog import app, db

if __name__ == '__main__':
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Database tables created")
    else:
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
