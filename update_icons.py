#!/usr/bin/env python3
"""
Downloads icons (Homarr, Google Favicons, raw URLs) locally into icons/
and generates a flake.nix providing all icons as local paths and derivations.
"""

import os
import sys
import urllib.request
from pathlib import Path

# Icons definition
# Type can be:
# - "homarr": fetched from Homarr dashboard icons repository
# - "googleFavicon": fetched from Google Favicons service sz=128
# - "url": fetched from direct URL
ICONS = {
    "wealthfolio": {
        "type": "url",
        "url": "https://assets.wealthfolio.app/images/logo.png",
        "filename": "wealthfolio.png",
    },
    "immich": {
        "type": "homarr",
        "name": "immich",
        "filename": "immich.png",
    },
    "home-assistant": {
        "type": "homarr",
        "name": "home-assistant",
        "filename": "home-assistant.png",
    },
    "siyuan": {
        "type": "url",
        "url": "https://github.com/siyuan-note.png",
        "filename": "siyuan.png",
    },
    "karakeep": {
        "type": "homarr",
        "name": "karakeep",
        "filename": "karakeep.png",
    },
    "google-docs": {
        "type": "homarr",
        "name": "google-docs",
        "filename": "google-docs.png",
    },
    "google-sheets": {
        "type": "homarr",
        "name": "google-sheets",
        "filename": "google-sheets.png",
    },
    "google-slides": {
        "type": "homarr",
        "name": "google-slides",
        "filename": "google-slides.png",
    },
    "google-forms": {
        "type": "homarr",
        "name": "google-forms",
        "filename": "google-forms.png",
    },
    "gmail": {
        "type": "homarr",
        "name": "gmail",
        "filename": "gmail.png",
    },
    "whatsapp": {
        "type": "homarr",
        "name": "whatsapp",
        "filename": "whatsapp.png",
    },
    "telegram": {
        "type": "homarr",
        "name": "telegram",
        "filename": "telegram.png",
    },
    "discord": {
        "type": "homarr",
        "name": "discord",
        "filename": "discord.png",
    },
    "messenger": {
        "type": "googleFavicon",
        "domain": "messenger.com",
        "filename": "messenger.png",
    },
    "youtube-music": {
        "type": "homarr",
        "name": "youtube-music",
        "filename": "youtube-music.png",
    },
    "spotify": {
        "type": "homarr",
        "name": "spotify",
        "filename": "spotify.png",
    },
    "fetlife": {
        "type": "googleFavicon",
        "domain": "fetlife.com",
        "filename": "fetlife.png",
    },
    "vscode": {
        "type": "homarr",
        "name": "visual-studio-code",
        "filename": "vscode.png",
    },
    "tailscale": {
        "type": "homarr",
        "name": "tailscale",
        "filename": "tailscale.png",
    },
    "gridfinity": {
        "type": "googleFavicon",
        "domain": "https://gridfinity-cutout.pages.dev",
        "filename": "gridfinity.png",
    },
    "xtb": {
        "type": "googleFavicon",
        "domain": "xtb.com",
        "filename": "xtb.png",
    },
    "outlook": {
        "type": "homarr",
        "name": "microsoft-outlook",
        "filename": "outlook.png",
    },
}


def get_icon_url(icon_def: dict) -> str:
    icon_type = icon_def["type"]
    if icon_type == "homarr":
        return f"https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/png/{icon_def['name']}.png"
    elif icon_type == "googleFavicon":
        return f"https://www.google.com/s2/favicons?domain={icon_def['domain']}&sz=128"
    elif icon_type == "url":
        return icon_def["url"]
    else:
        raise ValueError(f"Unknown icon type: {icon_type}")


def download_icon(url: str, dest_path: Path):
    print(f"Downloading {url} -> {dest_path.name}...")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"},
    )
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Failed to download {url}: HTTP status {resp.status}")
        content = resp.read()
        if len(content) == 0:
            raise RuntimeError(f"Downloaded empty file from {url}")
        dest_path.write_bytes(content)


def generate_flake(root_dir: Path, icons_dict: dict):
    # Generates flake.nix
    lines = [
        "{",
        '  description = "Locally tracked webicons flake for reproducible desktop launchers";',
        "",
        "  inputs = {",
        '    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";',
        "  };",
        "",
        "  outputs = { self, nixpkgs }:",
        "    let",
        '      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];',
        "      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f system (import nixpkgs { inherit system; }));",
        "    in {",
        "      # Nixpkgs derivations: packages.<system>.<icon>",
        "      packages = forEachSupportedSystem (system: pkgs: {",
    ]

    for key, item in icons_dict.items():
        fname = item["filename"]
        lines.append(f'        "{key}" = pkgs.runCommand "{fname}" {{}} "cp ${{./icons/{fname}}} $out";')

    lines.extend([
        "      });",
        "",
        "      # Direct paths referencing flake repository files",
        "      icons = {",
    ])

    for key, item in icons_dict.items():
        fname = item["filename"]
        lines.append(f'        "{key}" = ./icons/{fname};')

    lines.extend([
        "      };",
        "    };",
        "}",
        "",
    ])

    flake_path = root_dir / "flake.nix"
    flake_path.write_text("\n".join(lines))
    print(f"Generated {flake_path.name}")


def main():
    root_dir = Path(__file__).resolve().parent
    icons_dir = root_dir / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)

    for key, item in ICONS.items():
        url = get_icon_url(item)
        dest = icons_dir / item["filename"]
        download_icon(url, dest)

    generate_flake(root_dir, ICONS)
    print("All icons downloaded and flake.nix generated successfully.")


if __name__ == "__main__":
    main()
