# reddit_gdpr_delete
Delete all comments/posts from the GDPR request

# How reliable is this?
I don't know. This is still very early code. Please contribute to improve it!

# Why does this exist?
When accessing the reddit API only the most recent 1000 comments are returned. This script allows to delete all comments included in the GDPR request.

# Does this delete all my comments?
The script tries to delete all comments in the given csv file and then check if they were deleted. If they weren't it retries to delete it.
This script cannot delete any comments not in the GDPR request, if such comments would exist.

# Guide
***DO NOT SHARE your config.json file with anyone under any circumstances!***
1. Go to https://www.reddit.com/settings/data-request and request your data
2. Wait until you receive it (can take up to 30 days)
3. Run the python script once, this will create the config.json where you will add your credentials
4. Go to https://www.reddit.com/prefs/apps, click "create another app...", give it a random name and select "script", add a redirect uri (http://reddit.com worked for me), press "create app" 
5. Add the string below "personal use script" to the JSON file as the reddit_client_id
6. Add the string after "secret" to the JSON file as the reddit_client_secret
7. Add your Reddit username and password to the JSON file
8. Put the csv file from the GDPR request with post that you want to delete in the same folder as reddit_delete.py
9. Change file_path in reddit_delete.py to that file
10. Rerun the script


