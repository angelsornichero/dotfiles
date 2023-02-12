# Alias
alias ls='lsd --group-dirs=first'
alias cat='bat'

# Plugins
source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source /usr/share/zsh/plugins/sudo.plugin.zsh

# Starship
eval "$(starship init zsh)"
