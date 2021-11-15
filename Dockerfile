FROM python:3.9.5
WORKDIR /project
COPY requirements.txt project/requirements.txt
RUN pip install -r project/requirements.txt
COPY .. .
CMD ["python3", "async_bot.py"]