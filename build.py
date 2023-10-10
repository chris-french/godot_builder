#! ./venv/bin/python

import sys
import os
from datetime import datetime
from uuid import uuid4
import subprocess
from dataclasses import dataclass
from pathlib import Path
from dotenv import dotenv_values

Build_Version = str(uuid4())[:8]; print(f'build_verison={Build_Version}')
PY_Version = sys.version; print(f'python={PY_Version}')
PWD = os.getenv('PWD')
PATH = os.getenv('PATH')

env = dotenv_values('./config/.env')

env['GODOT_VERSION_STATUS'] = f'{env["major"]}.{env["minor"]}.{env["patch"]}-{Build_Version}'

LOG = Path('./config/log.csv').absolute()

if not LOG.is_file():
    with open(LOG, 'w') as f:
        f.write(f'build,editor_start,editor_end,debug_start,debug_end,release_start,release_end\n')


@dataclass
class Times:
    s: float
    e: float
    error: int


get_ts = lambda: datetime.timestamp(datetime.utcnow())

finished_times = [f'Godot Builder. pwd={PWD}', f'Build Version: {env["GODOT_VERSION_STATUS"]}']

def run_cmd(build: str, cmd: str) -> Times:
    cache = []
    exe = cmd.split()
    for m in finished_times:
        print(m.strip() + '\n')
    print(f'running command: {cmd}')
    s = get_ts()

    p = subprocess.Popen(
        exe,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env
    )

    formatter = lambda s: f'{s:.2f} secs' if s < 60 else f'{s/60:.2f} mins'

    while(True):
        # returns None while subprocess is running
        retcode = p.poll()
        line = p.stdout.readline().decode("utf-8")
        cache.append(line)
        message = f'{build}|{formatter(get_ts()-s)}|{line}'
        if retcode is not None:
            finished_times.append(message)
            if retcode > 0:
                with open(Path(f'config/logs/error_log.{build}.{Build_Version}.txt'), 'w') as f:
                    f.writelines(cache)
            break
        else:
            print(message)

    e = get_ts()
    return Times(s, e if retcode == 0 else retcode, retcode)


def run_build(build, clean=True) -> Times:
    times = run_cmd(f'build={build}',
    f'docker run -t '
    f'--mount type=bind,source={PWD}/bin,target=/godot/bin '
    f'--mount type=bind,source={PWD}/.scons_cache,target=/godot/.scons_cache '
    f'--mount type=bind,source={PWD}/godot,target=/godot '
    f'--mount type=bind,source={PWD}/dockerfiles,target=/scripts '
    f'godot_editor {build}')

    if clean: run_cmd('move_&_clean', f'dockerfiles/move_and_clean_bin.sh {build}')
    return times


DOCKER_FILE_BASE = os.getenv('DOCKER_FILE_BASE', 'dockerfiles/Dockerfile.base')
DOCKER_FILE_EDITOR = os.getenv('DOCKER_FILE_BASE', 'dockerfiles/Dockerfile.editor')


base_image_times = run_cmd('build image: base',
    f'docker build -f {DOCKER_FILE_BASE} '
    '--tag godot_builder '
    '--platform=linux/amd64 .')

editor_image_times = run_cmd('build image: editor',
    f'docker build --no-cache -f {DOCKER_FILE_EDITOR} '
    '--tag godot_editor '
    '--platform=linux/amd64 '
    '--no-cache '
    #'--pull=false '
    '.')

run_cmd('clean', 'dockerfiles/upkeep.sh')

editor_times = run_build('editor')
debug_times = run_build('debug', clean=False)
release_times = run_build('release')

with open(LOG, 'a') as f:
    f.write(f'{Build_Version},{editor_times.s},{editor_times.e},{debug_times.s},{debug_times.e},{release_times.s},{release_times.e}\n')

errors = int(editor_times.error > 0) +\
    int(debug_times.error) > 0 +\
    int(release_times.error > 0)

[print(m) for m in finished_times]
print(f'Build completed. Errors: {errors}')
