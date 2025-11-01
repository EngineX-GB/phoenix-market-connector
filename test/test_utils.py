
class TestUtils:

    def __init__(self):
        pass

    @staticmethod
    def generate_test_file(directory, filename, text: str):
        feed = open(directory + "/" + filename, 'w', encoding='utf-8')
        feed.write(text)
        feed.close()

