{
  description = ''OpenReproLab 2026-2027'';

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python314;
    in 
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          python
          pkgs.uv
          pkgs.fish
        ];

        env = {
          UV_PYTHON = python.interpreter;
          UV_PYTHON_DOWNLOADS = "never";

          LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib  # libstdc++ (for numpy)
            pkgs.zlib  # libz (for numpy)
          ];
        };

        shellHook = ''
          # $- expands to currently active shell option flags, e.g.:
          #    iBs -> interactive (i), brace expansion enabled (B), reading from stdin (s)
          #    hsc -> hash command locations (h), command came from `-c` string (c)
          # *i* is treated as a glob pattern
          if [[ $- == *i* ]]; then  # true if $- contains the letter i
            exec fish
          fi
        '';
      };
    };
}