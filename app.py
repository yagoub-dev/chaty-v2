    from flask import Flask, render_template_string
    app = Flask(__name__)
    @app.route('/')
    def home():
        return render_template_string('<h1 style="color:white;text-align:center;padding-top:50px;background:#075e54;height:100vh">مرحبا في Chaty V2 🔥</h1>')
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
