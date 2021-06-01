class EntryModel:
    def __init__(self, entry_id=None, title='', preamble='', main_text='', chars_count=0):
        self.entry_id = entry_id
        self.title = title
        self.preamble = preamble
        self.main_text = main_text
        self.chars_count = chars_count

