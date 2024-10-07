FROM python:3.12-alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache nginx && \
	pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple && \
	pip install --no-cache-dir -r requirements.txt
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["sh", "-c", "/app/setup.sh"]