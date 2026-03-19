#!/bin/bash

fileName="vicsek.cpp"
execute="./runtime"
inputFile="LHSpoints.txt"
g++ -O3 -march=native -fopenmp -ftree-vectorize -ffast-math vicsek.cpp cnpy/cnpy.cpp -Icnpy -lz -o runtime

counter=0
while read -r eta rho v0; do
    echo "Simulation #$counter running... eta: $eta, rho: $rho, v0: $v0"
    "$execute" "$counter" "$eta" "$rho" "$v0"
    ((counter++))
done < "$inputFile"