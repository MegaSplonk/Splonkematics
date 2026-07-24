for i in */*.kicad_sch; do kicad-cli sch export bom $i; done
nix-shell -p python3 python314Packages.pandas --run "python3 merge_bom.py"
