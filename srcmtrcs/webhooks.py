#!/usr/bin/env python3
# SrcMtrcs
# Copyright(C) 2018 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This is Source Operations Metrics..."""


import os
import logging
import hmac
import json

import daiquiri
import requests

from flask import request, Blueprint, jsonify, current_app
from IGitt.GitHub.GitHubRepository import GitHubRepository
from IGitt.GitHub.GitHubIssue import GitHubToken, GitHubIssue


daiquiri.setup(level=logging.DEBUG, outputs=('stdout', 'stderr'))
_LOGGER = daiquiri.getLogger(__name__)


webhooks = Blueprint('webhook', __name__, url_prefix='')


@webhooks.route('/github', methods=['POST'])
def handle_github_webhook():  # pragma: no cover
    """Entry point for github webhook."""
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == 'ping':
        return jsonify({'msg': 'pong'})

    signature = request.headers.get('X-Hub-Signature')
    sha, signature = signature.split('=')

    secret = str.encode(current_app.config.get('GITHUB_WEBHOOK_SECRET'))

    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()

    if hmac.compare_digest(hashhex, signature):
        payload = request.json

        _LOGGER.debug(f"Webhook received: {payload}")
    else:
        _LOGGER.error(
            f"Webhook secret mismatch: me: {hashhex} != them: {signature}")

    return jsonify({"message": "thanks, we are working on it!"}), 200
