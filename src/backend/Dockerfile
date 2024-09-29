ARG COMMON_IMAGE_URL

# Stage 1: Build Phoenix app
FROM "${COMMON_IMAGE_URL:python:3.12-alpine}" as phx-builder

RUN apk add --allow-untrusted --no-cache yarn

ARG COMMON_IMAGE_URL
ARG APP
ARG PORT

ENV MIX_ENV=prod
ENV PORT=$PORT

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN if [[ "$APP" == "api" ]]; then echo "uvicorn api.main:app --reload" > run.sh; fi
RUN if [[ "$APP" == "worker" ]]; then echo "PYTHONPATH=. && python worker/main.py" >> run.sh; fi
RUN if [[ "$APP" == "notificator" ]]; then echo "PYTHONPATH=. && python notificator/main.py" >> run.sh; fi
RUN echo "$APP/bin/$APP start" >> run.sh

EXPOSE $PORT

ENTRYPOINT sh run.sh
