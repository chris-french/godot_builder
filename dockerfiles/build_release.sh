
#! /usr/bin/bash


echo "Compiling"

scons -j24 p=linuxbsd target=template_release module_mono_enabled=yes use_static_cpp=yes production=yes lto=full || { echo 'Prod build failed' ; exit 1; }


echo "Building Mono Solutions"

godot_bin=godot.linuxbsd.template_release.x86_64.mono

bin/$godot_bin --headless --generate-mono-glue modules/mono/glue

echo "Building Assemblies"

$PYTHON_BIN ./modules/mono/build_scripts/build_assemblies.py --godot-output-dir=bin --godot-platform=linuxbsd


echo "Build Done"
exit 0;
