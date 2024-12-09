#!/bin/sh
envsubst '$API_URL' < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default2.conf
mv /etc/nginx/conf.d/default2.conf /etc/nginx/conf.d/default.conf
nginx -g "daemon off;"