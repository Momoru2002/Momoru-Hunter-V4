# momoru/commands/config_cmd.py
import click
from rich.console import Console
from momoru.themes.cyberpunk import cyberpunk_theme
from momoru.config import CONFIG

console = Console(theme=cyberpunk_theme)

@click.group()
def cli():
    """Manage application assets configurations."""
    pass

@cli.command(name="show")
def show_config():
    """Show current active configuration parameters safely."""
    console.print("\n[accent]─── ACTIVE CONFIGURATION MONITOR ───[/accent]")
    
    # Tampilkan konfigurasi aplikasi umum
    console.print(f"Debug Mode   : [info]{CONFIG['app'].get('debug')}[/info]")
    console.print(f"Timeout      : [info]{CONFIG['app'].get('timeout')}s[/info]")
    console.print(f"Headless Bot : [info]{CONFIG['app'].get('headless')}[/info]")
    
    # Tampilkan intelijen metadata
    intel = CONFIG.get("intelligence", {})
    console.print(f"Min Score    : [warning]{intel.get('min_similarity_score')}[/warning]")
    console.print(f"Templates Loaded: [info]{len(intel.get('templates', []))}[/info]")
    
    # Tampilkan jumlah akun tumbal tanpa membocorkan password/email asli (Sangat Aman)
    accounts = CONFIG.get("accounts", [])
    console.print(f"Active Accounts : [success]{len(accounts)} Entities Loaded[/success]")
    
    if CONFIG["app"].get("debug"):
        console.print("\n[muted][*] Active Accounts List (Masked):[/muted]")
        for acc in accounts:
            console.print(f"  - Username: [info]{acc['username']}[/info] | Proxy: [muted]{acc['proxy'] if acc['proxy'] else 'No Proxy'}[/muted]")
            
    console.print("[accent]──────────────────────────────────────[/accent]\n")