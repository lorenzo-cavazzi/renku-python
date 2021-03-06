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
"""Renku service jobs management."""
from renku.service.cache.base import BaseCache
from renku.service.cache.models.job import Job
from renku.service.cache.serializers.job import JobSchema


class JobManagementCache(BaseCache):
    """Job management cache."""

    job_schema = JobSchema()

    def make_job(self, user, job_data):
        """Cache job state under user hash set."""
        job_data.update({'user_id': user.user_id})

        job_obj = self.job_schema.load(job_data)
        job_obj.save()

        return job_obj

    @staticmethod
    def get_job(user, job_id):
        """Get user job."""
        try:
            job_obj = Job.get((Job.job_id == job_id) &
                              (Job.user_id == user.user_id))
        except ValueError:
            return

        return job_obj

    @staticmethod
    def get_jobs(user):
        """Get all user jobs."""
        return Job.query((Job.user_id == user.user_id))

    @staticmethod
    def invalidate_job(user, job_id):
        """Remove users job record."""
        job_obj = JobManagementCache.get_job(user, job_id)

        if job_obj:
            job_obj.delete()

        return job_obj
