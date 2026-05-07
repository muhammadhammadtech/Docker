FROM node:16-alpine

RUN apk add --no-cache curl

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["npm", "start"]
