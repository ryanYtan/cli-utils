import sys
from pathlib import Path

for f in Path('./bin/').glob('*'):
    f.unlink()
Path('./bin/').rmdir()
Path('./bin/').mkdir()

folders = [f for f in Path('.').iterdir() if f.is_dir() and f.name != 'bin' and f.name != '.git']

for f in folders:
    print(f'Found folder: {f}')

for f in folders:
    main_files = list(f.glob(f'{f.name}.py'))
    if not main_files:
        print(f'WARNING: No main file found for {f.name}', file=sys.stderr)
        continue
    target = Path('./bin/') / f.stem
    main_file = main_files[0]
    with open(main_file) as f, open(target, 'w') as t:
        first_line = f.readline()
        if not first_line.startswith('#!'):
            t.write('#!/usr/bin/env python3\n\n')
        t.write(first_line)
        for line in f:
            t.write(line)
    target.chmod(0o755) #make executable
    print(f'Installed {target}')
