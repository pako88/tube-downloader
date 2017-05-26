FROM alpine:latest
MAINTAINER Pascal König "mail@koenig-pascal.de"
EXPOSE 80
RUN apk --no-cache add py-pip ffmpeg ca-certificates
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python","app.py"]
