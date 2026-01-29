FROM node:18-alpine

ENV NODE_ENV=production

WORKDIR /usr/src/app

# Create non-root user first
RUN addgroup -S nodejs && adduser -S nodejs -G nodejs

COPY package*.json ./
RUN npm install --only=production

COPY --chown=nodejs:nodejs . .

USER nodejs

EXPOSE 8080

CMD ["npm", "start"]
