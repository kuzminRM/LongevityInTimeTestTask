FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY lit_tt.conf /etc/nginx/conf.d/
COPY proxy_params /etc/nginx/
