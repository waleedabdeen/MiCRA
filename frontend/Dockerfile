# Builder
FROM node:18-alpine AS builder

WORKDIR /app

COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/
COPY package-lock.json /app/

RUN npm i

ARG REACT_APP_SERVER_URL=$REACT_APP_SERVER_URL
RUN npm run build

# Production image
FROM nginx:1.24.0-alpine as production

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
