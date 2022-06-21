# goto
Shell tool to quick-cd to desired directories

## Installation
An "real" installation is not available.
Add the repo to the path and source the functions.
```
GOTO_ROOT="/path/to/goto/src"
export PATH="${PATH}:${GOTO_ROOT}"
source "${GOTO_ROOT}/func.sh"
```

## Usage
Add a new directory:
`goto-add key /path/to/dir`

Add the current directory:
`goto-add-current key`

List known directories
`goto-list`

Actually switch to a directory
`goto key`
