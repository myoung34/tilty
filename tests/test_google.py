# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import google


def test_google_type(
):
    assert google.__type__() == 'Google'


@mock.patch('tilty.emitters.google.httplib2')
@mock.patch('tilty.emitters.google.discovery')
@mock.patch('tilty.emitters.google.client')
@mock.patch(
    'tilty.emitters.google.GOOGLE_REVOKE_URI',
    return_value='http://revoke.com'
)
@mock.patch(
    'tilty.emitters.google.GOOGLE_TOKEN_URI',
    return_value='http://token.com'
)
def test_google(
    mock_token_uri,
    mock_revoke_uri,
    mock_oauth_client,
    mock_googleapi_client,
    mock_httplib,
):
    config = {
      "client_id": "11111111-111111111111111111111",
      "client_secret": "xxxxxxxxx-fffffffff-wwwww",
      "token_uri": "https://oauth2.googleapis.com/token",
      "spreadsheet_id": "xxxxxxxxxxxxxxxx-yyyyyyyyyyyyyyyy",
      "access_token": "yyyy.cccc-dddddddddd-eeeeee-ffffffffffffffff",
      "refresh_token": "yyyy.cccc-dddddddddd-eeeeee-ffffffffffffffff",
    }

    google.Google(config=config).emit(tilt_data={
        'color': 'black',
        'mac': '00:0a:95:9d:68:16',
        'gravity': 1000,
        'temp': 80,
        'timestamp': 155558888,
    })
    assert mock_oauth_client.mock_calls == [
        mock.call.OAuth2Credentials(
            access_token='yyyy.cccc-dddddddddd-eeeeee-ffffffffffffffff',
            client_id='11111111-111111111111111111111',
            client_secret='xxxxxxxxx-fffffffff-wwwww',
            refresh_token='yyyy.cccc-dddddddddd-eeeeee-ffffffffffffffff',
            revoke_uri=mock.ANY,
            token_expiry=None,
            token_uri=mock.ANY,
            user_agent=None
        ),
        mock.call.OAuth2Credentials().access_token_expired.__bool__(),
        mock.call.OAuth2Credentials().authorize(mock.ANY),
        mock.call.OAuth2Credentials().refresh(mock.ANY),
        mock.call.OAuth2Credentials().access_token_expired.__bool__(),
        mock.call.OAuth2Credentials().authorize(mock.ANY),
        mock.call.OAuth2Credentials().refresh(mock.ANY),
    ]

    assert mock_googleapi_client.mock_calls == [
        mock.call.build('sheets', 'v4', credentials=mock.ANY),
        mock.call.build().spreadsheets(),
        mock.call.build().spreadsheets().values(),
        mock.call.build().spreadsheets().values().append(
            body={
                'majorDimension': 'ROWS',
                'values': [[
                    155558888,
                    'TODO',
                    1000,
                    80,
                    'BLACK',
                    '00:0a:95:9d:68:16'
                ]]
            },
            range='Data!A:F',
            spreadsheetId='xxxxxxxxxxxxxxxx-yyyyyyyyyyyyyyyy',
            valueInputOption='USER_ENTERED'
        ),
        mock.call.build().spreadsheets().values().append().execute(),
    ]
    assert mock_httplib.mock_calls == [mock.call.Http(), mock.call.Http()]
