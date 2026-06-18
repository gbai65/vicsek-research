for (( i=29; i<100; i++)); do
    echo $i
    root="../617 logs/default/2/slurm_temp_logs_$i"

    for k in 0 1 2 3 4; do
        if [[ $k -eq 0 ]]; then
            suffix=""
        else
            suffix="_$k"
        fi
        file="${root}${suffix}/outputs.txt"
        [[ -f "$file" ]] || continue
        echo "done"
        tail -n +800 "$file" | awk '{match($0, /Order = ([0-9.eE+-]+)/, a); print a[1]}' > "../new extracted order/${i}_${k}.txt"
    done
done