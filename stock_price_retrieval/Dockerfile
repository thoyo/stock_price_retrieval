FROM python:3.8

ENV STOCK_PRICE_RETRIEVAL /opt/stock_price_retrieval

RUN mkdir -p $STOCK_PRICE_RETRIEVAL
WORKDIR $STOCK_PRICE_RETRIEVAL

COPY requirements.txt .
COPY config.json .
RUN pip install -r requirements.txt

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

COPY main.py .

CMD ["python", "-u", "main.py"]

