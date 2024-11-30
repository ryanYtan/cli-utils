#!/bin/bash

#check for sudo
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

#rm -rf ./bin
#mkdir -p ./bin

#copy all the files in src to bin
find ./src/ -name "*.py" -exec cp {} ./bin/ \;

#remove .py extension
for file in ./bin/*.py; do
    mv "$file" "${file%.py}"
done

#if each file doesn't have a shebang, add it
for file in ./bin/*; do
    if [ "$(head -n 1 "$file")" != "#!/usr/bin/env python3" ]; then
        sed -i '1s/^/#!\/usr\/bin\/env python3\n/' "$file"
    fi
done

#make the files executable
sudo chmod 755 ./bin/*

#copy to /usr/local/bin
sudo cp ./bin/* /usr/local/bin
