#! /usr/bin/bash

echo "Building=$1"

bash /scripts/build_$1.sh && exit 0;
