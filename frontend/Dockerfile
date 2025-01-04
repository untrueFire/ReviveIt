FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json pnpm-lock.yaml ./

RUN npm config set registry https://registry.npmmirror.com &&\
	corepack enable &&\
	corepack prepare pnpm@9.15.2 &&\
	pnpm config set registry https://registry.npmmirror.com/ &&\
	pnpm install --frozen-lockfile
COPY . .

RUN pnpm build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY run.sh /

EXPOSE 80

CMD ["sh", "/run.sh"]
