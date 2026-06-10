# momoru/logger.py
import logging
from momoru.themes.cyberpunk import console

class CyberpunkLogger:
    """Utility class untuk menjembatani standard logging Python ke Rich Console."""
    
    @staticmethod
    def info(message: str):
        console.print(f"[info][*] INFO:[/info] [muted]{message}[/muted]")

    @staticmethod
    def success(message: str):
        console.print(f"[success][+] SUCCESS:[/success] {message}")

    @staticmethod
    def danger(message: str):
        console.print(f"[danger][!] ERROR:[/danger] [danger]{message}[/danger]")

    @staticmethod
    def warning(message: str):
        console.print(f"[warning][─] WARNING:[/warning] {message}")