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


class CorefereeError(Exception):
    def __init__(self, text: str = ""):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return self.text


class LanguageNotSupportedError(CorefereeError):
    pass


class ModelNotSupportedError(CorefereeError):
    pass


class VectorsModelNotInstalledError(CorefereeError):
    pass


class VectorsModelHasWrongVersionError(CorefereeError):
    pass


class MultiprocessingParsingNotSupportedError(CorefereeError):
    pass
