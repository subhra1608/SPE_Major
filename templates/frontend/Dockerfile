
FROM node:14-alpine
COPY package*.json ./
RUN npm install

COPY /public /public
COPY /src /src

CMD ["npm", "start"]


