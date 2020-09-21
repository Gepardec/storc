#!/bin/bash

docker build -t gepardec/ansible-jboss -f Dockerfile.test .

docker run --rm -it -v $(cd .. && pwd):/mnt gepardec/ansible-jboss