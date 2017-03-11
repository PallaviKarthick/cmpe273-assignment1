FROM python:2.7.13
MAINTAINER PallaviKarthick "pallaviatg@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install pyGithub
ENTRYPOINT ["python" , "app.py"]
