#Tidy up the file
#Fill up the requirements files
#Set up the directory for Docker
#Use 1 best.pt for trial
#Try to host on local
#Push to Google Container Registry
#Run with Streamlit

FROM python:3.8.6-buster

WORKDIR /safety_detection

COPY docker docker

COPY requirements_prod.txt requirements.txt
COPY setup.py setup.py

RUN pip install .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN make reset_local_files

CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT
