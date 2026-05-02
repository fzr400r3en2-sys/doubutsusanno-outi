import argparse
import html
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from resolve_public_url import resolve_public_url


ECL_MEDIUM = 1
APP_VERSION = "4"
FORMAT_BITS = (1, 0, 3, 2)
ECC_CODEWORDS_PER_BLOCK = (
    (),
    (7, 10, 13, 17),
    (10, 16, 22, 28),
    (15, 26, 18, 22),
    (20, 18, 26, 16),
    (26, 24, 18, 22),
    (18, 16, 24, 28),
    (20, 18, 18, 26),
    (24, 22, 22, 26),
    (30, 22, 20, 24),
    (18, 26, 24, 28),
)
NUM_ERROR_CORRECTION_BLOCKS = (
    (),
    (1, 1, 1, 1),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 2, 4),
    (1, 2, 4, 4),
    (2, 4, 4, 4),
    (2, 4, 6, 5),
    (2, 4, 6, 6),
    (2, 5, 8, 8),
    (4, 5, 8, 8),
)


def append_bits(bits, value, length):
    for index in range(length - 1, -1, -1):
        bits.append((value >> index) & 1)


def raw_data_modules(version):
    result = (16 * version + 128) * version + 64
    if version >= 2:
        num_align = version // 7 + 2
        result -= (25 * num_align - 10) * num_align - 55
        if version >= 7:
            result -= 36
    return result


def raw_data_codewords(version):
    return raw_data_modules(version) // 8


def data_codeword_count(version, ecl):
    return raw_data_codewords(version) - ECC_CODEWORDS_PER_BLOCK[version][ecl] * NUM_ERROR_CORRECTION_BLOCKS[version][ecl]


def make_data_codewords(text, version, ecl):
    data = text.encode("utf-8")
    count_bits = 8 if version <= 9 else 16
    capacity_bits = data_codeword_count(version, ecl) * 8
    bits = []

    if len(data) >= (1 << count_bits):
        return None

    append_bits(bits, 0x4, 4)
    append_bits(bits, len(data), count_bits)
    for byte in data:
        append_bits(bits, byte, 8)

    if len(bits) > capacity_bits:
        return None

    append_bits(bits, 0, min(4, capacity_bits - len(bits)))
    while len(bits) % 8:
        bits.append(0)

    result = []
    for start in range(0, len(bits), 8):
        value = 0
        for bit in bits[start:start + 8]:
            value = (value << 1) | bit
        result.append(value)

    pad_byte = 0xEC
    while len(result) < data_codeword_count(version, ecl):
        result.append(pad_byte)
        pad_byte ^= 0xEC ^ 0x11

    return result


def choose_version(text, ecl):
    for version in range(1, len(ECC_CODEWORDS_PER_BLOCK)):
        codewords = make_data_codewords(text, version, ecl)
        if codewords is not None:
            return version, codewords
    raise ValueError("URL is too long for this QR generator. Use a shorter public URL.")


def make_gf_tables():
    exp = [0] * 512
    log = [0] * 256
    value = 1
    for index in range(255):
        exp[index] = value
        log[value] = index
        value <<= 1
        if value & 0x100:
            value ^= 0x11D
    for index in range(255, 512):
        exp[index] = exp[index - 255]
    return exp, log


GF_EXP, GF_LOG = make_gf_tables()


def gf_multiply(left, right):
    if left == 0 or right == 0:
        return 0
    return GF_EXP[GF_LOG[left] + GF_LOG[right]]


def reed_solomon_generator(degree):
    result = [0] * (degree - 1) + [1]
    root = 1
    for _ in range(degree):
        for index in range(degree):
            result[index] = gf_multiply(result[index], root)
            if index + 1 < degree:
                result[index] ^= result[index + 1]
        root = gf_multiply(root, 0x02)
    return result


def reed_solomon_remainder(data, generator):
    result = [0] * len(generator)
    for byte in data:
        factor = byte ^ result.pop(0)
        result.append(0)
        for index, coefficient in enumerate(generator):
            result[index] ^= gf_multiply(coefficient, factor)
    return result


def add_ecc_and_interleave(data, version, ecl):
    block_count = NUM_ERROR_CORRECTION_BLOCKS[version][ecl]
    block_ecc_len = ECC_CODEWORDS_PER_BLOCK[version][ecl]
    raw_count = raw_data_codewords(version)
    short_block_count = block_count - raw_count % block_count
    short_block_len = raw_count // block_count
    generator = reed_solomon_generator(block_ecc_len)
    blocks = []
    offset = 0

    for index in range(block_count):
        data_len = short_block_len - block_ecc_len
        if index >= short_block_count:
            data_len += 1

        block_data = list(data[offset:offset + data_len])
        offset += data_len
        ecc = reed_solomon_remainder(block_data, generator)
        if index < short_block_count:
            block_data.append(0)
        blocks.append(block_data + ecc)

    result = []
    for index in range(len(blocks[0])):
        for block_index, block in enumerate(blocks):
            if index != short_block_len - block_ecc_len or block_index >= short_block_count:
                result.append(block[index])

    return result


class QRMatrix:
    def __init__(self, version):
        self.version = version
        self.size = version * 4 + 17
        self.modules = [[False] * self.size for _ in range(self.size)]
        self.functions = [[False] * self.size for _ in range(self.size)]

    def set_function(self, x, y, dark):
        self.modules[y][x] = bool(dark)
        self.functions[y][x] = True

    def set_module(self, x, y, dark):
        self.modules[y][x] = bool(dark)

    def draw_finder(self, x, y):
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                xx = x + dx
                yy = y + dy
                if 0 <= xx < self.size and 0 <= yy < self.size:
                    distance = max(abs(dx), abs(dy))
                    self.set_function(xx, yy, distance <= 1 or distance == 3)

    def draw_alignment(self, x, y):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                distance = max(abs(dx), abs(dy))
                self.set_function(x + dx, y + dy, distance != 1)

    def alignment_positions(self):
        if self.version == 1:
            return []
        count = self.version // 7 + 2
        step = 26 if self.version == 32 else ((self.version * 4 + count * 2 + 1) // (count * 2 - 2)) * 2
        return [6] + [self.size - 7 - index * step for index in range(count - 2, -1, -1)]

    def draw_function_patterns(self):
        self.draw_finder(3, 3)
        self.draw_finder(self.size - 4, 3)
        self.draw_finder(3, self.size - 4)

        for index in range(8, self.size - 8):
            dark = index % 2 == 0
            self.set_function(6, index, dark)
            self.set_function(index, 6, dark)

        positions = self.alignment_positions()
        for y in positions:
            for x in positions:
                if not ((x == 6 and y == 6) or (x == 6 and y == self.size - 7) or (x == self.size - 7 and y == 6)):
                    self.draw_alignment(x, y)

        for index in range(9):
            if index != 6:
                self.set_function(8, index, False)
                self.set_function(index, 8, False)

        for index in range(8):
            self.set_function(self.size - 1 - index, 8, False)
            self.set_function(8, self.size - 1 - index, False)

        self.set_function(8, self.size - 8, True)

        if self.version >= 7:
            self.draw_version()

    def draw_version(self):
        remainder = self.version
        for _ in range(12):
            remainder = (remainder << 1) ^ ((remainder >> 11) * 0x1F25)
        bits = (self.version << 12) | remainder

        for index in range(18):
            bit = (bits >> index) & 1
            a = self.size - 11 + index % 3
            b = index // 3
            self.set_function(a, b, bit)
            self.set_function(b, a, bit)

    def draw_format(self, ecl, mask):
        data = (FORMAT_BITS[ecl] << 3) | mask
        remainder = data
        for _ in range(10):
            remainder = (remainder << 1) ^ ((remainder >> 9) * 0x537)
        bits = ((data << 10) | remainder) ^ 0x5412

        for index in range(6):
            self.set_function(8, index, (bits >> index) & 1)
        self.set_function(8, 7, (bits >> 6) & 1)
        self.set_function(8, 8, (bits >> 7) & 1)
        self.set_function(7, 8, (bits >> 8) & 1)
        for index in range(9, 15):
            self.set_function(14 - index, 8, (bits >> index) & 1)

        for index in range(8):
            self.set_function(self.size - 1 - index, 8, (bits >> index) & 1)
        for index in range(8, 15):
            self.set_function(8, self.size - 15 + index, (bits >> index) & 1)
        self.set_function(8, self.size - 8, True)

    def mask_bit(self, x, y, mask):
        if mask == 0:
            return (x + y) % 2 == 0
        if mask == 1:
            return y % 2 == 0
        if mask == 2:
            return x % 3 == 0
        if mask == 3:
            return (x + y) % 3 == 0
        if mask == 4:
            return (x // 3 + y // 2) % 2 == 0
        if mask == 5:
            return (x * y) % 2 + (x * y) % 3 == 0
        if mask == 6:
            return ((x * y) % 2 + (x * y) % 3) % 2 == 0
        return ((x + y) % 2 + (x * y) % 3) % 2 == 0

    def draw_codewords(self, codewords, mask):
        bits = []
        for byte in codewords:
            append_bits(bits, byte, 8)

        bit_index = 0
        right = self.size - 1
        while right >= 1:
            if right == 6:
                right -= 1
            for vert in range(self.size):
                upward = ((right + 1) & 2) == 0
                y = self.size - 1 - vert if upward else vert
                for column in range(2):
                    x = right - column
                    if self.functions[y][x]:
                        continue
                    dark = bit_index < len(bits) and bits[bit_index] == 1
                    if self.mask_bit(x, y, mask):
                        dark = not dark
                    self.set_module(x, y, dark)
                    bit_index += 1
            right -= 2


def encode_qr(text, ecl=ECL_MEDIUM, mask=0):
    version, data = choose_version(text, ecl)
    codewords = add_ecc_and_interleave(data, version, ecl)
    matrix = QRMatrix(version)
    matrix.draw_function_patterns()
    matrix.draw_codewords(codewords, mask)
    matrix.draw_format(ecl, mask)
    return matrix.modules


def svg_for_matrix(matrix, title, description, border=4):
    size = len(matrix)
    escaped_title = html.escape(title)
    escaped_description = html.escape(description)
    rects = []
    for y, row in enumerate(matrix):
        for x, dark in enumerate(row):
            if dark:
                rects.append(f"M{x + border},{y + border}h1v1h-1z")
    path_data = "".join(rects)
    view_size = size + border * 2
    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_size} {view_size}" role="img" aria-labelledby="title description">',
        f"  <title id=\"title\">{escaped_title}</title>",
        f"  <desc id=\"description\">{escaped_description}</desc>",
        '  <rect width="100%" height="100%" fill="#ffffff"/>',
        f'  <path fill="#4d392d" d="{path_data}"/>',
        "</svg>",
        "",
    ])


def write_qr(path, url, title):
    matrix = encode_qr(url)
    path.write_text(svg_for_matrix(matrix, title, url), encoding="utf-8")


def with_query(url, **params):
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(params)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def main():
    parser = argparse.ArgumentParser(description="Generate install QR codes for doubutsusanno-outi.")
    parser.add_argument("--base-url", help="Public URL. Defaults to DOUBUTSU_HOME_PUBLIC_URL or GitHub Pages.")
    parser.add_argument("--output-dir", type=Path, help="QR output directory.")
    args = parser.parse_args()

    app_root = Path(__file__).resolve().parents[1]
    output_dir = args.output_dir or app_root / "assets" / "install"
    output_dir.mkdir(parents=True, exist_ok=True)

    base_url = resolve_public_url(args.base_url)
    targets = {
        "iphone": with_query(base_url, install="iphone", v=APP_VERSION),
        "android": with_query(base_url, install="android", v=APP_VERSION),
    }

    write_qr(output_dir / "qr-iphone.svg", targets["iphone"], "iPhone QR code for doubutsusanno-outi")
    write_qr(output_dir / "qr-android.svg", targets["android"], "Android QR code for doubutsusanno-outi")

    for device, url in targets.items():
        print(f"{device}: {url}")


if __name__ == "__main__":
    main()
