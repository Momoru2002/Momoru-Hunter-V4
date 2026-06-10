class PluginInstance:
    def __init__(self):
        self.name = "Example"
    def fetch_comments(self, username: str): return []
    def fire_report(self, target: str, bot_account: dict): return True