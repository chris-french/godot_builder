#! /usr/bin/bash

echo "Starting build godot_bin=$godot_bin python_bin=$PYTHON_BIN"

rm -Rf bin/editor/*
rm -Rf bin/release/*
rm -Rf bin/debug/*
rm -Rf ./godot/bin/*


cd godot
git pull origin master
cd ..

