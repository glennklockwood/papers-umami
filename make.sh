#/bin/bash
#
#  because I be lazy
#

os="$(uname -s)"
if [ "$os" == "Darwin" ]; then
    preview_cmd="open"
elif [ "$os" == "Linux" ]; then
    preview_cmd="evince" # just guessing here.  I don't use linux
else
    preview_cmd="echo 'open this yourself: '"
fi

make clean && make && $preview=cmdholistic-io.pdf
