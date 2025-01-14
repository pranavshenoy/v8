
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


# export PATH="/home/pranav/depot_tools":$PATH
# echo "here you go!!!....$(which gclient)"
# gn_dir="out.gn/x64.release.sample"
# depot_tools_dir="../depot_tools/"
# rm -rf $gn_dir #todo: remove later

# if [ ! -d "$depot_tools_dir" ]; then
#     cd ..
#     git clone 
# fi



# if [ ! -d "$gn_dir" ]; then
    
#     echo "Initializing v8 builds"
#     gclient root

#     gclient config --spec "solutions = [
#   {
#     \"name\": \"src\",
#     \"url\": \"git@github.com:pranavshenoy/v8.git\",
#     \"managed\": False,
#     \"custom_deps\": {},
#     \"custom_vars\": {},
#   },
# ]
# "

#     gclient sync --nohooks --no-history
#     echo "Installing build deps"
#     ./build/install-build-deps.sh
#     #pip3 install mb
#     pip3 install gn_helpers
#     tools/dev/v8gen.py x64.release.sample
#     # add more args to gn
# fi


rm v8-run-*.log
rm v8_young_gen_*.log
rm hello_world
ninja -C out.gn/x64.release.sample v8_monolith
ninja -C out.gn/x64.release.sample  v8_hello_world
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
        # ./hello_world $bm
        export USE_MEMBALANCER=1 LOG_DIRECTORY=$full_path LOG_GC=1 C_VALUE=1;  bash -c './hello_world $bm'
        mv v8_young_gen_*.log $full_path
        mv v8-custom-log.log $full_path
    done
done
echo "Plotting charts"
python3 charts.py "results/$TIMESTAMP/"

