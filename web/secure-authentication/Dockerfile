FROM node:16-buster-slim

COPY package.json yarn.lock /app/
WORKDIR /app

ENV FLAG temporary_flag
RUN yarn

COPY . .

EXPOSE 3000

CMD ["node", "/app/index.js"]

