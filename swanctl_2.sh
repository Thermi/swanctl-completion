# swanctl completion

_swanctl() {
    local cur prev words cword
    _init_completion || return

    REPLY=$(python ./swanctl.py --words="${words[*]}" --cur="${cur}" --prev="${prev}" --cword="$cword" )
ret=$?

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

COMPREPLY=( $(compgen -W "${REPLY}" -- "$cur") )
} &&
complete -o nosort -F _swanctl swanctl