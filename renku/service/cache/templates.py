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
"""Renku service templates cache management."""

from renku.service.cache.base import BaseCache

from renku.service.cache.models.template import Template
from renku.service.cache.serializers.template import TemplateSchema


class TemplateManagementCache(BaseCache):
    """Project management cache."""

    template_schema = TemplateSchema()

    @staticmethod
    # def get_templates(user, url, ref):
    def get_templates(url, ref):
        """Get <user?> cached template."""
        try:
            record = Template.get(Template.url == url, Template.ref == ref)
            # record = Project.get((Project.project_id == project_id) &
            #                      (Project.user_id == user.user_id))
        except ValueError as e:
            print(e)
            return

        return record
