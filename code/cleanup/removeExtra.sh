# root="/mnt/c/Users/grace_0ddpimo/vicsek/logs"

# for (( i=0; i<199; i++ )); do
#     dir_name="${root}/slurm_temp_logs_${i}"
#     if [ -d "$dir_name" ]; then
#         find "$dir_name" -type f -name "checkpoint*" -delete
#     fi
#     for (( j=1; j<5; j++ )); do
#         dir_name="${root}/slurm_temp_logs_${i}_${j}"
        
#         if [ -d "$dir_name" ]; then
#             find "$dir_name" -type f -name "checkpoint*" -delete
#         fi
#     done
# done
echo "hi"