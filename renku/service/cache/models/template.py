# -*- coding: utf-8 -*-
#
# Copyright 2020 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Renku service cache template related models."""

import hashlib
from walrus import Model, TextField, Array  # DateTimeField, IntegerField,

from renku.service.cache.base import BaseCache
from renku.service.config import CACHE_PROJECTS_TEMPLATES


class Template(Model):
    """Template object."""

    __database__ = BaseCache.model_db

    url = TextField()
    ref = TextField()
    # directories = submodel with path, name, description, number (ADD variables?)
    directories = Array()
    # last downloaded? or pull anyway every time just in case?

    @property
    def abs_path(self):
        """Full path of cached project."""
        combo_text = f'{self.url}@{self.ref}'
        folder_name = hashlib.sha1(combo_text.encode()).hexdigest()[:16]
        return CACHE_PROJECTS_TEMPLATES / folder_name
