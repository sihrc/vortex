#! /bin/bash
docker build -t {{project}} .
docker stop {{project}}
docker rm {{project}}
docker run -v $(pwd):/{{project}} -dt {{project}} .
docker exec -it {{project}} bash
