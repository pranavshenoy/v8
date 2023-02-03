#!/bin/bash

depot_tools_dir="../depot_tools"

if [ ! -d $depot_tools_dir ];
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    export PATH=$depot_tools_dir:$PATH
    echo "depot tool installed"

gn_dir="out.gn/x64.release.sample"
if [ ! -d $gn_dir ];

    gclient root
    gclient config --spec "solutions = [
    {
        \"name\": \"src\",
        \"url\": \"git@github.com:pranavshenoy/v8.git\",
        \"managed\": False,
        \"custom_deps\": {},
        \"custom_vars\": {},
    },
    ]
    "
    gclient sync
    tools/dev/v8gen.py x64.release.sample
    
    echo "out.gn generated"

