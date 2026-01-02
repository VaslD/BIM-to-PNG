#!/usr/bin/env python3

from oodle import OodleDecompressor
from os import SEEK_END
from os.path import splitext
from PIL import Image
from struct import unpack
from texture2ddecoder import decode_bc1, decode_bc5
import sys

# FIXME: Change oo2core.dll path
OO2CORE_LIBRARY_PATH=r'C:\Program Files (x86)\Steam\steamapps\common\DOOM Eternal\oo2core_8_win64.dll'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('No command-line argument.')

    for path in sys.argv[1:]:
        with open(path, 'rb+') as file:
            if file.peek(8)[:8] == b'DIVINITY':
                # Convert Divinity-compressed textures with Oodle
                assert file.read(8) == b'DIVINITY'
                size: int = unpack('<q', file.read(8))[0]
                decompressor = OodleDecompressor(OO2CORE_LIBRARY_PATH)
                decompressed = decompressor.decompress(file.read(), size)
                assert isinstance(decompressed, bytes)
                assert decompressed[:3] == b'BIM'
                file.seek(0)
                assert file.write(decompressed) == len(decompressed)
                file.truncate()
                file.seek(0)

            # Read Doom Eternal BIM
            assert file.read(3) == b'BIM'
            header = file.read(60)
            texture: int = unpack('<i', header[1:5])[0]
            width: int = unpack('<i', header[9:13])[0]
            height: int = unpack('<i', header[13:17])[0]
            maps: int = unpack('<i', header[21:25])[0]
            format: int = unpack('<i', header[38:42])[0]
            print(f"Width:  {width}")
            print(f"Height: {height}")
            print(f"Type:   {texture}")
            print(f"Format: {format}")

            # Get LOD0 image
            level = 0
            size = 0
            for i in range(maps):
                header = file.read(36)
                assert unpack('<q', header[:8])[0] == level
                if level == 0:
                    size = unpack('<i', header[20:24])[0]
                    assert unpack('<i', header[24:28])[0] != 1
                    print(f"Size:   {size}")
                level += 1

            image = file.read(size)
            match format:
                case 25:
                    image = decode_bc5(image, width, height)
                    image = Image.frombytes('RGBA', (width, height), image, 'raw', ('BGRA'))
                    assert image.width == width
                    assert image.height == height
                case 33:
                    image = decode_bc1(image, width, height)
                    image = Image.frombytes('RGBA', (width, height), image, 'raw', ('BGRA'))
                    assert image.width == width
                    assert image.height == height
                case _:
                    raise ValueError('Format not supported.')
            path = f'{splitext(path)[0]}.png'
            image.save(path, 'PNG', optimize=True)
            print(f'Wrote:  "{path}"')
            print()
