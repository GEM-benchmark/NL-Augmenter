# Copyright 2021 msg systems ag

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import warnings

warnings.filterwarnings("ignore", message=r"\[W007\]", category=UserWarning)

import coreferee.manager

coreferee.manager.CorefereeBroker.set_extensions()
