FROM python:3.8


RUN apt-get update
RUN mkdir -p /workflow

COPY . /workflow
RUN chmod +x /workflow/main.py
RUN pip install -r workflow/requirements.txt

ENTRYPOINT ["python", "workflow/main.py"]
