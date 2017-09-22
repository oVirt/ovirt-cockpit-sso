#!/bin/bash

# prints private key retrieved from a .p12 file
# Usage:
#    keygen.sh [P12_FILE] [password]

# echo P12 file: $1 1>&2
# echo password 2: $2 1>&2

/usr/bin/openssl pkcs12 -in "$1" -passin "pass:$2" -nocerts -nodes | \
    grep -B 0 -A 1000 'BEGIN PRIVATE KEY' | \
    sed 's/-----BEGIN PRIVATE KEY/-----BEGIN RSA PRIVATE KEY/' | \
    sed 's/-----END PRIVATE KEY/-----END RSA PRIVATE KEY/'
