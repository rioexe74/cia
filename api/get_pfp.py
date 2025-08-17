
import json
import logging
from twikit.guest import GuestClient

# Custom Response class for Vercel Python API
class Response(dict):
    def __init__(self, body, status=200, headers=None):
        super().__init__(
            statusCode=status,
            headers=headers or {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            body=body
        )

# Vercel Python API handler (async)
async def handler(request):
    try:
        # Get username from query params
        username = request.query.get('username')
        if not username:
            return Response(
                json.dumps({'error': 'Username parameter is missing'}),
                status=400,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            )

        try:
            client = GuestClient()
            await client.activate()
        except Exception as e:
            logging.error(f"GuestClient activation failed: {e}")
            return Response(
                json.dumps({'error': f'Could not activate Twitter guest client: {str(e)}'}),
                status=500,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            )

        try:
            user = await client.get_user_by_screen_name(username)
            pfp_url = (user.profile_image_url or '').replace('_normal', '')
            display_name = getattr(user, 'name', '') or ''
            screen_name = getattr(user, 'screen_name', '') or username
            result = {"pfp_url": pfp_url, "name": display_name, "handle": f"@{screen_name}"}
            return Response(
                json.dumps(result),
                status=200,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            )
        except Exception as e:
            logging.error(f"Twitter user fetch failed: {e}")
            return Response(
                json.dumps({'error': f"User '{username}' not found or profile is protected."}),
                status=404,
                headers={
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return Response(
            json.dumps({'error': f'Unexpected server error: {str(e)}'}),
            status=500,
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        )