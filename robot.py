import yaml
from pathlib import Path
from playwright.sync_api import sync_playwright


class Robot:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.filepath = Path(f"test/{name}.yaml")
        self.config = None
        self.load()
        self.driver = None
        self.browser = None
        self.page = None
        self.launch()

        self.locator = None

    def launch(self):
        self.driver = sync_playwright().start()
        # Use playwright.chromium, playwright.firefox or playwright.webkit
        # Pass headless=False to launch() to see the browser UI
        self.browser = self.driver.chromium.launch(headless=False, slow_mo=100)
        # launch browser max size
        self.browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        self.page = self.browser.new_page()
        self.page.goto(self.url)
        # page.screenshot(path="example.png")

    def close(self):
        self.browser.close()
        self.driver.stop()

    def load(self):
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {
                "main": {
                    "params": {
                        "url": self.url
                    },
                    "steps": []
                }
            }
    
    def save(self):
        with open(self.filepath, "w") as f:
            yaml.dump(self.config, f)

    def add_step(self, step: dict):
        self.config["main"]["steps"].append(step)
        self.save()

    def get_steps(self):
        return self.config["main"]["steps"]

    def get_driver(self):
        return self.driver

    def set_locator(self, xpath):
        self.locator = self.page.locator(xpath)

    def get_locator(self):
        return self.locator