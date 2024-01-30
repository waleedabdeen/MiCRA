# Builder
FROM node:18-alpine AS builder

WORKDIR /app

COPY public/ /app/public
COPY src/ /app/src
COPY package.json /app/
COPY package-lock.json /app/

RUN npm i
RUN npm run build

# Production image
FROM nginx:1.24.0-alpine as production

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

ENV REACT_APP_SERVER_URL=http://localhost:5000

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
