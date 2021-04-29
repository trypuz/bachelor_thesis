class EntryModel:
    def __init__(self, entry_id=None, title='', preamble='', main_text='', words_count=0):
        self.entry_id = entry_id
        self.title = title
        self.preamble = preamble
        self.main_text = main_text
        self.words_count = words_count

