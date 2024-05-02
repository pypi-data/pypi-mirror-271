#!/bin/bash
DIR=$(dirname "$0")
VERSION=$(./tools/get-version.sh)
mkdir -p "${DIR}/../dist"
sed -e "s/VERSION_PLACEHOLDER/${VERSION}/" \
    "${DIR}/../dist/python-distronode-compat.spec.in" \
    > "${DIR}/../dist/python-distronode-compat.spec"
