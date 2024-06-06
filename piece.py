class Piece(int):
    CHARS = {
        'color': ('light', 'dark'),
        'shape': ('square', 'circle'),
        'size': ('small', 'big'),
        'top': ('empty', 'full')
    }

    def __str__(self):
        description = 'Piece'
        for i, (characteristic, values) in enumerate(self.CHARS.items()):
            description += f', {characteristic}: {values[self >> i & 1]}'
        return description

if __name__ == '__main__':
    for i in range(16):
        print(Piece(i))
