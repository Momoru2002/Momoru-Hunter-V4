# momoru/themes/cyberpunk.py
from rich.theme import Theme
from rich.console import Console

# 1. Definisikan skema warna global kita
cyberpunk_theme = Theme({
    "danger": "bold red",
    "info": "bold cyan",
    "accent": "bold magenta",
    "success": "bold green",
    "warning": "bold yellow",
    "muted": "dim white"
})

# 2. Instansiasi objek console dengan tema di atas agar bisa di-import file lain
console = Console(theme=cyberpunk_theme)