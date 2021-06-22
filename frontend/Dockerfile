# Build app
FROM node:16.3-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@4.0.3 serve -g --silent

ADD public ./public
ADD src ./src
RUN npm run build

CMD serve -s build -l 4000