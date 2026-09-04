{
  description = "Locally tracked webicons flake for reproducible desktop launchers";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f system (import nixpkgs { inherit system; }));
    in {
      # Nixpkgs derivations: packages.<system>.<icon>
      packages = forEachSupportedSystem (system: pkgs: {
        "wealthfolio" = pkgs.runCommand "wealthfolio.png" {} "cp ${./icons/wealthfolio.png} $out";
        "immich" = pkgs.runCommand "immich.png" {} "cp ${./icons/immich.png} $out";
        "home-assistant" = pkgs.runCommand "home-assistant.png" {} "cp ${./icons/home-assistant.png} $out";
        "siyuan" = pkgs.runCommand "siyuan.png" {} "cp ${./icons/siyuan.png} $out";
        "karakeep" = pkgs.runCommand "karakeep.png" {} "cp ${./icons/karakeep.png} $out";
        "google-docs" = pkgs.runCommand "google-docs.png" {} "cp ${./icons/google-docs.png} $out";
        "google-sheets" = pkgs.runCommand "google-sheets.png" {} "cp ${./icons/google-sheets.png} $out";
        "google-slides" = pkgs.runCommand "google-slides.png" {} "cp ${./icons/google-slides.png} $out";
        "google-forms" = pkgs.runCommand "google-forms.png" {} "cp ${./icons/google-forms.png} $out";
        "gmail" = pkgs.runCommand "gmail.png" {} "cp ${./icons/gmail.png} $out";
        "whatsapp" = pkgs.runCommand "whatsapp.png" {} "cp ${./icons/whatsapp.png} $out";
        "telegram" = pkgs.runCommand "telegram.png" {} "cp ${./icons/telegram.png} $out";
        "discord" = pkgs.runCommand "discord.png" {} "cp ${./icons/discord.png} $out";
        "messenger" = pkgs.runCommand "messenger.png" {} "cp ${./icons/messenger.png} $out";
        "youtube-music" = pkgs.runCommand "youtube-music.png" {} "cp ${./icons/youtube-music.png} $out";
        "spotify" = pkgs.runCommand "spotify.png" {} "cp ${./icons/spotify.png} $out";
        "fetlife" = pkgs.runCommand "fetlife.png" {} "cp ${./icons/fetlife.png} $out";
        "vscode" = pkgs.runCommand "vscode.png" {} "cp ${./icons/vscode.png} $out";
        "gridfinity" = pkgs.runCommand "gridfinity.png" {} "cp ${./icons/gridfinity.png} $out";
      });

      # Direct paths referencing flake repository files
      icons = {
        "wealthfolio" = ./icons/wealthfolio.png;
        "immich" = ./icons/immich.png;
        "home-assistant" = ./icons/home-assistant.png;
        "siyuan" = ./icons/siyuan.png;
        "karakeep" = ./icons/karakeep.png;
        "google-docs" = ./icons/google-docs.png;
        "google-sheets" = ./icons/google-sheets.png;
        "google-slides" = ./icons/google-slides.png;
        "google-forms" = ./icons/google-forms.png;
        "gmail" = ./icons/gmail.png;
        "whatsapp" = ./icons/whatsapp.png;
        "telegram" = ./icons/telegram.png;
        "discord" = ./icons/discord.png;
        "messenger" = ./icons/messenger.png;
        "youtube-music" = ./icons/youtube-music.png;
        "spotify" = ./icons/spotify.png;
        "fetlife" = ./icons/fetlife.png;
        "vscode" = ./icons/vscode.png;
        "gridfinity" = ./icons/gridfinity.png;
      };
    };
}
