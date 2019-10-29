# swanctl completion

_swanctl() {
    local cur prev words cword
    _init_completion || return
    echo "${words[@]}" >> completion_test
    REPLY=$(python ./swanctl.py --words="${words[*]}" --cur="${cur}" --prev="${prev}" --cword="$cword" )
ret=$?
echo "ret: $ret" > completion_test
case $ret in
    4)
    _filedir
    return
    ;;
    5)
    _known_hosts_real -- "$cur"
    return
    ;;
esac

echo "${REPLY}" >> completion_test
COMPREPLY=( $(compgen -W "${REPLY}" -- "$cur") )
} &&
complete -o nosort -F _swanctl swanctl