FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/local/lib/python3.7/

# instruction from google
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk google-cloud-sdk-app-engine-python -y

RUN mkdir /src;

WORKDIR /src

RUN mkdir /config

COPY config /config/

RUN pip install -r /config/requirements.txt && rm /config/requirements.txt

COPY src /src

RUN chmod +x wait-for-it.sh

EXPOSE 8085

CMD [ "python", "/src/main.py" ]
