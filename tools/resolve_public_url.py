import argparse
import os
import re
import subprocess
from pathlib import Path


PUBLIC_URL_ENV = "DOUBUTSU_HOME_PUBLIC_URL"
LEGACY_PUBLIC_URL_ENV = "ANIMAL_HOME_PUBLIC_URL"


def normalize_url(url):
    value = url.strip()
    if not re.match(r"^https?://", value):
        raise ValueError("Public URL must start with http:// or https://")
    return value.rstrip("/") + "/"


def repo_root():
    current = Path(__file__).resolve()
    for candidate in current.parents:
        if (candidate / ".git").exists():
            return candidate

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=current.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def git_remote_url(root):
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def parse_github_remote(remote_url):
    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>.+?)(?:\.git)?/?$", remote_url)
    if not match:
        raise ValueError(f"Unsupported GitHub remote URL: {remote_url}")
    return match.group("owner"), match.group("repo")


def github_pages_url(owner, repo):
    if repo == f"{owner}.github.io":
        return normalize_url(f"https://{owner}.github.io/")
    return normalize_url(f"https://{owner}.github.io/{repo}/")


def resolve_public_url(base_url=None):
    explicit_url = base_url or os.environ.get(PUBLIC_URL_ENV) or os.environ.get(LEGACY_PUBLIC_URL_ENV)
    if explicit_url:
        return normalize_url(explicit_url)

    root = repo_root()
    owner, repo = parse_github_remote(git_remote_url(root))
    return github_pages_url(owner, repo)


def main():
    parser = argparse.ArgumentParser(description="Resolve the public URL for doubutsusanno-outi.")
    parser.add_argument("--base-url", help="Override the detected public URL.")
    args = parser.parse_args()
    print(resolve_public_url(args.base_url))


if __name__ == "__main__":
    main()
