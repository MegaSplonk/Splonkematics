#!/usr/bin/env bash

rm -rf ./bom
mkdir -p ./bom
for dir in *; do
	if [ ! -d "$dir" ]; then
		continue
	fi
	if [ ! -e "$dir/$dir.kicad_sch" ]; then 
		continue;
	fi
	(cd bom && kicad-cli sch export bom "../$dir/$dir.kicad_sch")
done
nix-shell -p python314 python314Packages.pandas --run "python3 merge_bom.py"
