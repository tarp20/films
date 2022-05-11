FROM python:3.7

WORKDIR /films

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /films

EXPOSE 5000
CMD ["python", "./wsgi.py"]
