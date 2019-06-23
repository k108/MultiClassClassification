FROM ubuntu:latest 
MAINTAINER k108

RUN apt-get update \
    && apt-get -y install python python-pip vim \
    #&& pip install numpy \
    && pip install pandas \
    && pip install scipy \
    && pip install sklearn \
    && pip install psycopg2 \
    && pip install daemon \
    && pip install Flask
    
COPY engine /engine

COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]