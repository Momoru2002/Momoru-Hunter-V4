import click
from momoru.core.plugin_loader import PluginLoader
from momoru.core.scanner import BuzzerScanner
from momoru.core.statistics import TrustEvaluator
from momoru.exporters.json_exporter import JsonExporter
from momoru.exporters.html_exporter import HtmlExporter

@click.command()
@click.argument("username")
@click.option("--format", type=click.Choice(['json', 'html']), default='json')
@click.option("--platform", default="tiktok")
@click.option("--out", default="report_output")
def cli(username, format, platform, out):
    """Dossier compilation command layer."""
    plugin = PluginLoader.load_plugin(platform)
    if not plugin: return
    
    comments = plugin.fetch_comments(username)
    metrics = TrustEvaluator(BuzzerScanner(comments, username)).generate_metrics()
    
    if format == 'json':
        JsonExporter.export(metrics, f"{out}.json")
    elif format == 'html':
        HtmlExporter.export(metrics, f"{out}.html")