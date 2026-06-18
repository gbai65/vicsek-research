#!/bin/bash

module load physics

fileName="vicsek.cpp"
execute="./runtime"
inputFile="newCoexPoints.txt"
g++ -O3 -march=native -fopenmp -ftree-vectorize -ffast-math vicsek.cpp cnpy/cnpy.cpp -Icnpy -lz -o runtime

start_counter=0
max_count=500


counter=$start_counter
while read -r eta rho v0; do
    if (( counter >= max_count )); then
        break
    fi
    echo "Simulation #$counter running... eta: $eta, rho: $rho, v0: $v0"
    "$execute" "$counter" "$eta" "$rho" "$v0"
    ((counter++))
done < <(tail -n +$((start_counter + 1)) "$inputFile")