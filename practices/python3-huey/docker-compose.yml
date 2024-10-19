version: '3'

services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  app:
    build: .
    command: python your_app.py
    volumes:
      - .:/app
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
