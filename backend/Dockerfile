FROM python:3.12-alpine
WORKDIR /app
COPY . .
RUN pip config set global.index-url https://mirror.sjtu.edu.cn/pypi/web/simple && \
	pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["sh", "-c", "/app/setup.sh"]