FROM ubuntu:22.04@sha256:899ec23064539c814a4dbbf98d4baf0e384e4394ebc8638bea7bbe4cb8ef4e12

ENV user poultry
ENV chall_port 8080

RUN apt-get update && apt-get install -y socat

RUN adduser -u 1337 $user

WORKDIR /home/$user

COPY ./flag ./flag
COPY ./deploy/main ./main

RUN chmod 644 ./flag
RUN chmod 755 ./main

USER $user

EXPOSE $chall_port
CMD socat TCP-LISTEN:8080,reuseaddr,fork EXEC:./main,stderr
