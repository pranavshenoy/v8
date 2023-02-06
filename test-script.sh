#!/bin/bash


rm v8-run-*.log
rm v8_young_gen_*.log
rm hello_world
# set -e 
export SEMISPACE_SIZE=1 SKIP_RECOMPUTE_LIMIT=1 SKIP_MEMORY_REDUCER=1 USE_MEMBALANCER=1 LOG_DIRECTORY="/" LOG_GC="1" C_VALUE="1";
ninja -C out.gn/x64.release.sample v8_monolith
ninja -C out.gn/x64.release.sample  v8_hello_world
third_party/llvm-build/Release+Asserts/bin/clang++ out.gn/x64.release.sample/obj/v8_hello_world/hello-world.o out.gn/x64.release.sample/obj/libv8_monolith.a -o hello_world

#creating directory
TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
mkdir "results/$TIMESTAMP/"


#multiply the factor by 512KB to get semi_space size. and again by 2 to get young gen size
initial_semispace_size_factor=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25)
benchmarks=(  "typescript.js" "acdc.js" "box2d.js" "code-first-load.js" "crypto.js"  "deltablue.js" "earley-boyer.js" "gbemu-part.js" "mandreel.js" "navier-stokes.js" "pdfjs.js" "raytrace.js" "regexp.js" "richards.js" "splay.js" "zlib.js")
# initial_semispace_size_factor=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 )
# benchmarks=("acdc.js" "typescript.js" )
for bm in "${benchmarks[@]}";
do
    read -a dir_name -d '.' <<< $bm
    full_path="results/$TIMESTAMP/"$dir_name"/"
    mkdir $full_path
    echo "Running Test: "$dir_name
    for i in "${initial_semispace_size_factor[@]}";
    do 
        # echo "      semispace_size_factor: "$i
        # rm "semispace_size.txt"
        # echo $i >> "semispace_size.txt"
        # ./hello_world $bm
        export SEMISPACE_SIZE=$i SKIP_RECOMPUTE_LIMIT=1 SKIP_MEMORY_REDUCER=1 USE_MEMBALANCER=1 LOG_DIRECTORY=$full_path LOG_GC="1" C_VALUE="1";  bash -c "./hello_world $bm"
        mv v8_young_gen_*.log $full_path
        mv v8-custom-log.log $full_path
    done
done
# echo "Plotting charts"
# # python3 charts.py "results/$TIMESTAMP/"