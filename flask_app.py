# from flask import Flask, render_template
# import subprocess

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/run_streamlit')
# def run_streamlit():
#     try:
#         subprocess.Popen(['streamlit', 'run', 'app.py'])  # Replace 'app.py' with your Streamlit app filename
#         return 'Streamlit app is running!'
#     except Exception as e:
#         return f'Error: {str(e)}'

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_streamlit')
def run_streamlit():
    try:
        # Replace 'your_streamlit_app.py' with the actual filename of your Streamlit app
        subprocess.Popen(['streamlit', 'run', 'app.py'])
        return 'Streamlit app is running!'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
