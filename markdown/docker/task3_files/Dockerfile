FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY app/package.json app/package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts

COPY app/ ./

USER node
EXPOSE 3000
CMD ["node", "index.js"]
