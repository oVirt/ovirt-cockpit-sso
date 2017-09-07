FROM cockpit/ws:latest

RUN dnf -y install python && dnf clean all

ENV OVIRT_SSO_DEBUG true
ADD ./container /container
RUN ln -s /host/etc/cockpit/ws-certs.d /container/config/cockpit/ws-certs.d

CMD ["/container/atomic-run", "--port=9000", "--no-tls"]

