# -*- coding: utf-8 -*-
#
# Copyright 2019-2020 - Swiss Data Science Center (SDSC)
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
"""Renku service templates view tests."""

import json
import os
import uuid

import pytest
from flaky import flaky


@pytest.mark.service
@pytest.mark.integration
@flaky(max_runs=10, min_passes=1)
def test_read_manifest_from_template(svc_client):
    """Check reading manifest template."""
    # ! MOVE THESE
    TEMPLATE_URL = 'https://github.com/SwissDataScienceCenter/' \
        'renku-project-template'
    IT_GIT_ACCESS_TOKEN = os.getenv(
        'IT_OAUTH_GIT_TOKEN', 'LkoLiyLqnhMCAa4or5qa'
    )

    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'Renku-User-Id': '{0}'.format(uuid.uuid4().hex),
        'Renku-User-FullName': 'Just Sam',
        'Renku-User-Email': 'contact@justsam.io',
        'Authorization': 'Bearer {0}'.format(IT_GIT_ACCESS_TOKEN),
    }

    # payload = {
    #     # 'git_url': REMOTE_URL,
    #     # REMOTE_URL = 'https://dev.renku.ch/gitlab/contact/integration-test'
    #     'url': TEMPLATE_URL
    # }
    params = {
        'url': TEMPLATE_URL
    }

    response = svc_client.get(
        # '/templates.read_manifest', data=json.dumps(payload), headers=headers
        '/templates.read_manifest', query_string=params, headers=headers
    )


    assert response
    assert 'error' not in response.json.keys()
    assert response.json['result']['input_url'] == TEMPLATE_URL

    # svc_client, headers, project_id, _ = svc_client_with_repo

    # params = {
    #     'project_id': project_id,
    # }

    # response = svc_client.get(
    #     '/datasets.list',
    #     query_string=params,
    #     headers=headers,
    # )

    # assert response
    # assert_rpc_response(response)

    # assert {'datasets'} == set(response.json['result'].keys())
    # assert 0 != len(response.json['result']['datasets'])
    # assert {'identifier', 'name', 'version',
    #         'created'} == set(response.json['result']['datasets'][0].keys())
