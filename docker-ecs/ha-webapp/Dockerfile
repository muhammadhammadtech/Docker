FROM nginx:alpine
RUN apk add --no-cache curl
COPY index.html /usr/share/nginx/html/
COPY healthcheck.sh /usr/local/bin/
EXPOSE 80
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD /usr/local/bin/healthcheck.sh
CMD ["nginx", "-g", "daemon off;"]
