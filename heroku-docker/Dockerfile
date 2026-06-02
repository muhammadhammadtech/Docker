FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install --only=production

COPY . .

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
RUN chown -R nodejs:nodejs /usr/src/app

USER nodejs

EXPOSE 3000

ENV NODE_ENV=production

CMD ["npm", "start"]
