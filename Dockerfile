FROM python:3.12.7 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
ENV COUNTRY_DETAILS_API=$COUNTRY_DETAILS_API
ENV COUNTRY_EXCHANGE_DETAILS_API=$COUNTRY_EXCHANGE_DETAILS_API
ENV DATABASE_URL=$DATABASE_URL

ENV PIPENV_VENV_IN_PROJECT=1 \
    PIPENV_CUSTOM_VENV_NAME=.venv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
FROM python:3.12.7-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
