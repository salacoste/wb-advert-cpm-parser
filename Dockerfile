FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENTRYPOINT [ "python", "./wb_advert_cpm_parser.py"]