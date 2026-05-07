for (( i=0; i<201; i++)); do
    root="/csl/users/2026gbai/logs/slurm_temp_logs"
    if [ -d "${root}_$i" ]; then
        fileArr=()
        missingArr=()
        for j in "" "_1" "_2" "_3" "_4"; do
            if [ -f "${root}_$i$j/outputs.txt" ]; then
                fileArr+=("${root}_$i$j/outputs.txt")
            else
                missingArr+=($j)
            fi
        done
        if [[ ${#missingArr[@]} -gt 0 ]]; then
            echo "#${i}: Missing ${missingArr[*]}"
        fi
        if [[ ${#fileArr[@]} -gt 1 ]]; then
            unique_count=$(md5sum "${fileArr[@]}" | cut -d' ' -f1 | sort -u | wc -l)
            if [ "$unique_count" -ne "${#fileArr[@]}" ]; then
                echo "Issue at #${i}: Not unique"
            fi
        fi
    fi
done