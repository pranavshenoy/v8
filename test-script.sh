
#!/bin/bash

# echo "Pranav: Triggeting v8 script"
# #install depot tools
# git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
# export PATH=/path/to/depot_tools:$PATH
# echo "Pranav: depot_tools installed. check it out"
# echo "$(depot_tools -help)"
#resolving dependencies
# echo "hi"
# gclient sync
# ./build/install-build-deps.sh


gn_dir="out.gn/x64.release.sample"
if [ ! -d "$gn_dir" ]; then
    echo "Initializing v8 builds"
    tools/dev/v8gen.py x64.release.sampe
fi





rm v8-run-*.log
rm v8_young_gen_*.log
rm hello_world
ninja -C out.gn/x64.release v8_monolith
ninja -C out.gn/x64.release  v8_hello_world
third_party/llvm-build/Release+Asserts/bin/clang++ /home/pranav/v8/src/out.gn/x64.release.sample/obj/v8_hello_world/hello-world.o /home/pranav/v8/src/out.gn/x64.release.sample/obj/libv8_monolith.a -o hello_world


#creating directory
TIMESTAMP=`date +%Y-%m-%d_%H-%M-%S`
mkdir "results/$TIMESTAMP/"


#multiply the factor by 512KB to get semi_space size. and again by 2 to get young gen size
initial_semispace_size_factor=( 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25)
benchmarks=( "acdc.js" "box2d.js" "code-first-load.js" "crypto.js"  "deltablue.js" "earley-boyer.js" "gbemu-part.js" "mandreel.js" "navier-stokes.js" "pdfjs.js" "raytrace.js" "regexp.js" "richards.js" "splay.js" "typescript.js" "zlib.js")
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
        echo "      semispace_size_factor: "$i
        rm "semispace_size.txt"
        echo $i >> "semispace_size.txt"
        ./hello_world $bm
        mv v8_young_gen_*.log $full_path
        mv v8-custom-log.log $full_path
    done
done
echo "Plotting charts"
python3 charts.py "results/$TIMESTAMP/"

