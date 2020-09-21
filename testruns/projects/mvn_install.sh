#!/bin/bash
docker run --rm -it -v $(pwd):/mnt/ maven:latest bash -c "cd /mnt && mvn install"