CAGE_ENV="__CAGE_ENV__"
export CAGE_ENV

# TODO: Detect if directory still exists and change __CAGE_ENV__ accordingly

_OLD_PATH="$PATH"

# TODO: Remove hardcoded path and replace with some sort of install path

PATH="$CAGE_ENV:/Users/mihaic/Developer/cage:$PATH"
export PATH

PS1="(`basename \"$CAGE_ENV\"`) $PS1"
export PS1

if [ -n "${BASH-}" ] || [ -n "${ZSH_VERSION-}" ] ; then
    hash -r 2>/dev/null
fi
