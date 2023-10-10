Godot Builder
===

A tool to create nightly Godot Mono/C# builds for use on Arch Linux/Manjaro.

The `dist` folder is where binaries and the `GodotSharp` data folder is built. After creating a new project with the editor in `dist`, you can add the source:

```sh
dotnet nuget add source ${GODOT_BUILDER_DIR}/dist/editor/GodotSharp/Tools/nupkgs
```

where `GODOT_BUILDER_DIR` is the directory of godot builder.

## Building

Create a `venv`, do `/venv/bin/pip install -r requirements.txt` and run `build.py` -- you must have docker running.

## Example Deployment

The editor or release/debug builds in the `dist` folder can then be copied into a project to run the editor or create a server.

For example, a dockerfile to run a server for a `.pck` file built by the editor could look like:

```
ENV PATH="$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools:/server/godot"
RUN PATH=$PATH

RUN mkdir /server
WORKDIR /server

COPY bin/dist/release/godot.linuxbsd.template_debug.x86_64.mono godot
RUN chmod +x godot

COPY bin/dist/release/GodotSharp data_flocked_linuxbsd_x86_64
COPY bin/debug.pck debug.pck

RUN dotnet nuget add source data_flocked_linuxbsd_x86_64/Tools/nupkgs --name GodotSharp

WORKDIR /server

ENTRYPOINT ["godot", "--headless", "--server", "--main-pack", "debug.pck" ]

EXPOSE 8000
```
