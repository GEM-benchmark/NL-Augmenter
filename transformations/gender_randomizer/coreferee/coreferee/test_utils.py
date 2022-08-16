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

from os import sep
from threading import Lock

import pkg_resources
import spacy
from spacy.tokens import Doc
from thinc.api import Config

from .errors import LanguageNotSupportedError


def debug_structures(doc: Doc):
    for token in doc:
        print(
            token.i,
            token.text,
            token.lemma_,
            token.pos_,
            token.tag_,
            token.dep_,
            token.ent_type_,
            token.head.i,
            list(token.children),
        )


language_to_nlps = {}
lock = Lock()


def get_nlps(language: str, *, add_coreferee: bool = True) -> list:
    """Returns a list of *nlp* objects to use when testing the functionality for *language*.
    The list contains the latest versions of the Spacy models named in the config file.
    Note that if this method is called with *add_coreferee=False*, this setting will apply
    to all future calls within the same process space. This means that *add_coreferee=False*
    is only appropriate during development of rules tests and before any smoke tests are
    required."""
    with lock:
        if language not in language_to_nlps:
            relative_config_filename = sep.join(
                ("lang", language, "config.cfg")
            )
            if not pkg_resources.resource_exists(
                "coreferee", relative_config_filename
            ):
                raise LanguageNotSupportedError(language)
            absolute_config_filename = pkg_resources.resource_filename(
                __name__, relative_config_filename
            )
            config = Config().from_disk(absolute_config_filename)
            model_set = set()
            for config_entry in config:
                model_set.add(
                    "_".join((language, config[config_entry]["model"]))
                )
            nlps = []
            for model in model_set:
                # At present we presume there will never be an entry in the config file that
                # specifies a model name that can no longer be loaded. This seems a reasonable
                # assumption, but if it no longer applies this code will need to be changed in the
                # future.
                nlp = spacy.load(model)
                if add_coreferee:
                    nlp.add_pipe("coreferee")
                nlps.append(nlp)
            nlps = sorted(
                nlps, key=lambda nlp: (nlp.meta["name"], nlp.meta["version"])
            )
            language_to_nlps[language] = nlps
        return language_to_nlps[language]
