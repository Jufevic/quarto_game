class Piece(int):
    CHARS = {
        'color': ('light', 'dark'),
        'shape': ('square', 'circle'),
        'size': ('small', 'big'),
        'top': ('empty', 'full')
    }

    def __str__(self):
        characteristics = []
        for i, (characteristic, values) in enumerate(self.CHARS.items()):
            characteristics.append(f'{values[self >> i & 1]} {characteristic}')
        return 'Piece: ' + ', '.join(characteristics)

if __name__ == '__main__':
    for i in range(16):
        print(Piece(i))
