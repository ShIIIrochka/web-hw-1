FROM python:3.13-alpine

COPY ./pyproject.toml /
COPY ./uv.lock /

RUN pip install --upgrade pip && \
    pip install uv

RUN uv export --format requirements-txt --output-file requirements.txt --no-dev
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "ash", "/entrypoint.sh"]