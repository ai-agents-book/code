"""Fetch the GloVe word vectors chapter 1's notebook needs.

`notebooks/ch01-llms.ipynb` reads `../assets/glove.6B.100d.txt` -- a 347 MB
file that is deliberately not committed to this repository (see
.gitignore). Run this once before opening that notebook:

    python scripts/fetch_assets.py

Be aware of the download before you run it: GloVe is distributed only as
one archive containing all four dimensionalities (50d/100d/200d/300d), so
fetching the 100d vectors means downloading the **entire ~862 MB zip**.
This script extracts just the one ~347 MB member the notebook uses and
discards the rest of the archive afterwards -- it does not keep 862 MB on
disk, but it does transfer it over the network.

Upstream original (the file the GloVe authors publish):
    https://nlp.stanford.edu/data/glove.6B.zip

We fetch from Hugging Face's mirror instead:
    https://huggingface.co/stanfordnlp/glove/resolve/main/glove.6B.zip
because it is reachable over plain HTTPS with no redirect chain, and
`huggingface.co` is already in tools/check_secrets.py's ALLOWED_HOSTS --
the same host this project already trusts for the book's own rendering.

Deliberately uses only the Python standard library: a reader runs this
before `uv sync`, so it cannot depend on anything the sync would install
(e.g. `requests` or `tqdm`).
"""

from __future__ import annotations

import argparse
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

GLOVE_ZIP_URL = "https://huggingface.co/stanfordnlp/glove/resolve/main/glove.6B.zip"
MEMBER_NAME = "glove.6B.100d.txt"
ARCHIVE_SIZE_MB = 862  # the whole glove.6B.zip -- all four dimensionalities
MEMBER_SIZE_MB = 347  # just the 100d file this script keeps

DEFAULT_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

CHUNK_SIZE = 1024 * 1024  # 1 MiB


def _download(url: str, dest: Path) -> None:
    """Stream `url` into `dest`, printing progress as it goes.

    Raises OSError / urllib.error.URLError on any failure (a bad URL, a
    dropped connection, a response shorter than its own Content-Length).
    Never leaves a partially-written `dest` behind: the caller is
    responsible for removing it on failure, which main() does.
    """
    with urllib.request.urlopen(url) as response:
        total = 0
        content_length = response.headers.get("Content-Length")
        if content_length is not None:
            total = int(content_length)
        downloaded = 0
        with open(dest, "wb") as fh:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                fh.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(
                        f"\r  {downloaded / 1e6:.0f} / {total / 1e6:.0f} MB "
                        f"({pct}%)",
                        end="",
                        flush=True,
                    )
                else:
                    print(f"\r  {downloaded / 1e6:.0f} MB", end="", flush=True)
        print()
        if total and downloaded != total:
            raise OSError(
                f"download ended after {downloaded} bytes, expected {total} "
                "-- the connection likely dropped partway through"
            )


def _extract_member(archive_path: Path, member: str, target: Path) -> None:
    """Stream only `member` out of the zip at `archive_path`, into `target`.

    Writes to a `.partial` sibling first and renames on success, so a
    reader who interrupts extraction (or hits a corrupt archive) never
    finds a half-written file at the final path. Raises KeyError if the
    archive has no such member, zipfile.BadZipFile if it is not a valid
    zip or fails its CRC check (the shape a truncated download takes).
    """
    partial = target.with_name(target.name + ".partial")
    with zipfile.ZipFile(archive_path) as zf:
        with zf.open(member) as src, open(partial, "wb") as dst:
            while True:
                chunk = src.read(CHUNK_SIZE)
                if not chunk:
                    break
                dst.write(chunk)
    partial.rename(target)


def fetch(
    *,
    url: str = GLOVE_ZIP_URL,
    assets_dir: Path = DEFAULT_ASSETS_DIR,
    member: str = MEMBER_NAME,
) -> int:
    target = assets_dir / member
    if target.exists():
        print(f"{target} already exists -- nothing to do.")
        return 0

    assets_dir.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".partial")

    print(f"Downloading {url}")
    print(
        f"This is the full GloVe 6B archive (~{ARCHIVE_SIZE_MB} MB); only "
        f"the ~{MEMBER_SIZE_MB} MB {member} is kept, the rest is discarded "
        "afterwards. This can take several minutes on a normal connection."
    )

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            archive_path = Path(tmpdir) / "glove.6B.zip"
            try:
                _download(url, archive_path)
            except (urllib.error.URLError, OSError, ValueError) as exc:
                print(f"\nDownload failed: {exc}", file=sys.stderr)
                return 1

            print(f"Extracting {member}...")
            try:
                _extract_member(archive_path, member, target)
            except KeyError as exc:
                print(f"Extraction failed: {member} not found in archive ({exc})", file=sys.stderr)
                return 1
            except zipfile.BadZipFile as exc:
                print(f"Extraction failed: {exc} -- the archive is likely truncated or corrupt", file=sys.stderr)
                return 1
            except OSError as exc:
                print(f"Extraction failed: {exc}", file=sys.stderr)
                return 1
            # archive_path is removed automatically with the TemporaryDirectory
    finally:
        # A CRC failure (truncated/corrupt archive) or a KeyboardInterrupt
        # raises out of the read loop inside _extract_member with `partial`
        # already opened and partially written, and no chance for that
        # function to clean up after itself. Removing it here, unconditionally
        # on any non-success path, is what keeps a half-written file from
        # ever sitting at a name a later run's existence check could read as
        # "already fetched".
        if partial.exists() and not target.exists():
            partial.unlink()

    print(f"Wrote {target} ({target.stat().st_size / 1e6:.0f} MB)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        default=GLOVE_ZIP_URL,
        help=argparse.SUPPRESS,  # test/debug seam, not for normal use
    )
    parser.add_argument(
        "--assets-dir",
        default=DEFAULT_ASSETS_DIR,
        type=Path,
        help=argparse.SUPPRESS,  # test/debug seam, not for normal use
    )
    args = parser.parse_args(argv)
    return fetch(url=args.url, assets_dir=args.assets_dir)


if __name__ == "__main__":
    sys.exit(main())
