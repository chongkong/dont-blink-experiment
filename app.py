from dontblink.factory import create_app

app = create_app()


if __name__ == '__main__':
    app.run("localhost", 8081, debug=True)
