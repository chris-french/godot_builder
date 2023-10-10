
#! /usr/bin/bash


echo "Compiling"

echo "cache_dir=$SCONS_CACHE"

godot_bin=godot.linuxbsd.editor.x86_64.mono

scons -j24 p=linuxbsd target=editor module_mono_enabled=yes debug_symbols=yes use_static_cpp=yes lto=full || { echo 'Editor build failed' ; exit 1; }


echo "Building Mono Solutions"

bin/$godot_bin --headless --generate-mono-glue modules/mono/glue

echo "Building Assemblies"

$PYTHON_BIN ./modules/mono/build_scripts/build_assemblies.py --godot-output-dir=./bin --godot-platform=linuxbsd


echo "Build Done"
exit 0;

