FROM python

RUN apt-get update -y
RUN apt-get upgrade -y

RUN mkdir /bot

COPY . /bot/

COPY requirements.txt /bot/

RUN python -m pip install --no-cache-dir -r /bot/requirements.txt

WORKDIR /bot

RUN pip freeze > requirements.txt

CMD ["python", "main.py"]