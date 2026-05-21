for (( i=0; i<201; i++)); do
    echo $i
    root="/csl/users/2026gbai/logs/slurm_temp_logs_$i"

    for k in 0 1 2 3 4; do
        if [[ $k -eq 0 ]]; then
            suffix=""
        else
            suffix="_$k"
        fi
        file="${root}${suffix}/outputs.txt"
        [[ -f "$file" ]] || continue

        tail -n +800 "$file" | awk '{match($0, /Order = ([0-9.eE+-]+)/, a); print a[1]}' > "/csl/users/2026gbai/extractedOrder/${i}_${k}.txt"
    done
done