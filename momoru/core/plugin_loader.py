import importlib
import os
from momoru.logger import CyberpunkLogger

class PluginLoader:
    @staticmethod
    def load_plugin(platform_name: str):
        try:
            module_path = f"momoru.plugins.{platform_name.lower()}"
            module = importlib.import_module(module_path)
            return module.PluginInstance()
        except ModuleNotFoundError:
            CyberpunkLogger.error(f"Plugin for platform '{platform_name}' not found.")
            return None