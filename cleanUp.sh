# for (( i=10; i<44; i++ )); do
#   mkdir "/mnt/c/Users/grace_0ddpimo/vicsek/logs/#0$i"
#   for ((j = 1; j<6; j++)); do
#     mkdir "/mnt/c/Users/grace_0ddpimo/vicsek/logs/#00$i/$j"
#   done

# done

# for j in "runtime_0" "runtime_1" "runtime_2" "runtime_3" "runtime_a0" "runtime_a1" "runtime_a2" "runtime_a3" "runtime_b0" "runtime_b1" "runtime_b2" "runtime_b3"; do
#   for (( i=0; i<30; i++ )); do
#       movee="/mnt/c/Users/grace_0ddpimo/vicsek/${j}/temp_logs_${i}"
#       mover="/mnt/c/Users/grace_0ddpimo/vicsek/logs/0${i}"
#       if [ -d "$movee" ]; then
#         chmod +x "$movee"
#         if [ -d "$mover" ]; then
#           addition=1
#           while [ -d "$mover_${addition}" ]
#             do
#                 ((addition++))
#           done
#           mover="/mnt/c/Users/grace_0ddpimo/vicsek/logs/0${i}_${}"
#         fi
#         mv "$movee" "$mover"
#       fi
#   done
# done

root="/mnt/c/Users/grace_0ddpimo/vicsek/logs/"

# for (( i=10; i<44; i++)); do
#   mkdir "$root#0${i}/{1..5}"


#   mv -v "$root#00${i}/2/temp_logs_${i}"/* "$root#00${i}/2"
#   rmdir -p "$root#00${i}/2/temp_logs_${i}"

#   mv -v "$root#00${i}/4/temp_logs_${i}"/* "$root#00${i}/3"
#   rmdir -p "$root#00${i}/4/temp_logs_${i}"
# done

for (( i=000; i<044; i++)); do
  find "$root#$i" -type d | wc -l
  final=5
  for (( j=1; j<6; j++)); do
    if [ -d "$root#$i/$j" ]; then
      if cmp -s file1 file2 && cmp -s file2 file3;
        echo 
    else
      final=$j
      break
    fi
  if []
  done
done