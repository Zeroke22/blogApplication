FROM ubuntu:latest
LABEL authors="mykhailo"

ENTRYPOINT ["top", "-b"]