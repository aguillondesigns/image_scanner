FROM python:3.11

COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
EXPOSE 5000

ENTRYPOINT [ "python3", "/app/src/local.py"]