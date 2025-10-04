# ---------- Base ----------

FROM python:3.9.7-alpine3.14 AS base

ENV PYTHONUNBUFFERED 1

# Create app directory
RUN mkdir -p /home/application/current
WORKDIR /home/application/current
ENV PYTHONPATH "${PYTHONPATH}:/home/application/current"

# System dependencies
RUN apk update \
    && apk add build-base postgresql-dev gcc python3-dev musl-dev openssl-dev libffi-dev

# Python requirements
COPY environment/requirements/requirements.txt /tmp/
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Entrypoint
COPY environment/entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
CMD ['dev']


# ---------- Development ----------
FROM base AS development

COPY environment/requirements/requirements-dev.txt /tmp/
#RUN apk add py3-pydot graphviz && pip install -r /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt

# ---------- Production ----------
FROM base AS production

# Bundle app source
COPY .src/ /home/application/current
