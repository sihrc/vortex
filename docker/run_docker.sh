#! /bin/bash
docker build -t vortex .
docker stop -f vortex
docker rm vortex
docker run -v $(pwd):/vortex --name vortex -dt vortex bash
docker exec -it vortex bash
