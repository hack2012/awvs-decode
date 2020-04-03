#!/usr/bin/env python3
import struct, zlib, os, datetime

mask, pos = 2 ** 32 - 16, 32
base_path = os.path.abspath("awvs_script_blob_decode_" + datetime.date.today().isoformat())
with open('wvsc_blob.bin', 'rb') as fp:
    s = fp.read()
    while pos < len(s):
        file_len = struct.unpack('<I', s[pos:pos + 4])[0]
        d = zlib.decompress(s[pos + 4: pos + 4 + file_len])
        path_len = ord(struct.unpack('<c', d[1:2])[0])
        path = os.path.join(base_path, bytes.decode(d[2 + 1: 2 + path_len]))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(d[2 + path_len + 1 + 2 + (1 if (len(d) - path_len - 3) > 2 ** 14 else 0) +
                                 (1 if (len(d) - path_len - 3) > 2 ** 21 else 0):])
        pos += ((file_len + 4) & mask) + 16
