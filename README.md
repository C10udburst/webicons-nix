# webicons-nix

Locally tracked web application icons flake for reproducible NixOS desktop launchers.

## How it works

1. `update_icons.py` defines the icons list, downloads them into `./icons/`, and generates `flake.nix` with local paths and derivations.
2. GitHub Actions runs on pushes that modify `update_icons.py`, runs the script, and commits/pushes the downloaded icons and updated `flake.nix` back to the repository.
3. No hash mismatches or network requests are needed at NixOS build time because the files are tracked directly inside the flake repository.

## Usage in Nix Flake

```nix
inputs = {
  webicons.url = "github:C10udburst/webicons-nix";
};
```

Access icons via `inputs.webicons.packages.${pkgs.system}.<name>` or direct paths via `inputs.webicons.icons.<name>`.
