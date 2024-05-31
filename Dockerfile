FROM ubuntu:latest
LABEL authors="vvolkovskiy"

ENTRYPOINT ["top", "-b"]