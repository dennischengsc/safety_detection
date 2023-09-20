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
import threading
import subprocess
import os

app = Flask(__name__)

# Create a global variable to keep track of the Streamlit process
streamlit_process = None

@app.route('/')
def index():
    return render_template('index.html')

def run_streamlit_app():
    global streamlit_process
    try:
        streamlit_command = ['streamlit', 'run', 'app.py']  # Replace 'app.py' with your Streamlit app filename
        streamlit_process = subprocess.Popen(streamlit_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = streamlit_process.stdout.readline()
            if output == b'' and streamlit_process.poll() is not None:
                break
            if output:
                print(output.strip())
        streamlit_process.wait()  # Wait for the Streamlit process to finish
    except Exception as e:
        print(f'Error: {str(e)}')

@app.route('/run_streamlit')
def run_streamlit():
    global streamlit_process
    if streamlit_process is None or streamlit_process.poll() is not None:
        # If there is no Streamlit process running or it has finished, start a new one
        streamlit_thread = threading.Thread(target=run_streamlit_app)
        streamlit_thread.start()
        return 'Streamlit app is running!'
    else:
        return 'Streamlit app is already running.'

if __name__ == '__main__':
    app.run(debug=True)
