import sys
from pathlib import Path

DIR_BIN = Path('./bin/')
DIR_SRC = Path('./src/')

print(f'### Clearing {DIR_BIN} directory')
for f in DIR_BIN.glob('*'):
    f.unlink()
DIR_BIN.mkdir(exist_ok=True)
print('...done')

print(f'### Finding programs...')
folders = [f for f in DIR_SRC.iterdir() if f.is_dir() and f != DIR_BIN and not f.name.startswith('.')]
for f in folders:
    print(f'Found PROG: {f}')
print(f'...done')

print(f'### Installing...')
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
print('...done. Exiting.')
