class Player:
    def __init__(self, my_id, name, color):
        self.id = my_id
        self.name = name
        self.color = color

    def __eq__(self, other) -> bool:
        return other is not None and other.id == self.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'Player(id: {self.id}; name: {self.name}; color: {self.color})'

    def __repr__(self):
        return str(self)
