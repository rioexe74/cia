import json
from twikit.guest import GuestClient

 # Vercel Python serverless function entry point
async def default(request):
    # Get the username from query string
    username = request.args.get('username') if hasattr(request, 'args') else None

    if not username:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Username parameter is missing'})
        }

    try:
        client = GuestClient()
        await client.activate()
        user = await client.get_user_by_screen_name(username)
        pfp_url = (user.profile_image_url or '').replace('_normal', '')
        display_name = getattr(user, 'name', '') or ''
        screen_name = getattr(user, 'screen_name', '') or username
        result = {"pfp_url": pfp_url, "name": display_name, "handle": f"@{screen_name}"}
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }