alias j='atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases --verbose=info'
alias fj='poetry run bin/huffmanize_zsh_aliases.py --verbose=debug'
alias d='poetry run python'
alias lj='atuin history list --format="{command}" | poetry run huffmanize-zsh-aliases'
alias s='poetry run local-harps'
alias kj='poetry run scripts/run_all.sh'
alias kf='atuin history list --format="{command}" --cwd | poetry run huffmanize-zsh-aliases --verbose=debug'
