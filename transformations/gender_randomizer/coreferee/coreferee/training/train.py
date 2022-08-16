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

import bisect
import os
import pickle
import shutil
import sys
import time
from datetime import datetime

import pkg_resources
import spacy
from packaging import version
from thinc.api import Config

from ..annotation import Annotator
from ..errors import LanguageNotSupportedError
from ..manager import (
    COMMON_MODELS_PACKAGE_NAMEPART,
    FEATURE_TABLE_FILENAME,
    KERAS_MODEL_FILENAME,
)
from ..rules import RulesAnalyzerFactory
from ..tendencies import ENSEMBLE_SIZE, TendenciesAnalyzer
from .loaders import GenericLoader
from .model import ModelGenerator


class TrainingManager:
    def __init__(
        self,
        root_path: str,
        lang: str,
        loader_classes: str,
        data_dir: str,
        log_dir: str,
    ):
        self.file_system_root = pkg_resources.resource_filename(root_path, "")
        relative_config_filename = os.sep.join(("lang", lang, "config.cfg"))
        if not pkg_resources.resource_exists(
            root_path, relative_config_filename
        ):
            raise LanguageNotSupportedError(lang)
        self.config = Config().from_disk(
            os.sep.join((self.file_system_root, relative_config_filename))
        )
        loader_classnames = loader_classes.split(",")
        self.loaders = []
        for loader_classname in loader_classnames:
            class_ = getattr(
                sys.modules["coreferee.training.loaders"], loader_classname
            )
            self.loaders.append(class_())
        self.lang = lang
        self.models_dirname = os.sep.join(
            (self.file_system_root, "..", "models", lang)
        )
        if not os.path.isdir(self.models_dirname):
            self.set_up_models_dir()

        self.relevant_config_entry_names = []
        self.nlp_dict = {}
        for config_entry_name, config_entry in self.config.items():
            this_model_dir = "".join(
                (
                    self.models_dirname,
                    os.sep,
                    "".join((COMMON_MODELS_PACKAGE_NAMEPART, self.lang)),
                    os.sep,
                    config_entry_name,
                )
            )
            if not os.path.isdir(this_model_dir):
                self.relevant_config_entry_names.append(config_entry_name)
                model_name = "_".join((lang, config_entry["model"]))
                self.load_model(
                    model_name,
                    config_entry_name,
                    config_entry["from_version"],
                    config_entry["to_version"],
                )
                if "vectors_model" in config_entry:
                    vectors_model_name = "_".join(
                        (lang, config_entry["vectors_model"])
                    )
                    self.load_model(
                        vectors_model_name,
                        config_entry_name,
                        config_entry["vectors_from_version"],
                        config_entry["vectors_to_version"],
                        is_vector_model=True,
                    )
            else:
                print(
                    "Skipping config entry",
                    config_entry_name,
                    "as model exists",
                )

        self.log_dir = log_dir
        if ".." in log_dir:
            print(".. not permitted in log_dir")
            sys.exit(1)
        if not os.path.isdir(self.log_dir):
            os.makedirs(self.log_dir)

        if not os.path.isdir(data_dir):
            print("Data directory", data_dir, "not found.")
            sys.exit(1)
        self.data_dir = data_dir

        temp_dir = os.sep.join((self.log_dir, "temp"))
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
        time.sleep(1)
        os.mkdir(temp_dir)

    def load_model(
        self,
        name,
        config_entry_name,
        from_version,
        to_version,
        *,
        is_vector_model=False
    ):
        if name not in self.nlp_dict:
            print("Loading model", name, "...")
            try:
                nlp = spacy.load(name)
            except OSError:
                if is_vector_model:
                    print(
                        "Config entry",
                        config_entry_name,
                        "specifies a vectors model",
                        name,
                        "that cannot be loaded.",
                    )
                else:
                    print(
                        "Config entry",
                        config_entry_name,
                        "specifies a model",
                        name,
                        "that cannot be loaded.",
                    )
                sys.exit(1)
        else:
            nlp = self.nlp_dict[name]
        if version.parse(nlp.meta["version"]) < version.parse(
            from_version
        ) or version.parse(nlp.meta["version"]) > version.parse(to_version):
            if is_vector_model:
                print(
                    "Config entry",
                    config_entry_name,
                    "specifies a version range for vectors model",
                    name,
                    "that does not include the loaded version.",
                )
            else:
                print(
                    "Config entry",
                    config_entry_name,
                    "specifies a version range for model",
                    name,
                    "that does not include the loaded version.",
                )
            sys.exit(1)
        self.nlp_dict[name] = nlp

    def set_up_models_dir(self):
        os.mkdir(self.models_dirname)
        package_dirname = "".join((COMMON_MODELS_PACKAGE_NAMEPART, self.lang))
        os.mkdir(os.sep.join((self.models_dirname, package_dirname)))
        setup_cfg_filename = os.sep.join((self.models_dirname, "setup.cfg"))
        with open(setup_cfg_filename, "w") as setup_cfg_file:
            self.writeln(setup_cfg_file, "[metadata]")
            self.writeln(
                setup_cfg_file, "name = ", package_dirname.replace("_", "-")
            )
            self.writeln(setup_cfg_file, "version = 1.0.0")
            self.writeln(setup_cfg_file)
            self.writeln(setup_cfg_file, "[options]")
            self.writeln(setup_cfg_file, "packages = find:")
            self.writeln(setup_cfg_file, "include_package_data = True")
            self.writeln(setup_cfg_file)
            self.writeln(setup_cfg_file, "[options.package_data]")
            self.writeln(setup_cfg_file, "* = *.bin, *.h5")
        pyproject_toml_filename = os.sep.join(
            (self.models_dirname, "pyproject.toml")
        )
        with open(pyproject_toml_filename, "w") as pyproject_toml_file:
            self.writeln(pyproject_toml_file, "[build-system]")
            self.writeln(pyproject_toml_file, "requires = [")
            self.writeln(pyproject_toml_file, '  "setuptools",')
            self.writeln(pyproject_toml_file, '  "wheel",')
            self.writeln(pyproject_toml_file, "]")
            self.writeln(
                pyproject_toml_file, 'build-backend = "setuptools.build_meta"'
            )
        init_py_filename = os.sep.join(
            (self.models_dirname, package_dirname, "__init__.py")
        )
        with open(init_py_filename, "w") as init_py_file:
            self.writeln(init_py_file)

    @staticmethod
    def writeln(file, *args):
        file.write("".join(("".join([str(arg) for arg in args]), "\n")))

    def log_incorrect_annotation(
        self,
        temp_log_file,
        token,
        correct_referred_token,
        incorrect_referred_token,
    ):
        doc = token.doc
        self.writeln(temp_log_file, "Incorrect annotation:")
        start_token_index = min(
            correct_referred_token.i, incorrect_referred_token.i
        )
        sentence_start_index = doc._.coref_chains.temp_sent_starts[
            doc[start_token_index]._.coref_chains.temp_sent_index
        ]
        if token._.coref_chains.temp_sent_index + 1 == len(
            doc._.coref_chains.temp_sent_starts
        ):
            self.writeln(temp_log_file, doc[sentence_start_index:])
            self.writeln(
                temp_log_file,
                "Tokens from ",
                sentence_start_index,
                " to the end:",
            )
            self.writeln(temp_log_file, doc[sentence_start_index:])
        else:
            sentence_end_index = doc._.coref_chains.temp_sent_starts[
                token._.coref_chains.temp_sent_index + 1
            ]
            self.writeln(
                temp_log_file,
                "Tokens ",
                sentence_start_index,
                " to ",
                sentence_end_index,
                ":",
            )
            self.writeln(
                temp_log_file, doc[sentence_start_index:sentence_end_index]
            )
        self.writeln(
            temp_log_file, "Referring pronoun: ", token, " at index ", token.i
        )
        for (
            potential_referred
        ) in token._.coref_chains.temp_potential_referreds:
            if hasattr(potential_referred, "true_in_training"):
                self.writeln(
                    temp_log_file,
                    "Training referred mentions: ",
                    potential_referred.pretty_representation,
                )
        self.writeln(
            temp_log_file,
            "Annotated referred mentions: ",
            [chain.pretty_representation for chain in token._.coref_chains],
        )
        self.writeln(temp_log_file)

    def generate_keras_ensemble(
        self,
        model_generator,
        temp_log_file,
        training_docs,
        tendencies_analyzer,
    ):
        keras_model = model_generator.generate_keras_model(
            training_docs, tendencies_analyzer, ENSEMBLE_SIZE
        )
        self.writeln(temp_log_file)
        self.writeln(temp_log_file, "Generated Keras model:")
        keras_model.summary(
            print_fn=lambda line: self.writeln(temp_log_file, line)
        )
        self.writeln(temp_log_file, "Training model ...")
        keras_history = model_generator.train_keras_model(
            training_docs, tendencies_analyzer, keras_model
        )
        for index in range(ENSEMBLE_SIZE):
            keras_accuracy = keras_history.history[
                "_".join(("output", str(index), "binary_accuracy"))
            ][-1]
            self.writeln(
                temp_log_file, "Sub-network ", index, " within ensemble:"
            )
            self.writeln(
                temp_log_file,
                "Binary accuracy after training is ",
                keras_accuracy,
            )
        return keras_model

    def load_documents(self, nlp, rules_analyzer):
        docs = []
        for loader in self.loaders:
            docs.extend(loader.load(self.data_dir, nlp, rules_analyzer))
        return docs

    def train_model(self, config_entry_name, config_entry, temp_log_file):
        self.writeln(temp_log_file, "Config entry name: ", config_entry_name)
        nlp_name = "_".join((self.lang, config_entry["model"]))
        nlp = self.nlp_dict[nlp_name]
        self.writeln(
            temp_log_file,
            "Spacy model: ",
            nlp_name,
            " version ",
            nlp.meta["version"],
        )
        if "vectors_model" in config_entry:
            vectors_nlp_name = "_".join(
                (self.lang, config_entry["vectors_model"])
            )
            vectors_nlp = self.nlp_dict[vectors_nlp_name]
            self.writeln(
                temp_log_file,
                "Spacy vectors model: ",
                vectors_nlp_name,
                " version ",
                vectors_nlp.meta["version"],
            )
        else:
            vectors_nlp = nlp
            self.writeln(
                temp_log_file, "Main model is being used as vectors model"
            )

        rules_analyzer = RulesAnalyzerFactory().get_rules_analyzer(nlp)
        docs = self.load_documents(nlp, rules_analyzer)
        # Separate into training and test for first run
        total_words = 0
        docs_to_total_words_position = []
        for doc in docs:
            docs_to_total_words_position.append(total_words)
            total_words += len(doc)
        split_index = bisect.bisect_right(
            docs_to_total_words_position, total_words * 0.8
        )
        training_docs = docs[:split_index]
        test_docs = docs[split_index:]
        self.writeln(temp_log_file, "Total words: ", total_words)
        self.writeln(
            temp_log_file,
            "Training docs: ",
            len(training_docs),
            "; test docs: ",
            len(test_docs),
        )
        model_generator = ModelGenerator(config_entry_name, nlp, vectors_nlp)
        feature_table = model_generator.generate_feature_table(training_docs)
        self.writeln(temp_log_file, "Feature table: ", feature_table.__dict__)
        tendencies_analyzer = TendenciesAnalyzer(
            rules_analyzer, vectors_nlp, feature_table
        )
        keras_ensemble = self.generate_keras_ensemble(
            model_generator, temp_log_file, training_docs, tendencies_analyzer
        )
        annotator = Annotator(nlp, vectors_nlp, feature_table, keras_ensemble)
        self.writeln(temp_log_file)
        correct_counter = incorrect_counter = 0
        for test_doc in test_docs:
            annotator.annotate(test_doc, used_in_training=True)
            self.writeln(temp_log_file, "test_doc ", test_doc[:100], "... :")
            self.writeln(temp_log_file)
            self.writeln(temp_log_file, "Coref chains:")
            self.writeln(temp_log_file)
            for chain in test_doc._.coref_chains:
                self.writeln(temp_log_file, chain.pretty_representation)
            self.writeln(temp_log_file)
            self.writeln(temp_log_file, "Incorrect annotations:")
            self.writeln(temp_log_file)
            for token in test_doc:
                if hasattr(token._.coref_chains, "temp_potential_referreds"):
                    for (
                        potential_referred
                    ) in token._.coref_chains.temp_potential_referreds:
                        if hasattr(potential_referred, "true_in_training"):
                            for chain in token._.coref_chains:
                                if potential_referred in chain:
                                    correct_counter += 1
                                else:
                                    incorrect_counter += 1
                                    self.log_incorrect_annotation(
                                        temp_log_file,
                                        token,
                                        token.doc[
                                            potential_referred.root_index
                                        ],
                                        token.doc[
                                            chain.mentions[0].root_index
                                        ],
                                    )
        if len(test_docs) > 0:
            accuracy = round(
                100 * correct_counter / (correct_counter + incorrect_counter),
                2,
            )
            self.writeln(temp_log_file)
            self.writeln(
                temp_log_file,
                "Correct: ",
                correct_counter,
                "; Incorrect: ",
                incorrect_counter,
                " (",
                accuracy,
                "%)",
            )
            print("Accuracy: ", "".join((str(accuracy), "%")))
        self.writeln(temp_log_file)
        self.writeln(temp_log_file, "Retraining with all documents")
        self.writeln(temp_log_file)
        docs = self.load_documents(nlp, rules_analyzer)
        feature_table = model_generator.generate_feature_table(docs)
        self.writeln(temp_log_file, "Feature table: ", feature_table.__dict__)
        tendencies_analyzer = TendenciesAnalyzer(
            rules_analyzer, vectors_nlp, feature_table
        )
        keras_ensemble = self.generate_keras_ensemble(
            model_generator, temp_log_file, docs, tendencies_analyzer
        )
        this_model_dir = os.sep.join(
            (
                self.models_dirname,
                "".join((COMMON_MODELS_PACKAGE_NAMEPART, self.lang)),
                config_entry_name,
            )
        )
        os.mkdir(this_model_dir)
        init_py_filename = os.sep.join((this_model_dir, "__init__.py"))
        with open(init_py_filename, "w") as init_py_file:
            self.writeln(init_py_file)
        feature_table_filename = os.sep.join(
            (this_model_dir, FEATURE_TABLE_FILENAME)
        )
        with open(feature_table_filename, "wb") as feature_table_file:
            pickle.dump(feature_table, feature_table_file)
        keras_filename = "".join(
            (this_model_dir, os.sep, KERAS_MODEL_FILENAME)
        )
        keras_ensemble.save(keras_filename)

    def train_models(self):
        for config_entry_name in self.relevant_config_entry_names:
            config_entry = self.config[config_entry_name]
            print("Processing", config_entry_name, "...")
            temp_log_filename = "".join(
                (
                    self.log_dir,
                    os.sep,
                    "temp",
                    os.sep,
                    config_entry_name,
                    ".log",
                )
            )
            with open(
                temp_log_filename, "w", encoding="utf-8"
            ) as temp_log_file:
                self.train_model(
                    config_entry_name, config_entry, temp_log_file
                )
        timestamp = datetime.now().isoformat(timespec="microseconds")
        sanitized_timestamp = "".join([ch for ch in timestamp if ch.isalnum()])
        zip_filename = "".join(
            (
                self.log_dir,
                os.sep,
                "training_log_",
                self.lang,
                "_",
                sanitized_timestamp,
                ".zip",
            )
        )
        shutil.make_archive(
            zip_filename, "zip", os.sep.join((self.log_dir, "temp"))
        )
        temp_dir = os.sep.join((self.log_dir, "temp"))
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir)
        zip_filename = "".join(
            (
                self.models_dirname,
                os.sep,
                "..",
                os.sep,
                COMMON_MODELS_PACKAGE_NAMEPART,
                self.lang,
            )
        )
        if os.path.isfile(zip_filename):
            os.remove(zip_filename)
        shutil.make_archive(zip_filename, "zip", self.models_dirname)
