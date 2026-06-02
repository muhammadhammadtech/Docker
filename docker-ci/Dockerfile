# Stage 1: Testing
FROM node:18-alpine AS testing
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm test

# Stage 2: Production
FROM node:18-alpine AS production
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY --from=testing /usr/src/app/app.js ./
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
RUN chown -R nodejs:nodejs /usr/src/app
USER nodejs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"
CMD ["npm", "start"]
