from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANIMALS = ROOT / "assets" / "animals"
HOMES = ROOT / "assets" / "homes"
PREVIEW = ROOT / "assets" / "preview.html"

SVG_HEADER = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img">\n'
SVG_FOOTER = "</svg>\n"


def svg(body):
    return SVG_HEADER + body.strip() + "\n" + SVG_FOOTER


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


STYLE = """
  <defs>
    <style>
      .line{stroke:#4d392d;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
      .thin{stroke:#4d392d;stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
      .none{fill:none}
    </style>
  </defs>
"""


ASSETS = {
    ANIMALS / "dog.svg": svg(
        STYLE
        + """
  <path class="line" fill="#f2bf72" d="M70 144c8-33 39-54 78-45 33 7 52 33 48 65-4 37-36 54-76 50-38-4-59-31-50-70z"/>
  <path class="line" fill="#f7cd8b" d="M58 92c-1-30 22-52 53-50 30 2 50 25 47 55-3 27-25 47-53 47-27 0-46-22-47-52z"/>
  <path class="line" fill="#9a6848" d="M57 73c-20 8-31 28-23 51 19 0 34-13 39-34z"/>
  <path class="line" fill="#9a6848" d="M144 72c22 5 37 23 34 47-18 4-36-7-44-27z"/>
  <path class="line" fill="#ffe4b0" d="M84 101c9-14 32-15 44-2 5 6 5 18-1 24-10 10-31 10-41 0-6-6-7-15-2-22z"/>
  <circle fill="#4d392d" cx="89" cy="87" r="6"/>
  <circle fill="#4d392d" cx="127" cy="87" r="6"/>
  <path class="thin none" d="M105 112c5 7 13 7 19 0"/>
  <path class="line none" d="M190 134c24-16 38-5 36 15"/>
  <path class="line none" d="M94 207v25"/>
  <path class="line none" d="M151 211v23"/>
  <path class="line" fill="#ef746f" d="M101 145c16 7 36 7 53-1v16c-17 8-36 8-53 0z"/>
  <circle fill="#4d392d" cx="113" cy="110" r="7"/>
"""
    ),
    ANIMALS / "cat.svg": svg(
        STYLE
        + """
  <path class="line" fill="#9ec3d5" d="M71 154c7-34 36-55 75-48 37 7 58 36 51 69-8 36-43 52-82 45-35-6-51-31-44-66z"/>
  <path class="line" fill="#b7d6e2" d="M64 85 82 43l31 28 31-28 19 43c13 33-9 64-50 65-40 1-62-30-49-66z"/>
  <path class="line" fill="#ffd3d2" d="m83 68 7-15 12 15z"/>
  <path class="line" fill="#ffd3d2" d="m132 68 12-15 7 15z"/>
  <circle fill="#4d392d" cx="95" cy="98" r="6"/>
  <circle fill="#4d392d" cx="133" cy="98" r="6"/>
  <path class="thin" fill="#f19a8d" d="m113 112 10 0-5 7z"/>
  <path class="thin none" d="M91 121c-16-3-27 1-35 7"/>
  <path class="thin none" d="M92 133c-15 1-25 7-31 15"/>
  <path class="thin none" d="M139 121c16-3 27 1 35 7"/>
  <path class="thin none" d="M138 133c15 1 25 7 31 15"/>
  <path class="line none" d="M186 149c37-9 54 14 37 36-11 14-34 11-38-5"/>
  <path class="line none" d="M101 215v20"/>
  <path class="line none" d="M153 216v19"/>
  <path class="thin none" d="M111 128c5 7 12 7 18 0"/>
"""
    ),
    ANIMALS / "bird.svg": svg(
        STYLE
        + """
  <path class="line" fill="#7ecbe8" d="M73 129c0-38 28-66 64-66 38 0 66 28 66 66 0 43-30 77-66 77s-64-34-64-77z"/>
  <path class="line" fill="#5aa5d6" d="M91 139c13-7 34-4 50 14-10 18-33 26-51 17-10-5-9-25 1-31z"/>
  <path class="line" fill="#ffe07b" d="m190 103 41 18-41 21z"/>
  <circle fill="#4d392d" cx="153" cy="101" r="7"/>
  <path class="thin none" d="M125 205v22"/>
  <path class="thin none" d="M152 205v22"/>
  <path class="thin none" d="M110 229h25"/>
  <path class="thin none" d="M139 229h25"/>
  <path class="line" fill="#9ddf9a" d="M68 72c14-30 50-38 78-22-22 1-37 14-45 35z"/>
  <path class="line" fill="#d9f4ff" d="M103 81c8-12 25-18 41-13-9 6-15 14-18 25z"/>
"""
    ),
    ANIMALS / "fish.svg": svg(
        STYLE
        + """
  <path class="line" fill="#f6a54f" d="M64 128c25-43 84-54 127-20 11 9 11 31 0 40-43 34-102 23-127-20z"/>
  <path class="line" fill="#f2785c" d="M193 108c22-28 43-30 52-23-3 21-14 33-33 43 19 10 30 22 33 43-9 7-30 5-52-23z"/>
  <path class="line" fill="#ffd86f" d="M118 96c15 5 25 17 30 32-14 1-29-5-39-17z"/>
  <path class="line" fill="#ffd86f" d="M121 160c13-5 23-16 27-31-14 0-27 5-38 16z"/>
  <circle fill="#4d392d" cx="88" cy="121" r="7"/>
  <path class="thin none" d="M55 128c10 6 19 6 29 0"/>
  <circle class="thin" fill="#d9f4ff" cx="47" cy="84" r="11"/>
  <circle class="thin" fill="#d9f4ff" cx="31" cy="56" r="8"/>
  <path class="thin none" d="M161 105c-7 15-7 32 0 47"/>
"""
    ),
    ANIMALS / "rabbit.svg": svg(
        STYLE
        + """
  <path class="line" fill="#f6f4e8" d="M76 147c5-36 34-61 72-57 39 4 63 33 57 70-6 39-39 61-79 56-38-5-56-31-50-69z"/>
  <path class="line" fill="#fdfaf1" d="M67 91c0-31 25-54 59-54s59 23 59 54-25 55-59 55-59-24-59-55z"/>
  <path class="line" fill="#fdfaf1" d="M83 52C74 15 88-7 107 13c13 14 14 42 6 66z"/>
  <path class="line" fill="#fdfaf1" d="M145 77c-8-30-4-58 12-70 21-15 31 9 19 46-6 18-16 29-31 24z"/>
  <path class="thin" fill="#ffd3d2" d="M94 57c-5-21 0-34 8-28 7 6 8 24 4 40z"/>
  <path class="thin" fill="#ffd3d2" d="M155 60c-2-21 3-33 11-27 6 6 5 23-3 39z"/>
  <circle fill="#4d392d" cx="105" cy="96" r="6"/>
  <circle fill="#4d392d" cx="146" cy="96" r="6"/>
  <path class="thin" fill="#f19a8d" d="m125 112 10 0-5 8z"/>
  <path class="thin none" d="M119 127c6 7 15 7 22 0"/>
  <circle class="line" fill="#fff" cx="196" cy="164" r="21"/>
  <path class="line none" d="M104 215v20"/>
  <path class="line none" d="M158 215v20"/>
"""
    ),
    HOMES / "doghouse.svg": svg(
        STYLE
        + """
  <path class="line" fill="#f2bf72" d="M56 121h144v96H56z"/>
  <path class="line" fill="#df6f59" d="M38 124 128 47l90 77z"/>
  <path class="line" fill="#fff3d4" d="M101 217v-52c0-18 12-31 27-31s27 13 27 31v52z"/>
  <path class="thin none" d="M83 144h28"/>
  <path class="thin none" d="M164 144h18"/>
  <circle fill="#4d392d" cx="128" cy="174" r="6"/>
  <path class="line" fill="#f8e6b3" d="M83 79h90v34H83z"/>
"""
    ),
    HOMES / "cushion.svg": svg(
        STYLE
        + """
  <path class="line" fill="#f7a4b5" d="M45 109c7-30 32-48 83-48s76 18 83 48c10 43-18 78-83 78s-93-35-83-78z"/>
  <path class="line" fill="#ffd1da" d="M66 119c5-19 23-31 62-31s57 12 62 31c7 26-15 47-62 47s-69-21-62-47z"/>
  <path class="thin none" d="M63 84c16 17 21 35 17 54"/>
  <path class="thin none" d="M193 84c-16 17-21 35-17 54"/>
  <path class="thin none" d="M85 176c25 13 61 13 86 0"/>
  <path class="thin none" d="M128 62v26"/>
"""
    ),
    HOMES / "tree.svg": svg(
        STYLE
        + """
  <path class="line" fill="#9a6848" d="M105 105h47v112h-47z"/>
  <path class="line none" d="M126 130c-23-12-39-28-47-47"/>
  <path class="line none" d="M132 139c26-10 44-27 55-50"/>
  <circle class="line" fill="#70bd67" cx="89" cy="84" r="43"/>
  <circle class="line" fill="#82cf71" cx="133" cy="62" r="49"/>
  <circle class="line" fill="#67b85f" cx="174" cy="91" r="43"/>
  <circle class="line" fill="#85d378" cx="126" cy="106" r="51"/>
  <path class="thin" fill="#f7d28a" d="M106 131c17-13 39-13 56 0-8 18-48 18-56 0z"/>
"""
    ),
    HOMES / "aquarium.svg": svg(
        STYLE
        + """
  <path class="line" fill="#b9e7f5" d="M43 64h170v128c0 17-13 30-30 30H73c-17 0-30-13-30-30z"/>
  <path class="thin none" d="M43 102c38 11 64-10 101 0 28 8 45 10 69-1"/>
  <path class="line" fill="#f4cf78" d="M57 183c28-12 49 7 72 0 24-7 45-13 70 0v20c0 9-8 17-17 17H74c-9 0-17-8-17-17z"/>
  <path class="thin" fill="#69b86f" d="M79 176c-2-27 8-45 26-57 1 27-9 47-26 57z"/>
  <path class="thin" fill="#69b86f" d="M164 179c-6-24-1-44 14-59 7 24 2 44-14 59z"/>
  <path class="thin" fill="#f6a54f" d="M109 139c16-19 39-19 55 0-16 18-39 18-55 0z"/>
  <path class="thin" fill="#f2785c" d="m164 139 22-15v30z"/>
  <circle fill="#4d392d" cx="125" cy="136" r="4"/>
  <circle class="thin" fill="#d9f4ff" cx="93" cy="111" r="8"/>
  <circle class="thin" fill="#d9f4ff" cx="74" cy="91" r="6"/>
"""
    ),
    HOMES / "grass.svg": svg(
        STYLE
        + """
  <path class="line" fill="#79bf5d" d="M32 207c14-35 34-58 60-72-6 32-4 56 8 72z"/>
  <path class="line" fill="#91cf65" d="M72 207c10-45 31-78 63-100-7 42-3 75 13 100z"/>
  <path class="line" fill="#67ad56" d="M130 207c10-36 31-63 62-82-6 34-1 61 15 82z"/>
  <path class="line" fill="#85c95f" d="M11 216c54-21 184-22 234 0v16H11z"/>
  <path class="line" fill="#8b603f" d="M85 222c3-31 24-52 52-52s49 21 52 52z"/>
  <path class="thin none" d="M103 207c8-9 20-14 34-14s26 5 34 14"/>
"""
    ),
    ANIMALS / "panda.svg": svg(
        STYLE
        + """
  <path class="line" fill="#fff8e8" d="M68 144c0-44 36-80 80-74 42 6 70 41 64 84-6 41-44 65-86 58-37-6-58-30-58-68z"/>
  <circle class="line" fill="#3a2a22" cx="78" cy="80" r="24"/>
  <circle class="line" fill="#3a2a22" cx="178" cy="80" r="24"/>
  <ellipse class="line" fill="#3a2a22" cx="98" cy="124" rx="16" ry="22"/>
  <ellipse class="line" fill="#3a2a22" cx="158" cy="124" rx="16" ry="22"/>
  <circle fill="#fff" cx="100" cy="120" r="6"/>
  <circle fill="#fff" cx="160" cy="120" r="6"/>
  <ellipse class="line" fill="#3a2a22" cx="128" cy="150" rx="12" ry="8"/>
  <path class="thin none" d="M128 160v6"/>
  <path class="thin none" d="M118 174c5 5 15 5 20 0"/>
"""
    ),
    ANIMALS / "pig.svg": svg(
        STYLE
        + """
  <path class="line" fill="#f7b9c1" d="M62 138c0-44 38-72 78-68 44 4 72 38 70 80-2 38-38 60-78 60-40 0-72-30-70-72z"/>
  <path class="line" fill="#f7b9c1" d="M58 96c5-22 22-32 38-22 8 18-12 34-30 32z"/>
  <path class="line" fill="#f7b9c1" d="M198 96c-5-22-22-32-38-22-8 18 12 34 30 32z"/>
  <ellipse class="line" fill="#f29db0" cx="128" cy="148" rx="38" ry="26"/>
  <circle fill="#4d392d" cx="116" cy="148" r="5"/>
  <circle fill="#4d392d" cx="140" cy="148" r="5"/>
  <circle fill="#4d392d" cx="100" cy="116" r="6"/>
  <circle fill="#4d392d" cx="156" cy="116" r="6"/>
  <path class="thin none" d="M105 178c8 8 18 8 26 0"/>
"""
    ),
    ANIMALS / "frog.svg": svg(
        STYLE
        + """
  <path class="line" fill="#82c264" d="M52 156c0-50 36-86 76-86s76 36 76 86c0 38-30 70-76 70s-76-32-76-70z"/>
  <path class="line" fill="#82c264" d="M70 78c0-22 14-38 30-38s28 16 28 38-12 36-28 36-30-14-30-36z"/>
  <path class="line" fill="#82c264" d="M128 78c0-22 14-38 30-38s28 16 28 38-12 36-28 36-30-14-30-36z"/>
  <circle class="line" fill="#fff" cx="100" cy="74" r="14"/>
  <circle class="line" fill="#fff" cx="158" cy="74" r="14"/>
  <circle fill="#4d392d" cx="100" cy="78" r="6"/>
  <circle fill="#4d392d" cx="158" cy="78" r="6"/>
  <path class="thin none" d="M88 158c20 12 38 12 60 0"/>
  <path class="line" fill="#a3d77f" d="M75 196c-20 5-32 22-22 36 14-2 24-13 28-32z"/>
  <path class="line" fill="#a3d77f" d="M183 196c20 5 32 22 22 36-14-2-24-13-28-32z"/>
"""
    ),
    ANIMALS / "bear.svg": svg(
        STYLE
        + """
  <path class="line" fill="#a87147" d="M70 144c0-44 36-78 78-72 42 6 68 41 62 84-6 41-42 65-84 58-37-6-56-32-56-70z"/>
  <circle class="line" fill="#a87147" cx="76" cy="78" r="22"/>
  <circle class="line" fill="#a87147" cx="184" cy="78" r="22"/>
  <circle class="line" fill="#c89070" cx="76" cy="78" r="10"/>
  <circle class="line" fill="#c89070" cx="184" cy="78" r="10"/>
  <ellipse class="line" fill="#e8c69c" cx="128" cy="158" rx="40" ry="32"/>
  <circle fill="#4d392d" cx="102" cy="118" r="7"/>
  <circle fill="#4d392d" cx="156" cy="118" r="7"/>
  <ellipse class="line" fill="#4d392d" cx="128" cy="142" rx="11" ry="8"/>
  <path class="thin none" d="M128 152v8"/>
  <path class="thin none" d="M115 170c8 6 18 6 26 0"/>
"""
    ),
    ANIMALS / "mouse.svg": svg(
        STYLE
        + """
  <path class="line" fill="#c9c4ba" d="M62 156c0-50 30-90 66-90s66 40 66 90c0 38-30 68-66 68s-66-30-66-68z"/>
  <circle class="line" fill="#c9c4ba" cx="80" cy="78" r="24"/>
  <circle class="line" fill="#c9c4ba" cx="176" cy="78" r="24"/>
  <circle class="line" fill="#f7c8d0" cx="80" cy="78" r="12"/>
  <circle class="line" fill="#f7c8d0" cx="176" cy="78" r="12"/>
  <circle fill="#4d392d" cx="100" cy="126" r="6"/>
  <circle fill="#4d392d" cx="156" cy="126" r="6"/>
  <path class="line" fill="#f29db0" d="M118 156c4 8 16 8 20 0l-10 10z"/>
  <path class="thin none" d="M114 178c8 5 20 5 28 0"/>
  <path class="thin none" d="M64 162c-14 4-26 12-30 24"/>
  <path class="thin none" d="M192 162c14 4 26 12 30 24"/>
"""
    ),
    HOMES / "bamboo.svg": svg(
        STYLE
        + """
  <path class="line" fill="#92c660" d="M70 28h32v204H70z"/>
  <path class="line" fill="#a4d56e" d="M156 44h32v188h-32z"/>
  <path class="thin none" d="M70 88h32"/>
  <path class="thin none" d="M70 142h32"/>
  <path class="thin none" d="M70 196h32"/>
  <path class="thin none" d="M156 102h32"/>
  <path class="thin none" d="M156 156h32"/>
  <path class="thin none" d="M156 210h32"/>
  <path class="line" fill="#7ab851" d="M102 60c20-12 38-2 50 14-20 4-38 2-50-14z"/>
  <path class="line" fill="#7ab851" d="M188 76c14-15 30-12 40-2-14 12-30 14-40 2z"/>
  <path class="line" fill="#7ab851" d="M22 116c14-12 28-10 38 0-12 12-28 12-38 0z"/>
"""
    ),
    HOMES / "pigpen.svg": svg(
        STYLE
        + """
  <path class="line" fill="#9a6848" d="M22 188h212v44H22z"/>
  <path class="line" fill="#caa168" d="M52 78h16v140H52z"/>
  <path class="line" fill="#caa168" d="M120 78h16v140h-16z"/>
  <path class="line" fill="#caa168" d="M188 78h16v140h-16z"/>
  <path class="line" fill="#caa168" d="M40 108h176v16H40z"/>
  <path class="line" fill="#caa168" d="M40 156h176v16H40z"/>
  <ellipse class="line" fill="#7d5c3a" cx="98" cy="208" rx="32" ry="9"/>
  <ellipse class="line" fill="#7d5c3a" cx="174" cy="208" rx="22" ry="7"/>
"""
    ),
    HOMES / "lilypad.svg": svg(
        STYLE
        + """
  <path class="line" fill="#b4e5f4" d="M16 156c20-10 40-10 60 0s40 10 60 0 40-10 60 0 40 10 44 0v76H16z"/>
  <path class="line" fill="#7ec064" d="M52 142c0-26 36-46 76-46s76 20 76 46-36 46-76 46-76-20-76-46z"/>
  <path class="line none" d="M128 96v46"/>
  <path class="line" fill="#ffd0e1" d="M128 78c-12-12 0-32 12-32s22 20 12 32c14 0 22 14 14 24-8 8-22 4-26-10-2 14-18 18-26 10-8-10 0-24 14-24z"/>
  <circle class="line" fill="#ffe97a" cx="128" cy="68" r="9"/>
"""
    ),
    HOMES / "cave.svg": svg(
        STYLE
        + """
  <path class="line" fill="#8c8a82" d="M22 224c0-94 48-164 106-164s106 70 106 164z"/>
  <path class="line" fill="#3a3530" d="M76 224c0-50 24-86 52-86s52 36 52 86z"/>
  <ellipse fill="#1a120c" cx="128" cy="200" rx="36" ry="28"/>
  <circle class="line" fill="#a8a5a0" cx="50" cy="208" r="14"/>
  <circle class="line" fill="#a8a5a0" cx="206" cy="208" r="14"/>
  <path class="line" fill="#fff" d="M82 84c12-14 32-22 46-22s34 8 46 22c-30-4-62-4-92 0z"/>
"""
    ),
    HOMES / "hole.svg": svg(
        STYLE
        + """
  <path class="line" fill="#85c95f" d="M11 168c54-21 184-22 234 0v66H11z"/>
  <ellipse class="line" fill="#3a2a22" cx="128" cy="184" rx="50" ry="36"/>
  <ellipse fill="#1a120c" cx="128" cy="190" rx="36" ry="24"/>
  <circle class="line" fill="#a8a5a0" cx="58" cy="184" r="12"/>
  <circle class="line" fill="#a8a5a0" cx="200" cy="188" r="14"/>
  <path class="line" fill="#67ad56" d="M40 162l10-26 10 26z"/>
  <path class="line" fill="#67ad56" d="M204 162l10-26 10 26z"/>
"""
    ),
}


def build_preview():
    items = [
        ("どうぶつ", "animals/dog.svg", "いぬ"),
        ("どうぶつ", "animals/cat.svg", "ねこ"),
        ("どうぶつ", "animals/bird.svg", "とり"),
        ("どうぶつ", "animals/fish.svg", "さかな"),
        ("どうぶつ", "animals/rabbit.svg", "うさぎ"),
        ("どうぶつ", "animals/panda.svg", "ぱんだ"),
        ("どうぶつ", "animals/pig.svg", "ぶた"),
        ("どうぶつ", "animals/frog.svg", "かえる"),
        ("どうぶつ", "animals/bear.svg", "くま"),
        ("どうぶつ", "animals/mouse.svg", "ねずみ"),
        ("おうち", "homes/doghouse.svg", "いぬごや"),
        ("おうち", "homes/cushion.svg", "クッション"),
        ("おうち", "homes/tree.svg", "き"),
        ("おうち", "homes/aquarium.svg", "すいそう"),
        ("おうち", "homes/grass.svg", "くさむら"),
        ("おうち", "homes/bamboo.svg", "たけ"),
        ("おうち", "homes/pigpen.svg", "ぶたごや"),
        ("おうち", "homes/lilypad.svg", "はす"),
        ("おうち", "homes/cave.svg", "ほらあな"),
        ("おうち", "homes/hole.svg", "あな"),
    ]
    cards = "\n".join(
        f'      <figure><img src="{src}" alt="{label}"><figcaption>{group}: {label}</figcaption></figure>'
        for group, src, label in items
    )
    return f"""<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>どうぶつさんのおうち 素材プレビュー</title>
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: "Hiragino Maru Gothic ProN", "Yu Gothic", "Meiryo", system-ui, sans-serif;
        color: #4d392d;
        background: #fff9e8;
      }}
      main {{
        width: min(1080px, 100%);
        margin: 0 auto;
        padding: 24px;
      }}
      h1 {{ margin: 0 0 20px; font-size: clamp(1.8rem, 5vw, 3rem); }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 16px;
      }}
      figure {{
        margin: 0;
        padding: 16px;
        border: 5px solid #4d392d;
        border-radius: 22px;
        background: white;
        text-align: center;
      }}
      img {{
        width: 100%;
        max-width: 170px;
        aspect-ratio: 1;
        object-fit: contain;
      }}
      figcaption {{
        margin-top: 10px;
        font-weight: 800;
        font-size: 1.1rem;
      }}
    </style>
  </head>
  <body>
    <main>
      <h1>どうぶつさんのおうち 素材プレビュー</h1>
      <div class="grid">
{cards}
      </div>
    </main>
  </body>
</html>
"""


def main():
    for path, content in ASSETS.items():
        write(path, content)
    write(PREVIEW, build_preview())
    print(f"generated {len(ASSETS)} svg files")
    print(f"generated {PREVIEW.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
