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
"""Renku service template serializers."""

from marshmallow import Schema, fields

from renku.service.serializers.rpc import JsonRPCResponse


class ManifestTemplatesRequest(Schema):
    """Request schema for listing manifest templates."""

    # url = fields.String(required=True)
    # ref = fields.String(missing='master')
    project_id = fields.String(required=True)


class ManifestTemplateSchema(Schema):
    """Manifest template schema"""

    description = fields.String(required=True)
    folder = fields.String(required=True)
    name = fields.String(required=True)
    variables = fields.Dict(missing={})


class ManifestTemplatesResponse(Schema):
    """Manifest templates response."""

    templates = fields.List(
        fields.Nested(ManifestTemplateSchema), required=True
    )


class ManifestTemplatesResponseRPC(JsonRPCResponse):
    """RPC schema for listing manifest templates."""

    result = fields.Nested(ManifestTemplatesResponse)
