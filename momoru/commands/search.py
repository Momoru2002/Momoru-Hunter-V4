# momoru/commands/search.py
import click
from rich.console import Console
from momoru.themes.cyberpunk import cyberpunk_theme
from momoru.config import CONFIG
from momoru.core.plugin_loader import PluginLoader
from momoru.core.scanner import BuzzerScanner
from momoru.core.statistics import TrustEvaluator

# Pastikan console menggunakan standar tema cyberpunk yang seragam
console = Console(theme=cyberpunk_theme)

@click.command()
@click.argument("username")
@click.option("--platform", default="tiktok", help="Target social media app layer")
def cli(username, platform):
    """Scan and dissect malicious signature patterns from a specific user profile."""
    console.print(f"\n[accent]🏃 RUNNING CYBERNETIC RADAR SCANNERS FOR SYSTEM LAYER @{username}...[/accent]")
    
    plugin = PluginLoader.load_plugin(platform)
    if not plugin:
        console.print(f"[danger][!] Plugin untuk platform '{platform}' gagal dimuat atau tidak ditemukan![/danger]")
        return

    # Menarik komentar nyata secara dinamis lewat engine browser
    comments = plugin.fetch_comments(username)
    
    # Berikan parameter ambang batas kemiripan bahasa (similarity score) dari config.yaml ke scanner
    min_score = CONFIG["intelligence"].get("min_similarity_score", 0.75)
    scanner = BuzzerScanner(comments, username, threshold=min_score)
    
    evaluator = TrustEvaluator(scanner)
    metrics = evaluator.generate_metrics()

    console.print("\n[accent]─── REPORT RADAR SCAN ANALYSIS ───[/accent]")
    console.print(f"Target Account    : [info]{metrics['username']}[/info]")
    console.print(f"Similarity Range  : [warning]{metrics['similarity_index']}[/warning]")
    
    # Ambil batas persentase indikator buzzer (default: 75%)
    if metrics['confidence_score'] >= (min_score * 100):
        console.print(f"Buzzer Match Ratio: [danger]{metrics['confidence_score']}%[/danger]")
        console.print(f"Classification    : [danger]{metrics['status']}[/danger]")
    else:
        console.print(f"Buzzer Match Ratio: [success]{metrics['confidence_score']}%[/success]")
        console.print(f"Classification    : [success]{metrics['status']}[/success]")
    console.print("[accent]─────────────────────────────────────────[/accent]\n")