FROM python:latest
EXPOSE 8000
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
WORKDIR /app
COPY . /app
ENTRYPOINT ["python"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]