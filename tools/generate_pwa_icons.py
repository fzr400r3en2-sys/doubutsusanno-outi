import math
import struct
import zlib
from pathlib import Path


COLORS = {
    "ink": (77, 57, 45, 255),
    "paper": (255, 249, 232, 255),
    "sky": (191, 227, 239, 255),
    "grass": (159, 202, 101, 255),
    "leaf": (95, 173, 112, 255),
    "sun": (255, 215, 106, 255),
    "button": (244, 154, 90, 255),
    "white": (255, 255, 255, 255),
}


class Canvas:
    def __init__(self, size, scale=3):
        self.size = size
        self.scale = scale
        self.width = size * scale
        self.height = size * scale
        self.pixels = [[COLORS["paper"] for _ in range(self.width)] for _ in range(self.height)]

    def point(self, x, y, color):
        ix = int(round(x * self.scale))
        iy = int(round(y * self.scale))
        if 0 <= ix < self.width and 0 <= iy < self.height:
            self.pixels[iy][ix] = color

    def fill_rect(self, x1, y1, x2, y2, color):
        left = max(0, int(math.floor(x1 * self.scale)))
        right = min(self.width, int(math.ceil(x2 * self.scale)))
        top = max(0, int(math.floor(y1 * self.scale)))
        bottom = min(self.height, int(math.ceil(y2 * self.scale)))
        for y in range(top, bottom):
            row = self.pixels[y]
            for x in range(left, right):
                row[x] = color

    def fill_circle(self, cx, cy, radius, color):
        cx *= self.scale
        cy *= self.scale
        radius *= self.scale
        left = max(0, int(cx - radius))
        right = min(self.width, int(cx + radius) + 1)
        top = max(0, int(cy - radius))
        bottom = min(self.height, int(cy + radius) + 1)
        limit = radius * radius
        for y in range(top, bottom):
            row = self.pixels[y]
            for x in range(left, right):
                if (x - cx) ** 2 + (y - cy) ** 2 <= limit:
                    row[x] = color

    def fill_polygon(self, points, color):
        scaled = [(x * self.scale, y * self.scale) for x, y in points]
        min_y = max(0, int(math.floor(min(y for _, y in scaled))))
        max_y = min(self.height - 1, int(math.ceil(max(y for _, y in scaled))))

        for y in range(min_y, max_y + 1):
            intersections = []
            for index, (x1, y1) in enumerate(scaled):
                x2, y2 = scaled[(index + 1) % len(scaled)]
                if y1 == y2:
                    continue
                if (y >= min(y1, y2)) and (y < max(y1, y2)):
                    intersections.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
            intersections.sort()
            for start, end in zip(intersections[0::2], intersections[1::2]):
                left = max(0, int(math.floor(start)))
                right = min(self.width - 1, int(math.ceil(end)))
                for x in range(left, right + 1):
                    self.pixels[y][x] = color

    def stroke_line(self, x1, y1, x2, y2, width, color):
        steps = int(max(abs(x2 - x1), abs(y2 - y1)) * self.scale)
        radius = width / 2
        for step in range(steps + 1):
            t = step / max(1, steps)
            self.fill_circle(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, radius, color)

    def downsample(self):
        rows = []
        for y in range(self.size):
            row = bytearray()
            for x in range(self.size):
                total = [0, 0, 0, 0]
                for sy in range(self.scale):
                    for sx in range(self.scale):
                        pixel = self.pixels[y * self.scale + sy][x * self.scale + sx]
                        for channel in range(4):
                            total[channel] += pixel[channel]
                area = self.scale * self.scale
                row.extend(channel // area for channel in total)
            rows.append(bytes(row))
        return rows


def png_chunk(name, data):
    chunk_type = name.encode("ascii")
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)


def write_png(path, size, rows):
    raw = b"".join(b"\x00" + row for row in rows)
    payload = b"".join([
        b"\x89PNG\r\n\x1a\n",
        png_chunk("IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)),
        png_chunk("IDAT", zlib.compress(raw, 9)),
        png_chunk("IEND", b""),
    ])
    path.write_bytes(payload)


def draw_icon(size):
    canvas = Canvas(size)
    canvas.fill_rect(0, 0, size, size, COLORS["sky"])
    canvas.fill_rect(0, size * 0.58, size, size, COLORS["grass"])

    canvas.fill_circle(size * 0.78, size * 0.22, size * 0.12, COLORS["sun"])
    canvas.fill_circle(size * 0.78, size * 0.22, size * 0.085, COLORS["white"])
    canvas.fill_circle(size * 0.78, size * 0.22, size * 0.065, COLORS["sun"])

    house_left = size * 0.22
    house_right = size * 0.76
    house_top = size * 0.42
    house_bottom = size * 0.78
    canvas.fill_polygon([(size * 0.18, house_top), (size * 0.49, size * 0.18), (size * 0.82, house_top)], COLORS["ink"])
    canvas.fill_polygon([(size * 0.24, house_top), (size * 0.49, size * 0.25), (size * 0.75, house_top)], COLORS["button"])
    canvas.fill_rect(house_left, house_top, house_right, house_bottom, COLORS["ink"])
    canvas.fill_rect(size * 0.27, size * 0.47, size * 0.71, size * 0.77, COLORS["paper"])
    canvas.fill_circle(size * 0.49, size * 0.64, size * 0.12, COLORS["ink"])
    canvas.fill_circle(size * 0.49, size * 0.64, size * 0.085, COLORS["white"])

    canvas.fill_circle(size * 0.39, size * 0.59, size * 0.075, COLORS["ink"])
    canvas.fill_circle(size * 0.59, size * 0.59, size * 0.075, COLORS["ink"])
    canvas.fill_circle(size * 0.39, size * 0.59, size * 0.044, COLORS["leaf"])
    canvas.fill_circle(size * 0.59, size * 0.59, size * 0.044, COLORS["leaf"])
    canvas.fill_circle(size * 0.49, size * 0.69, size * 0.03, COLORS["ink"])
    canvas.stroke_line(size * 0.43, size * 0.72, size * 0.49, size * 0.75, size * 0.025, COLORS["ink"])
    canvas.stroke_line(size * 0.55, size * 0.72, size * 0.49, size * 0.75, size * 0.025, COLORS["ink"])

    return canvas.downsample()


def main():
    icon_dir = Path(__file__).resolve().parents[1] / "assets" / "icons"
    icon_dir.mkdir(parents=True, exist_ok=True)
    for name, size in (("icon-192.png", 192), ("apple-touch-icon.png", 180), ("icon-512.png", 512)):
        write_png(icon_dir / name, size, draw_icon(size))
        print(icon_dir / name)


if __name__ == "__main__":
    main()
