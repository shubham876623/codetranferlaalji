from application import app
# import eventlet
# import eventlet.wsgi

port = 5001
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=port)
    # eventlet.wsgi.server(eventlet.listen(('', port)), app)



