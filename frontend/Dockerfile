# Build app
FROM node:16.3-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@4.0.3 serve -g --silent

ENV REACT_APP_BACKEND_ADDRESS=http://0.0.0.0:5000

ADD public ./public
ADD src ./src
RUN npm run build

CMD serve -s build -l 4000