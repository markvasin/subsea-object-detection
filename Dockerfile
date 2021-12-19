FROM python:3.9

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && apt-get clean \
    && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir model
COPY model/*.pt /code/model/
COPY main.py /code/

# clean
RUN apt-get autoremove -y && apt-get clean && \
    rm -rf /usr/local/src/*

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]