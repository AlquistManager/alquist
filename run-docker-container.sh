#!/bin/bash
# Run this file to launch a Docker container
# Port to run and path to yml files have to be passed as a parameter
docker run -d -v $2:/alquist/yaml -p $1:5000 alquist
