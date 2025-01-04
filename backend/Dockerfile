FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache nginx && \
	pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple && \
	pip install --no-cache-dir -r requirements.txt
COPY nginx.conf /etc/nginx/nginx.conf
COPY . .
EXPOSE 80
CMD ["sh", "/app/setup.sh"]