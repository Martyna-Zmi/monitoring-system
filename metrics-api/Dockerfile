FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY app.js .

VOLUME ["/data"]

CMD ["node", "app.js"]
