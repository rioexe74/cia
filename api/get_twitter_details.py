import asyncio
import json
from twikit.guest import GuestClient

def handler(request):
    # Get the username from query parameters
    username = request.args.get('username')
    if not username:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Username parameter is missing'})
        }

    async def get_pfp_url(username):
        try:
            client = GuestClient()
            await client.activate()
        except Exception as e:
            return None, f"Could not activate the guest client: {e}"
        try:
            user = await client.get_user_by_screen_name(username)
            pfp_url = (user.profile_image_url or '').replace('_normal', '')
            display_name = getattr(user, 'name', '') or ''
            screen_name = getattr(user, 'screen_name', '') or username
            return {"pfp_url": pfp_url, "name": display_name, "handle": f"@{screen_name}"}, None
        except Exception as e:
            return None, f"User '{username}' not found or profile is protected."

    result, error = asyncio.run(get_pfp_url(username))
    if error:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': error})
        }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(result)
    }
