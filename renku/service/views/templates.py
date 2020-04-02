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
"""Renku service templates view."""

from flask import Blueprint, request
from flask_apispec import marshal_with, use_kwargs
from renku.service.config import SERVICE_PREFIX

from renku.service.views import result_response
from renku.service.serializers.templates import ManifestTemplatesRequest, \
    ManifestTemplatesResponseRPC
from renku.service.views.decorators import header_doc, requires_cache, \
    requires_identity, accepts_json, handle_base_except, \
    handle_git_except, handle_renku_except, handle_validation_except
from renku.core.commands.init import read_template_manifest


TEMPLATES_BLUEPRINT_TAG = "templates"
templates_blueprint = Blueprint(
    TEMPLATES_BLUEPRINT_TAG, __name__, url_prefix=SERVICE_PREFIX
)


@use_kwargs(ManifestTemplatesRequest, locations=['query'])
@marshal_with(ManifestTemplatesResponseRPC)
@header_doc('List templates in repositpry.', tags=(TEMPLATES_BLUEPRINT_TAG, ))
@templates_blueprint.route(
    "/templates.read_manifest",
    methods=["GET"],
    provide_automatic_options=False,
)
@handle_base_except
@handle_git_except
@handle_renku_except
@handle_validation_except
@requires_cache
@requires_identity
@accepts_json
def read_manifest_from_template(user, cache):
    """Read the manifest file from a template to extract the list of available
    templates."""
    ctx = ManifestTemplatesRequest().load(request.args)
    user = cache.ensure_user(user)

    # read project and manifest
    project = cache.get_project(user, ctx['project_id'])
    manifest = read_template_manifest(project.abs_path)
    # INFO: specific error handling
    # #try: [...] except errors.InvalidTemplateError as e: [...]
    # # with chdir(project.abs_path): [...]

    return result_response(
        ManifestTemplatesResponseRPC(), {'templates': manifest}
    )
