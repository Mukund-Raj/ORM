class Fields:
    def __init__(self,**kwargs) -> None:
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.is_nullable = True if kwargs.get('is_nullable') == "YES" else False
        self.char_length = kwargs.get('char_length')
        self.num_precision = kwargs.get('num_precision')

    def __str__(self) -> str:
        return f"""
        Column name is {self.name}, 
        {self.type},
        {self.is_nullable},
        {self.char_length},
        {self.num_precision}
        """