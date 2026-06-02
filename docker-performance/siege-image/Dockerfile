FROM ubuntu:22.04
RUN apt-get update && apt-get install -y siege && rm -rf /var/lib/apt/lists/*
CMD ["siege", "--version"]
