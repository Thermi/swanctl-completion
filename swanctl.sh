# swanctl completion

_swanctl() {
    local cur prev words cword
    _init_completion || return
    local long_commands
    local short_commands
    local general_options
    long_commands='--counters --initiate --terminate --rekey --redirect
        --uninstall --install --list-sas --monitor-sa --list-pols
        --list-authorities --list-conns --list-certs --list-pools --list-algs
        --flush-certs --load-all --load-authorities --load-conns --load-creds
        --load-pools --log --version --stats --reload-settings --help'
    short_commands='-C -i -t -R -d -u -p -l -m -P -B -L -x -A -g -f -q -b
        -c -s -a -T -v -s -r -h'
    general_options='--help -h --raw -r --pretty -P --debug -v --options
        -+ --uri -u'

    local options

    if [[ "$cword" -eq 1 ]]
    then
        COMPREPLY=( $(compgen -W "$long_commands $short_commands" -- "$cur") )
    else
        local command="${words[1]}"

        case "$command" in
            -C|--counters)
                options="-n --name -a --all -R --reset"
                if [[ "$prev" == @(--name|-n) ]]
                then
                    COMPREPLY=( )
                    return
                fi
            ;;
            -i|--initiate)
                options="-c --child -i --ike"
                if [[ "$prev" == @(-c|--child|-i|--ike) ]]
                then
                    return
                fi
            ;;
            -t|--terminate)
                options="-c --child -i --ike -C --child-id -I --ike-id -f
                --force -t --timeout"
                if [[ "$prev" == @(-c|--child|-i|--ike|-C|--child-id|-I|\
                    --ike-id|-f|--force|-t|--timeout) ]]
                then
                    return
                fi
            ;;
            -R|--rekey)
                options="-c --child -i ---ike -C --child-id -I --ike-id -a
                --reauth"
                if [[ "$prev" == @(-c|--child|-i|--ike|-C|--child-id|-I\
                    |--ike-id|-a|--reauth) ]]
                then
                    return
                fi
            ;;
            -d|--redirect)
                options="-i --ike -I --ike-id -p --peer-ip -d --peer-id -g
                --gateway"
                if [[ "$prev" == @(i|--ike|-I|--ike-id|-p|--peer-ip|-d|\
                    --peer-id|-g|--gateway) ]]
                then
                    return
                fi
            ;;
            -u|--uninstall|-p|--install)
                options="-c --child -i --ike"
                if [[ "$prev" == @(-c|--child|-i|--ike) ]]
                then
                    return
                fi
            ;;
            -l|--list-sas)
                options="-i --ike -I --ike-id"
                if [[ "$prev" == @(-i|--ike|-I|--ike-id) ]]
                then
                    return
                fi
            ;;
            -P|--list-pols)
                options="-c --child -t --trap -d --drop -p --pass"
                if [[ "$prev" == @(-c|--child|-t|--trap|-d|--drop|-p|--pass) ]]
                then
                    return
                fi
            ;;
            -B|--list-authorities)
                options="-n --name"
                if [[ "$prev" == @(-n|--name) ]]
                then
                    return
                fi
            ;;
            -x|--list-certs)
                options="-s --subject -t --type -f --flag -p --pem -S --short -U --utc"
                if [[ "$prev" == @(-s|--subject|-p|--pem|-U|--utc) ]]
                then
                    return
                fi
                if [[ "$prev" == @(-t|--type) ]]
                then
                    COMPREPLY=(x509 x509_ac x509_crl ocsp_response pubkey)
                    return
                fi
                if [[ "$prev" == @(-f|--flag) ]]
                then
                    COMPREPLY=(none ca aa ocsp any)
                    return
                fi
            ;;
            -A|--list-pools)
                options="-l --leases -n --name -f --file"
                if [[ "$prev" == @(-n|--name) ]]
                then
                    return
                fi
                if [[ "$prev" == @(-f|--file) ]]
                then
                    _filedir
                    return
                fi
            ;;
            -f|--flush-certs)
                options="-t --type"
                if [[ "$prev" == @(-t|--type) ]]
                then
                    COMPREPLY=(x509 x509_ac x509_crl ocsp_response pubkey)
                    return
                fi
            ;;
            -q|--load-all)
                options="-c --clear -n --noprompt -f --file"
                if [[ "$prev" == @(-f|--file) ]]
                then
                    _filedir
                    return
                fi                
            ;;
            -b|--load-authorities)
            options="-f --file"
                if [[ "$prev" == @(-f|--file) ]]
                then
                    _filedir
                    return
                fi
            ;;
            -c|--load-conns)
                options="-f --file"
                if [[ "$prev" == @(-f|--file) ]]
                then
                    _filedir
                    return
                fi
            ;;
            -s|--load-creds)
                options="-c --clear -n --noprompt -f --file"
                if [[ "$prev" == @(-f|--file) ]]
                then
                    _filedir
                    return
                fi
            ;;
            -a|--load-pools)
                options="-c --clear -n --noprompt -f --file"
                if [[ "$prev" == @(-f|--file) ]]
                then
                    _filedir
                    return
                fi
            ;;
            -v|--version)
                options="-d --daemon"
                return
            ;;
        esac
        # catch general options
        case "$prev" in
            -h|--help)
                return
            ;;
            -r|--raw|-P|--pretty)
                return
            ;;
            -u|--uri)
                _known_hosts_real -- "$cur"
                return
            ;;
            -+|--options)
                _filedir
                return
            ;;
            -v|--debug)
                COMPREPLY=(-1 0 1 2 3 4)
                return
            ;;
        esac
        options+=" $general_options"
        COMPREPLY=( $(compgen -W "$options" -- "$cur") )
    fi
} &&
complete -o nosort -F _swanctl swanctl