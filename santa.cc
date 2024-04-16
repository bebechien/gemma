// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Command line text interface to gemma.

#include <ctime>
#include <iostream>
#include <random>
#include <string>
#include <thread>  // NOLINT
#include <vector>

// copybara:import_next_line:gemma_cpp
#include "compression/compress.h"
// copybara:import_next_line:gemma_cpp
#include "gemma.h"    // Gemma
// copybara:import_next_line:gemma_cpp
#include "util/app.h"
// copybara:import_next_line:gemma_cpp
#include "util/args.h"  // HasHelp
#include "hwy/base.h"
#include "hwy/contrib/thread_pool/thread_pool.h"
#include "hwy/highway.h"
#include "hwy/per_target.h"
#include "hwy/profiler.h"
#include "hwy/timer.h"

darkchien@bonobono:~/gemma.cpp$ more simple.cc 
// Copyright 2024 Google LLC
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Command line text interface to gemma.

#include <ctime>
#include <iostream>
#include <random>
#include <string>
#include <thread>  // NOLINT
#include <vector>

// copybara:import_next_line:gemma_cpp
#include "compression/compress.h"
// copybara:import_next_line:gemma_cpp
#include "gemma.h"    // Gemma
// copybara:import_next_line:gemma_cpp
#include "util/app.h"
// copybara:import_next_line:gemma_cpp
#include "util/args.h"  // HasHelp
#include "hwy/base.h"
#include "hwy/contrib/thread_pool/thread_pool.h"
#include "hwy/highway.h"
#include "hwy/per_target.h"
#include "hwy/profiler.h"
#include "hwy/timer.h"

namespace gcpp {

void RunSimple(LoaderArgs& loader, InferenceArgs& inference, AppArgs& app, std::string prompt_string) {
  hwy::ThreadPool inner_pool(0);
  hwy::ThreadPool pool(app.num_threads);
  // For many-core, pinning threads to cores helps.
  if (app.num_threads > 10) {
    PinThreadToCore(app.num_threads - 1);  // Main thread

    pool.Run(0, pool.NumThreads(),
             [](uint64_t /*task*/, size_t thread) { PinThreadToCore(thread); });
  }

  gcpp::Gemma model(loader, pool);

  int abs_pos = 0;      // absolute token index over all turns
  int current_pos = 0;  // token index within the current turn
  int prompt_size{};

  std::mt19937 gen;
  if (inference.deterministic) {
    gen.seed(42);
  } else {
    std::random_device rd;
    gen.seed(rd());
  }

  std::vector<int> prompt;

  HWY_ASSERT(model.Tokenizer().Encode(prompt_string, &prompt).ok());

  int verbosity = app.verbosity;

  // callback function invoked for each generated token.
  auto stream_token = [&abs_pos, &current_pos, &inference, &gen, &prompt_size,
                       tokenizer = &model.Tokenizer(),
                       verbosity](int token, float) {
    ++abs_pos;
    ++current_pos;
    if (current_pos < prompt_size) {
      std::cerr << "." << std::flush;
    } else if (token == gcpp::EOS_ID) {
      if (!inference.multiturn) {
        abs_pos = 0;
        if (inference.deterministic) {
          gen.seed(42);
        }
      }
      if (verbosity >= 2) {
        std::cout << "\n[ End ]" << std::endl;
      }
    } else {
      std::string token_text;
      HWY_ASSERT(tokenizer->Decode(std::vector<int>{token}, &token_text).ok());
      // +1 since position is incremented above
      if (current_pos == prompt_size + 1) {
        // first token of response
        token_text.erase(0, token_text.find_first_not_of(" \t\n"));
        if (verbosity >= 1) {
          std::cout << std::endl << std::endl;
        }
      }
      // TODO(austinvhuang): is explicit space necessary?
      std::cout << token_text << std::flush;
    }
    return true;
  };

  if (abs_pos == 0) {
    prompt.insert(prompt.begin(), 2);
  }
  prompt_size = prompt.size();

  GenerateGemma(model, inference, prompt, abs_pos, pool, inner_pool, stream_token,
                  /*accept_token=*/[](int){return true;}, gen, verbosity);

  std::cout << "\n\n";
}

}  // namespace gcpp

#include <fstream>
#include <sstream>

#define MODEL_PATH "/home/darkchien/model/"

int main(int argc, char** argv) {
  gcpp::LoaderArgs loader(argc, argv);
  gcpp::InferenceArgs inference(argc, argv);
  gcpp::AppArgs app(argc, argv);

  loader.tokenizer.path = MODEL_PATH"tokenizer.spm";
  loader.cache.path = MODEL_PATH"2b-it-sfp.sbs";
  loader.model_type = "2b-it";

  const char *system_pre = "You are Santa Claus, write a letter back from this kid.\n<start_of_turn>user\n";
  const char *system_post = "<end_of_turn>\n<start_of_turn>model\n";

  std::ifstream letter("letter.txt");
  std::stringstream buffer;
  buffer << system_pre << letter.rdbuf() << system_post;
  letter.close();

  gcpp::RunSimple(loader, inference, app, buffer.str());
  return 0;
}
