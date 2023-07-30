FROM python

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y wget

RUN apt-get -f install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0  \
    libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libgtk-4-1 libnspr4 libnss3  \
    libu2f-udev libvulkan1 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils

RUN apt install xvfb -y
RUN export DISPLAY=:1
RUN Xvfb $DISPLAY -screen $DISPLAY 1280x1024x16 &


RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

RUN mkdir /main_app

COPY ../requirements.txt /main_app/

COPY voxweb /main_app/

RUN python -m pip install -r /main_app/requirements.txt

WORKDIR /main_app

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]