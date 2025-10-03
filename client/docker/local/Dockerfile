FROM docker.io/node:20.11-alpine3.19 AS base

FROM base AS node-build-stage

#RUN apk update && apk add --no-cache libc6-compat
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/community" >> /etc/apk/repositories \
    && apk update \
    && apk add --no-cache libc6-compat


WORKDIR /app

COPY package*.json yarn.lock* pnpm-lock.yaml* ./

RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi

COPY . .

RUN addgroup -g 1001 -S nodejs && \
   adduser -S nextjs -u 1001 -G nodejs && \
   chown -R nextjs:nodejs /app

USER nextjs

CMD [ "npm", "run", "dev" ]


 