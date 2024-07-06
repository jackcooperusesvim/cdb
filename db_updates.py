
class db_field():
    def __init__(self,id: str,t: type):
        self.id = id
        self.type = t
    def __str__(self) -> str:
        return self.id
