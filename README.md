# Django Ninja Tutorial

Django Ninja with SQLite

Basic CRUD API for Employees and Department using Django Ninja.
Deployed using Granian Server

## Docker Compose Commands

Get running containers

`docker ps`

Build and Run in detached mode

`docker compose up --build -d`

To enter Bash Shell for migrating db changes or static files

`docker exec -it <container id from docker ps> bash`

To view logs of container. You can pass head to view first N lines or tail to view last N lines specified by argument after head/tail

`docker logs --tail 1000 -f <container id from docker ps>`
