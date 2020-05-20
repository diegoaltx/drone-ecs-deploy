FROM python:3-alpine
WORKDIR /usr/src/drone-ecs-deploy
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENTRYPOINT [ "python", "./ecs-deploy.py" ]
