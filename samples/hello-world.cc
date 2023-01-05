// Copyright 2015 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <chrono>
#include <future>
#include<v8.h>

#include "include/libplatform/libplatform.h"
#include "include/v8-context.h"
#include "include/v8-initialization.h"
#include "include/v8-isolate.h"
#include "include/v8-local-handle.h"
#include "include/v8-primitive.h"
#include "include/v8-script.h"
#include "include/v8-container.h"
#include "include/v8-template.h"


inline std::string read_file(const std::string& path) {
  // if (!std::filesystem::exists(path)) {
  //   // std::cout << "ERROR! " << path << " not exist!" << std::endl;
  //   return "";
  // }
  std::ifstream t(path);
  return std::string((std::istreambuf_iterator<char>(t)),
                     std::istreambuf_iterator<char>());
}

inline v8::Local<v8::String> fromString(v8::Isolate* isolate, const std::string& str) {
  return v8::String::NewFromUtf8(isolate, str.data()).ToLocalChecked();
}

void Print(const v8::FunctionCallbackInfo<v8::Value>& args) {
  // print only work when there is a single isolate running. should find a way to bind isolate.
  // but we also can just not care about printing. the code doesnt print anything important.
  // the below code is kept for debugging purpose.
  // v8::String::Utf8Value str(isolate, args[0]);
  // fwrite(*str, sizeof(**str), str.length(), stdout);
  // fprintf(stdout, "\n");
  // fflush(stdout);
}

struct Input {
  std::string size;
  std::string liveness;
  std::string duration;
};

struct Signal {
  std::mutex m;
  Signal() {
    m.lock();
  }

  void wait() {
    m.lock();
    m.unlock();
  }

  void signal() {
    m.unlock();
  }
};


const std::string iterations = "1500";
std::string getSplay() {

  std::string browserbench_path = "/home/pranav/WebKit/Websites/browserbench.org/";
  std::string jetstream2_path = browserbench_path + "JetStream2.0/";
  std::string octane_path = jetstream2_path + "Octane/";
  std::string header = "let performance = {now() { return 0; }};";
  std::string footer = "for(i = 0; i < "+iterations+"; i++) {new Benchmark().runIteration();}";
  std::string input = header + read_file(octane_path + "splay.js") + footer;
  return input;
}

std::string getpdfjs() {

  std::string browserbench_path = "/home/pranav/WebKit/Websites/browserbench.org/";
  std::string jetstream2_path = browserbench_path + "JetStream2.0/";
  std::string octane_path = jetstream2_path + "Octane/";
  std::string header = "let performance = {now() { return 0; }};";
  std::string footer = "for(i = 0; i < "+iterations+"; i++) {new Benchmark().runIteration();}";
  std::string input = header + read_file(octane_path + "pdfjs.js") + footer;
  return input;
}

std::string getTypeScript() {

  std::string browserbench_path = "/home/pranav/WebKit/Websites/browserbench.org/";
  std::string jetstream2_path = browserbench_path + "JetStream2.0/";
  std::string octane_path = jetstream2_path + "Octane/";
  std::string header = "let performance = {now() { return 0; }};";
  std::string footer = "for(i = 0; i < "+iterations+"; i++) {new Benchmark().runIteration();}";
  std::string input = header + read_file(octane_path + "typescript-compiler.js")
       + read_file(octane_path + "typescript-input.js")
       + read_file(octane_path + "typescript.js")
       + footer;
  return input;
}

std::string getZlibScript() {

  std::string browserbench_path = "/home/pranav/WebKit/Websites/browserbench.org/";
  std::string jetstream2_path = browserbench_path + "JetStream2.0/";
  std::string octane_path = jetstream2_path + "Octane/";
  std::string header = "let performance = {now() { return 0; }};";
  std::string footer = "for(i = 0; i < "+iterations+"; i++) {new Benchmark().runIteration();}";
  std::string input = header + read_file(octane_path + "zlib-data.js")
       + read_file(octane_path + "zlib.js");
  return input;
}

std::string getGbemuScript() {

  std::string browserbench_path = "/home/pranav/WebKit/Websites/browserbench.org/";
  std::string jetstream2_path = browserbench_path + "JetStream2.0/";
  std::string octane_path = jetstream2_path + "Octane/";
  std::string header = "let performance = {now() { return 0; }};";
  std::string footer = "for(i = 0; i < "+iterations+"; i++) {new Benchmark().runIteration();}";
  std::string input = header + read_file(octane_path + "gbemu-part1.js")
       + read_file(octane_path + "gbemu-part2.js");
  return input;
}

//full js script name as input
std::string getScript(std::string name) {

  if(name.compare("typescript.js") == 0) {
    return getTypeScript();
  }
  if(name.compare("zlib.js") == 0) {
    return getZlibScript();
  }
  if(name.compare("gbemu-part.js") == 0) {
    return getGbemuScript();
  }

  std::string browserbench_path = "/home/pranav/WebKit/Websites/browserbench.org/";
  std::string jetstream2_path = browserbench_path + "JetStream2.0/";
  std::string octane_path = jetstream2_path + "Octane/";
  std::string header = "let performance = {now() { return 0; }};";
  std::string footer = "for(i = 0; i < "+iterations+"; i++) {new Benchmark().runIteration();}";
  std::string input = header + read_file(octane_path + name) + footer;
  // std::cout<<read_file(octane_path + name).length()<<"\n";
  return input;
}

void run_acdc(const Input& input, Signal *s) {
  v8::Isolate::CreateParams create_params;
  create_params.array_buffer_allocator =
    v8::ArrayBuffer::Allocator::NewDefaultAllocator();
  v8::Isolate* isolate = v8::Isolate::New(create_params);
  // isolate->SetName("acdc_" + input.size + "_" + input.liveness);
  {
    v8::Isolate::Scope isolate_scope(isolate);
    v8::HandleScope handle_scope(isolate);
    v8::Local<v8::Context> context = v8::Context::New(isolate);
    v8::Context::Scope context_scope(context);
    {
      v8::Local<v8::String> source = fromString(isolate, read_file("/home/pranav/v8/src/samples/acdc.js"));
      v8::Local<v8::Script> script =
        v8::Script::Compile(context, source).ToLocalChecked();
      {
        std::vector<std::string> args = {"minSize", input.size, "maxSize", input.size, "benchmarkDuration", input.duration, "minLiveness", input.liveness, "maxLiveness", input.liveness};
        v8::Local<v8::Array> array = v8::Array::New(isolate, static_cast<int>(args.size()));
        for (int i = 0; i < args.size(); i++) {
          v8::Local<v8::String> arg =
            v8::String::NewFromUtf8(isolate, args[i].c_str()).ToLocalChecked();
          v8::Local<v8::Number> index = v8::Number::New(isolate, i);
          array->Set(context, index, arg).FromJust();
        }
        v8::Local<v8::String> name = v8::String::NewFromUtf8Literal(isolate, "arguments", v8::NewStringType::kInternalized);
        context->Global()->Set(context, name, array).FromJust();
      }
      {
        auto print_tmpl = v8::FunctionTemplate::New(isolate, Print);
        auto print_val = print_tmpl->GetFunction(context).ToLocalChecked();
        v8::Local<v8::String> name = v8::String::NewFromUtf8Literal(isolate, "print", v8::NewStringType::kInternalized);
        context->Global()->Set(context, name, print_val).FromJust();
      }
      s->wait();
      script->Run(context);
    }
  }
  std::this_thread::sleep_for (std::chrono::seconds(5));
  std::cout << "try isolate->dispose!" << std::endl;
  isolate->Dispose();
  std::cout << "isolate->dispose ok!" << std::endl;
}

void acdc() {
  std::vector<std::future<void>> futures;
  Signal s;
  futures.push_back(std::async(std::launch::async,
                               run_acdc,
                               Input {/*size=*/"8", /*liveness=*/"16", /*duration=*/"400"},
                               &s));
  futures.push_back(std::async(std::launch::async,
                               run_acdc,
                              //  platform,
                               Input {/*size=*/"64", /*liveness=*/"128", /*duration=*/"600"},
                               &s));
  futures.push_back(std::async(std::launch::async,
                               run_acdc,
                              //  platform,
                               Input {/*size=*/"8", /*liveness=*/"1", /*duration=*/"800"},
                               &s));
  futures.push_back(std::async(std::launch::async,
                               run_acdc,
                              //  platform,
                               Input {/*size=*/"64", /*liveness=*/"8", /*duration=*/"4000"},
                               &s));
  s.signal();
  for (auto& f: futures) {
    f.get();
  }
}





int main(int argc, char* argv[]) {
  
  char* pgm = argv[1];
  
  // Initialize V8.
  v8::V8::InitializeICUDefaultLocation(argv[0]);
  v8::V8::InitializeExternalStartupData(argv[0]);
  std::unique_ptr<v8::Platform> platform = v8::platform::NewDefaultPlatform();
  v8::V8::InitializePlatform(platform.get());
  v8::V8::Initialize();

  // Create a new Isolate and make it the current one.
  v8::Isolate::CreateParams create_params;
  create_params.array_buffer_allocator =
      v8::ArrayBuffer::Allocator::NewDefaultAllocator();
  v8::Isolate* isolate = v8::Isolate::New(create_params);
  {
    v8::Isolate::Scope isolate_scope(isolate);

    // Create a stack-allocated handle scope.
    v8::HandleScope handle_scope(isolate);

    // Create a new context.
    v8::Local<v8::Context> context = v8::Context::New(isolate);

    // Enter the context for compiling and running the hello world script.
    v8::Context::Scope context_scope(context);

    if(strcmp(pgm, "acdc.js") == 0) {
      printf("Testing %s\n", pgm);
      acdc();
      return 0;
    }
    //TODO: revert
    printf("Testing %s\n", pgm);
    // Create a string containing the JavaScript source code.
    v8::Local<v8::String> source = fromString(isolate, getScript(pgm));
    // v8::Local<v8::String> source = v8::String::NewFromUtf8Literal(isolate, getJS());

    // Compile the source code.
    v8::Local<v8::Script> script =
        v8::Script::Compile(context, source).ToLocalChecked();

    // Run the script to get the result.
    v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

    //TODO: revert
    // // Convert the result to an UTF8 string and print it.
    // v8::String::Utf8Value utf8(isolate, result);
    // if(pgm[0] == 's') {
    //   printf("Testing splay\n");
    //   // Create a string containing the JavaScript source code.
    //   v8::Local<v8::String> source = fromString(isolate, getSplay());
    //   // v8::Local<v8::String> source = v8::String::NewFromUtf8Literal(isolate, getJS());

    //   // Compile the source code.
    //   v8::Local<v8::Script> script =
    //       v8::Script::Compile(context, source).ToLocalChecked();

    //   // Run the script to get the result.
    //   v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

    //   // Convert the result to an UTF8 string and print it.
    //   // v8::String::Utf8Value utf8(isolate, result);
    //   // printf("%s\n", *utf8);
    // } else if(pgm[0] == 't') {

    //   printf("Testing typescript\n");
    //   // Create a string containing the JavaScript source code.
    //   v8::Local<v8::String> source = fromString(isolate, getTypeScript());
    //   // v8::Local<v8::String> source = v8::String::NewFromUtf8Literal(isolate, getJS());

    //   // Compile the source code.
    //   v8::Local<v8::Script> script =
    //       v8::Script::Compile(context, source).ToLocalChecked();

    //   // Run the script to get the result.
    //   v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

    //   // Convert the result to an UTF8 string and print it.
    //   // v8::String::Utf8Value utf8(isolate, result);
    //   // printf("%s\n", *utf8);
    // } else if(pgm[0] == 'p') {
    //   printf("Testing pdfjs\n");
    //   // Create a string containing the JavaScript source code.
    //   v8::Local<v8::String> source = fromString(isolate, getpdfjs());
    //   // v8::Local<v8::String> source = v8::String::NewFromUtf8Literal(isolate, getJS());

    //   // Compile the source code.
    //   v8::Local<v8::Script> script =
    //       v8::Script::Compile(context, source).ToLocalChecked();

    //   // Run the script to get the result.
    //   v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

    //   // Convert the result to an UTF8 string and print it.
    //   v8::String::Utf8Value utf8(isolate, result);
      
    // } else if(pgm[0] == 'a'){
    //   printf("Running ACDC\n");
    //   acdc();
    // } else {
    //   printf("please enter right argument %s", pgm);
    // }
    // {
    //   // Create a string containing the JavaScript source code.
    //   v8::Local<v8::String> source =
    //       v8::String::NewFromUtf8Literal(isolate, "'Hello' + ', World!'");

    //   // Compile the source code.
    //   v8::Local<v8::Script> script =
    //       v8::Script::Compile(context, source).ToLocalChecked();

    //   // Run the script to get the result.
    //   v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

    //   // Convert the result to an UTF8 string and print it.
    //   v8::String::Utf8Value utf8(isolate, result);
    //   printf("%s\n", *utf8);
    // }

    // {
    //   // Use the JavaScript API to generate a WebAssembly module.
    //   //
    //   // |bytes| contains the binary format for the following module:
    //   //
    //   //     (func (export "add") (param i32 i32) (result i32)
    //   //       get_local 0
    //   //       get_local 1
    //   //       i32.add)
    //   //
    //   const char csource[] = R"(
    //     let bytes = new Uint8Array([
    //       0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x07, 0x01,
    //       0x60, 0x02, 0x7f, 0x7f, 0x01, 0x7f, 0x03, 0x02, 0x01, 0x00, 0x07,
    //       0x07, 0x01, 0x03, 0x61, 0x64, 0x64, 0x00, 0x00, 0x0a, 0x09, 0x01,
    //       0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a, 0x0b
    //     ]);
    //     let module = new WebAssembly.Module(bytes);
    //     let instance = new WebAssembly.Instance(module);
    //     instance.exports.add(3, 4);
    //   )";

    //   // Create a string containing the JavaScript source code.
    //   v8::Local<v8::String> source =
    //       v8::String::NewFromUtf8Literal(isolate, csource);

    //   // Compile the source code.
    //   v8::Local<v8::Script> script =
    //       v8::Script::Compile(context, source).ToLocalChecked();

    //   // Run the script to get the result.
    //   v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

    //   // Convert the result to a uint32 and print it.
    //   uint32_t number = result->Uint32Value(context).ToChecked();
    //   printf("3 + 4 = %u\n", number);
    // }
  }

  // Dispose the isolate and tear down V8.
  isolate->Dispose();
  v8::V8::Dispose();
  v8::V8::DisposePlatform();
  delete create_params.array_buffer_allocator;
  return 0;
}
