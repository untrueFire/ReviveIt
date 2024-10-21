FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json yarn.lock ./

RUN yarn config set registry https://registry.npmmirror.com/ &&\
	yarn install --frozen-lockfile

COPY . .

RUN yarn build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY run.sh /

EXPOSE 80

CMD ["sh","-c", "/run.sh"]
