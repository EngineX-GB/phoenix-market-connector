class PageData:

    def __init__(self, page_number, page_size, total_count, total_pages):
        self.page_number = page_number
        self.page_size = page_size
        self.total_count = total_count
        self.total_pages = total_pages

    def get_total_pages(self):
        return self.total_pages

    def get_page_number(self):
        return self.page_number