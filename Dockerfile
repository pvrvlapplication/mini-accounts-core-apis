FROM python:latest
EXPOSE 8000:8000
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]