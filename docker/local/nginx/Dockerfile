FROM nginx:1.25.3-alpine

WORKDIR /etc/nginx/conf.d

RUN rm default.conf

COPY ./nginx.conf ./default.conf