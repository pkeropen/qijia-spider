FROM python:3.5
ENV PATH /usr/local/bin:$PATH
EXPOSE 3306
EXPOSE 80

ADD . /qijia-spider
WORKDIR /qijia-spider

RUN pip install -r requirements.txt
#COPY spiders.py /usr/local/lib/python3.7/site-packages/scrapy_redis
CMD [ "python", "/qijia-spider/main.py" ]

