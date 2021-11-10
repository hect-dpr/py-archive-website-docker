FROM python
COPY fetch /root/fetch
WORKDIR /root/fetch
RUN pip install -r requirements.txt; chmod +x fetch.py