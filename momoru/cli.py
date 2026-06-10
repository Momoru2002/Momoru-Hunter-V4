# momoru/cli.py
import click
import sys
from rich.console import Console
from momoru.themes.cyberpunk import cyberpunk_theme
from momoru.commands import search, report, export, config_cmd

# Inisialisasi console menggunakan tema cyberpunk kita
console = Console(theme=cyberpunk_theme)

def display_banner():
    """Fungsi untuk nge-render banner cyberpunk dengan paduan warna Merah dan Biru/Cyan."""
    
    # Bagian ASCII Art (Warna Merah Neon)
    ascii_art = """
[danger]███╗   ███╗ ██████╗ ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗[/danger]
[danger]████╗ ████║██╔═══██╗████╗ ████║██╔═══██╗██╔══██╗██║   ██║[/danger]
[danger]██╔████╔██║██║   ██║██╔████╔██║██║   ██║██████╔╝██║   ██║[/danger]
[danger]██║╚██╔╝██║██║   ██║██║╚██╔╝██║██║   ██║██╔══██╗██║   ██║[/danger]
[danger]██║ ╚═╝ ██║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝██║  ██║╚██████╔╝[/danger]
[danger]╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝[/danger]\
"""

    # Bagian Pembatas Garis Digital (Warna Biru/Cyan)
    divider = "[info] █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ [/info]\n[info] ╚══╝  ╚══╝  ╚══╝  ╚══╝  ╚══╝  ╚══╝  ╚══╝  ╚══╝  ╚══╝  ╚══╝[/info]"
    
    # Bagian Metadata Info
    metadata = f"""
        [accent]🚨 AUTOMATED ANTI-BUZZER INTELLIGENCE SYSTEM 🚨[/accent]

[danger][+][/danger] [info]Version[/info] : 4.0.0
[danger][+][/danger] [info]Author[/info]  : MOMORU
[danger][+][/danger] [info]Target[/info]  : Buzzer Mitigation & Sybil Attacker
[danger][+][/danger] [info]Github[/info]  : https://github.com/Momoru2002

[danger]────────────────────────────────────────────────────────────[/danger]
[accent]CHALLENGE THE MANIPULATION • PROTECT THE GENERATION[/accent]
[danger]────────────────────────────────────────────────────────────[/danger]
"""
    
    # Print ke terminal
    console.print(ascii_art)
    console.print(divider)
    console.print(metadata)

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    """Momoru Hunter V4: Tactical Anti-Buzzer Forensics Command Engine."""
    # Banner selalu dimunculkan sebagai core interface init di baris pertama
    display_banner()
    
    # Jika user cuma ngetik 'py momoru/cli.py' tanpa sub-command,
    # munculkan panduan menu help otomatis tepat di bawah banner.
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())

# Daftarkan command-command modular kita ke gateway CLI utama
main.add_command(search.cli, name="search")
main.add_command(report.cli, name="report")
main.add_command(export.cli, name="export")
main.add_command(config_cmd.cli, name="config")

if __name__ == "__main__":
    main()