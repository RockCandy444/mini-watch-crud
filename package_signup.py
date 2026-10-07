"""Create a source-only ZIP for the registration assignment."""
import ast
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / "mini-watch-signup-submit.zip"
EXCLUDED = {".git", ".venv", "venv", "node_modules", ".next", "out", "dist", ".local", "__pycache__", ".pytest_cache", "test-results"}
SUFFIXES = {".py", ".jsx", ".js", ".mjs", ".json", ".html", ".css", ".sql", ".md", ".txt"}


def included(path):
    if not path.is_file() or any(part in EXCLUDED for part in path.relative_to(ROOT).parts):
        return False
    if path.name.startswith(".env"):
        return path.name == ".env.example"
    return not path.name.startswith("try_") and (path.suffix in SUFFIXES or path.name == ".gitignore")


if __name__ == "__main__":
    paths = [path for path in ROOT.rglob("*") if included(path)]
    for path in paths:
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(paths):
            archive.write(path, "mini-watch/" + path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(OUTPUT) as archive:
        assert archive.testzip() is None
        names = archive.namelist()
        assert "mini-watch/monitor/frontend/package-lock.json" in names
        assert "mini-watch/monitor/frontend/src/app/register/page.jsx" in names
        assert "mini-watch/monitor/backend/models.py" in names
        assert not any(part in EXCLUDED for name in names for part in Path(name).parts)
        assert not any(Path(name).name.startswith(".env") and not name.endswith(".env.example") for name in names)
    print(f"Python syntax and ZIP verified: {len(paths)} files, {OUTPUT.stat().st_size} bytes")
    print(OUTPUT)
