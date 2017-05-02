from pipig import app


def data_setup():
    pass

if __name__ == '__main__':
    with app.app_context():
        data_setup()