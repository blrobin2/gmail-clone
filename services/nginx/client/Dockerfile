FROM node:19.1.0-buster-slim

WORKDIR /usr/src/app

COPY package*.json /usr/src/app/package*.json

RUN npm install

COPY . /usr/src/app/
