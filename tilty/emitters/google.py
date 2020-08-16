# -*- coding: utf-8 -*-
""" Google Sheets emitter """
import logging
from typing import Any, Dict

import httplib2
from googleapiclient import discovery
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client

LOGGER = logging.getLogger()


def __type__() -> str:
    return 'Google'


class Google:  # pylint: disable=too-few-public-methods
    """ Google wrapper class """

    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # <start config sample>
        # [google]
        # access_token = 11111111111111111111111111
        # client_id = 111111-1111.apps.googleusercontent.com
        # client_secret = 1111111111111111
        # refresh_token = 11111111111111111111111111
        # spreadsheet_id = 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms

        self.access_token: Any = config.get('access_token')
        self.credentials: client.OAuth2Credentials = client.OAuth2Credentials(
            access_token=self.access_token,
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            refresh_token=config['refresh_token'],
            token_expiry=None,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent=None,
            revoke_uri=GOOGLE_REVOKE_URI,
        )
        self.refresh_if_needed()
        self.spreadsheet_id: str = config['spreadsheet_id']

    def refresh_if_needed(self) -> None:
        """ OAuth Refresh helper

        Args:
        """
        if not self.access_token or self.credentials.access_token_expired:
            LOGGER.info('[google] refreshing access token')
            http = self.credentials.authorize(httplib2.Http())
            self.credentials.refresh(http)

    def emit(self, tilt_data: dict) -> None:
        """ Emitter

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """
        self.refresh_if_needed()
        service: discovery.Resource = discovery.build(
            'sheets',
            'v4',
            credentials=self.credentials
        )
        resource: Dict[str, Any] = {
          "majorDimension": "ROWS",
          "values": [[
              tilt_data['timestamp'],
              'TODO',
              tilt_data['gravity'],
              tilt_data['temp'],
              tilt_data['color'].upper(),
              tilt_data['mac'],
            ]]
        }
        LOGGER.info('[google] inserting sheet data')
        service.spreadsheets().values().append(
          spreadsheetId=self.spreadsheet_id,
          range='Data!A:F',
          body=resource,
          valueInputOption="USER_ENTERED"
        ).execute()
