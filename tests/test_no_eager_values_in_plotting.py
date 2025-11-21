from pathlib import Path

BANNED_SUBSTRINGS = [
    "data.values",
    "cube.values",
    "da.values",
]


def test_no_full_values_calls_in_plotting_code():
    plotting_root = Path("src/cubedynamics/plotting")
    hits = []
    for path in plotting_root.rglob("*.py"):
        text = path.read_text()
        for token in BANNED_SUBSTRINGS:
            if token in text:
                hits.append((str(path), token))
    assert not hits, f"Avoid eager .values on full cubes in plotting code: {hits}"
