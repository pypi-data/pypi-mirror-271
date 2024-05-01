from lytils import ctext


class GSpreadNotInstalled(Exception):
    # Raise this when undetected_chromedriver is not installed
    def __init__(
        self,
        message="<y>Module 'gspread' not installed.",
    ):
        self.message = ctext(message)
        super().__init__(self.message)
