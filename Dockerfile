FROM python:3.12-alpine AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/app/install -r requirements.txt


# =========== Development Stage =============#
FROM build as development

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=build /app/install /usr/local

COPY script.sh /app/
RUN chmod +x script.sh

COPY . /app

RUN ls -la /app/script.sh

ENTRYPOINT [ "/app/script.sh" ]


# =========== Production Stage =============#
FROM build as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN useradd -r nduser

COPY --from=build /app/install /usr/local

COPY script.sh /app/
RUN chmod +x script.sh

COPY --chown=nduser . /app/

RUN chmod -R 755 /app

USER nduser

RUN ls -la /app/script.sh
ENTRYPOINT [ "/app/script.sh" ]