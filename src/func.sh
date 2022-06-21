goto() {
    cmd=$(gotocfg.py prepare-cd -k "$1")
    echo "$cmd"
    if [ ${cmd:0:2} = "cd" ]
    then
        eval "$cmd"
    fi
}

goto-add() {
    gotocfg.py set-path -k "$1" -p "$2"
}

goto-list() {
    gotocfg.py list-paths
}

goto-add-current() {
    gotocfg.py set-path -k "$1" -p "$(pwd)"
}
