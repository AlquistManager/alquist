#!/bin/bash
# Run this file to launch a Docker container
# Port to run has to be passed as a parameter
docker run -it -p $1:5000 alquist
