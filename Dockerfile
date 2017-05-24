FROM cockpit/ws:latest

RUN dnf -y install python && dnf clean all

ENV OVIRT_SSO_DEBUG true
ADD ./container /container

CMD ["/container/atomic-run", "--port=9000", "--no-tls"]

