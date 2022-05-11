

class LatexToken:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.source = ""
    
    def is_text(self):
        return self.name == "TEXT" or self.name == "NAME"
    def is_operator(self):
        return not self.is_text()

    def set_pos (self, start, length):
        self.start = start
        self.length = length

        return self
    def set_source(self, string):
        self.source = string

        return self
    def validate_name(self):
        can_be_name = self.name == "NAME"
        if not can_be_name:
            return self

        for chr in self.value:
            if chr.isspace():
                can_be_name = False
                break
        
        self.name = "NAME" if can_be_name else "TEXT"
        return self
    
    def __str__(self):
        return self.name + ":" + str(self.value)
