FROM python:3.9.6-slim
WORKDIR /usr/src/app

COPY . ./
RUN ./dinstall.sh
CMD ["python", "./bot.py"]