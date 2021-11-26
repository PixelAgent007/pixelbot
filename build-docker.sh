#!/bin/bash
docker build --pull --rm -f "DOCKERFILE" -t pixelbot:$(cat VERSION) "."
