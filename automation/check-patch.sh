#!/bin/bash -xe

make distclean

make dist
make srpm
make rpm

# Store any relevant artifacts in exported-artifacts for the ci system to
# archive
#[[ -d exported-artifacts ]] || mkdir -p exported-artifacts
#find tmp.repos -iname \*rpm -exec mv "{}" exported-artifacts/ \;
#mv ./*tar.gz exported-artifacts/

