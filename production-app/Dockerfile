FROM node:18-alpine

LABEL org.opencontainers.image.title="Production Node.js App"
LABEL org.opencontainers.image.description="Dockerized production-ready Node.js application"
LABEL org.opencontainers.image.version="1.1"
LABEL maintainer="Muhammad Hammad"

WORKDIR /app

ENV NODE_ENV=production \
    NPM_CONFIG_UPDATE_NOTIFIER=false

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

COPY package*.json ./

RUN npm install -g npm@latest && \
    npm install --omit=dev && \
    npm cache clean --force

COPY server.js ./

RUN chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 3000

HEALTHCHECK --interval=20s \
             --timeout=5s \
             --start-period=10s \
             --retries=3 \
CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["npm", "start"]
