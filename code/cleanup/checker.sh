for (( i=1; i<29; i++)); do
    root="C:\Users\grace_0ddpimo\vicsek\code\617 logs\default\1\slurm_temp_logs"
    echo "${root}_$i"
    if [ -d "${root}_$i" ]; then
        echo "here"
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