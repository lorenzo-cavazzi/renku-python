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
from renku.service.utils import make_project_path
from renku.service.serializers.templates import ManifestTemplatesRequest, \
    ManifestTemplatesResponseRPC
from renku.service.views.decorators import header_doc, requires_cache, \
    requires_identity, accepts_json, handle_base_except, \
    handle_git_except, handle_renku_except, handle_validation_except

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

    return result_response(
        ManifestTemplatesResponseRPC(), {
            'input_url': ctx['url'],
            'another': 'test'
        }
    )
    # a = 2
    # pass

    # ctx = ProjectCloneContext().load(
    #     (lambda a, b: a.update(b) or a)(request.json, user),
    #     unknown=EXCLUDE,
    # )
    # local_path = make_project_path(user, ctx)
    # user = cache.ensure_user(user)

    # if local_path.exists():
    #     shutil.rmtree(str(local_path))

    #     for project in cache.get_projects(user):
    #         if project.git_url == ctx['git_url']:
    #             project.delete()

    # local_path.mkdir(parents=True, exist_ok=True)
    # renku_clone(
    #     ctx['url_with_auth'],
    #     local_path,
    #     depth=ctx['depth'],
    #     raise_git_except=True,
    #     config={
    #         'user.name': ctx['fullname'],
    #         'user.email': ctx['email'],
    #     }
    # )

    # project = cache.make_project(user, ctx)

    # return result_response(ProjectCloneResponseRPC(), project)
