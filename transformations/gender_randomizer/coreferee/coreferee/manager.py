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

import importlib
import os
import pickle
import traceback
from sys import exc_info

import pkg_resources
import spacy
from packaging import version
from spacy.language import Language
from spacy.tokens import Doc, Token
from tensorflow import keras
from thinc.api import Config

from .annotation import Annotator
from .errors import (
    LanguageNotSupportedError,
    ModelNotSupportedError,
    MultiprocessingParsingNotSupportedError,
    VectorsModelHasWrongVersionError,
    VectorsModelNotInstalledError,
)

COMMON_MODELS_PACKAGE_NAMEPART = "coreferee_model_"

FEATURE_TABLE_FILENAME = "feature_table.bin"

KERAS_MODEL_FILENAME = "keras_ensemble.h5"


class CorefereeManager:
    @staticmethod
    def get_annotator(nlp: Language) -> Annotator:
        model_name = "_".join((nlp.meta["lang"], nlp.meta["name"]))
        relative_config_filename = os.sep.join(
            ("lang", nlp.meta["lang"], "config.cfg")
        )
        if not pkg_resources.resource_exists(
            __name__, relative_config_filename
        ):
            raise LanguageNotSupportedError(nlp.meta["lang"])
        absolute_config_filename = pkg_resources.resource_filename(
            __name__, relative_config_filename
        )
        config = Config().from_disk(absolute_config_filename)
        for config_entry_name, config_entry in config.items():
            if (
                nlp.meta["name"] == config_entry["model"]
                and version.parse(nlp.meta["version"])
                >= version.parse(config_entry["from_version"])
                and version.parse(nlp.meta["version"])
                <= version.parse(config_entry["to_version"])
            ):
                if "vectors_model" in config_entry:
                    try:
                        vectors_nlp = spacy.load(
                            "_".join(
                                (
                                    nlp.meta["lang"],
                                    config_entry["vectors_model"],
                                )
                            )
                        )
                    except OSError:
                        raise VectorsModelNotInstalledError(
                            "".join(
                                (
                                    "Model ",
                                    model_name,
                                    " is only supported in conjunction with model ",
                                    nlp.meta["lang"],
                                    "_",
                                    config_entry["vectors_model"],
                                    " which must be loaded using 'python -m spacy download ",
                                    nlp.meta["lang"],
                                    "_",
                                    config_entry["vectors_model"],
                                    "'.",
                                )
                            )
                        )
                    if version.parse(
                        vectors_nlp.meta["version"]
                    ) < version.parse(
                        config_entry["vectors_from_version"]
                    ) or version.parse(
                        vectors_nlp.meta["version"]
                    ) > version.parse(
                        config_entry["vectors_to_version"]
                    ):
                        raise VectorsModelHasWrongVersionError(
                            "".join(
                                (
                                    "Model ",
                                    model_name,
                                    " is only supported in conjunction with model ",
                                    nlp.meta["lang"],
                                    "_",
                                    config_entry["vectors_model"],
                                    " between versions ",
                                    config_entry["vectors_from_version"],
                                    " and ",
                                    config_entry["vectors_to_version"],
                                    " inclusive.",
                                )
                            )
                        )
                else:
                    vectors_nlp = nlp
                model_package_name = "".join(
                    (
                        COMMON_MODELS_PACKAGE_NAMEPART,
                        nlp.meta["lang"],
                        ".",
                        config_entry_name,
                    )
                )
                try:
                    importlib.import_module(model_package_name)
                except ModuleNotFoundError:
                    print(
                        "".join(
                            (
                                "Model could not be loaded for config entry '",
                                config_entry_name,
                                "' If models exist for language '",
                                nlp.meta["lang"],
                                "', load them with the command 'python -m coreferee install ",
                                nlp.meta["lang"],
                                "'.",
                            )
                        )
                    )
                    raise ModelNotSupportedError(
                        "".join(
                            (
                                nlp.meta["lang"],
                                "_",
                                nlp.meta["name"],
                                " version ",
                                nlp.meta["version"],
                            )
                        )
                    )
                this_feature_table_filename = pkg_resources.resource_filename(
                    model_package_name, FEATURE_TABLE_FILENAME
                )
                with open(
                    this_feature_table_filename, "rb"
                ) as feature_table_file:
                    feature_table = pickle.load(feature_table_file)
                absolute_keras_model_filename = (
                    pkg_resources.resource_filename(
                        model_package_name, KERAS_MODEL_FILENAME
                    )
                )
                keras_ensemble = keras.models.load_model(
                    absolute_keras_model_filename
                )
                return Annotator(
                    nlp, vectors_nlp, feature_table, keras_ensemble
                )
        raise ModelNotSupportedError(
            "".join(
                (
                    nlp.meta["lang"],
                    "_",
                    nlp.meta["name"],
                    " version ",
                    nlp.meta["version"],
                )
            )
        )


@Language.factory("coreferee")
class CorefereeBroker:
    def __init__(self, nlp: Language, name: str):
        self.nlp = nlp
        self.pid = os.getpid()
        self.annotator = CorefereeManager().get_annotator(nlp)

    def __call__(self, doc: Doc) -> Doc:
        if os.getpid() != self.pid:
            raise MultiprocessingParsingNotSupportedError(
                "Unfortunately at present parsing cannot be shared between forked processes."
            )
        try:
            self.annotator.annotate(doc)
        except:
            print("Unexpected error annotating document, skipping ....")
            exception_info_parts = exc_info()
            print(exception_info_parts[0])
            print(exception_info_parts[1])
            traceback.print_tb(exception_info_parts[2])
        return doc

    def __getstate__(self):
        return self.nlp.meta

    def __setstate__(self, meta):
        nlp_name = "_".join((meta["lang"], meta["name"]))
        self.nlp = spacy.load(nlp_name)
        self.annotator = CorefereeManager().get_annotator(self.nlp)
        self.pid = os.getpid()
        CorefereeBroker.set_extensions()

    @staticmethod
    def set_extensions():
        if not Doc.has_extension("coref_chains"):
            Doc.set_extension("coref_chains", default=None)
        if not Token.has_extension("coref_chains"):
            Token.set_extension("coref_chains", default=None)
