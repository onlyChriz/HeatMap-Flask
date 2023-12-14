from __init__ import create_app

#entry of app
#Run program here

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
    