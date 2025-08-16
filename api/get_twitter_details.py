import asyncio
import json
from twikit.guest import GuestClient

# Vercel serverless function entry point
async def handler(request):
    username = request.args.get('username')
    if not username:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Missing username parameter'})
        }
    try:
        client = GuestClient()
        await client.activate()
        user = await client.get_user_by_screen_name(username)
        pfp_url = (user.profile_image_url or '').replace('_normal', '')
        display_name = getattr(user, 'name', '') or ''
        screen_name = getattr(user, 'screen_name', '') or username
        result = {
            'pfp_url': pfp_url,
            'name': display_name,
            'handle': f"@{screen_name}"
        }
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

# For Vercel Python API routes, export the handler
# Vercel will call this function for each request
