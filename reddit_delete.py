import praw
import csv
import time
import json
import os


file_path = 'comment_headers.csv'

if(not os.path.isfile('config.json')):
    print("config.json not found, created config.json. Add credentials to file then restart script.")
    with open('config.json', 'w') as f:
        f.write("""{
    "reddit_client_id": "",
    "reddit_client_secret": "",
    "reddit_username": "",
    "reddit_password": ""
}""")
    
    exit()

# Load config from json
with open('config.json', 'r') as f:
    config = json.load(f)

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=config['reddit_client_id'],
    client_secret=config['reddit_client_secret'],
    username=config['reddit_username'],
    password=config['reddit_password'],
    user_agent="Reddit Comment Deletion Script"
)




def check_deletion(comment_id):
    comment = reddit.comment(id=comment_id)
    if(comment.body == "[deleted]"):
        return True
    else:
        return False
    
def comment_status(comment_id):
    # Get the comment by its ID
    comment = reddit.comment(id=comment_id)
    try:
        content = comment.body
        author = comment.author
    except:
        return "Not found"

    if(author != config['reddit_username']):
        # print("Different user: ", author)
        return "Different user"
    elif(content == "[deleted]"):
        # print("Already deleted.")
        return "Deleted"
    else:
        return "Exists"


def delete_comment(comment_id):
    # Get the comment by its ID
    comment = reddit.comment(id=comment_id)
    try:
        content = comment.body
        author = comment.author
    except:
        return "Not found"

    if(author != config['reddit_username']):
        return "Different user"
    elif(content == "[deleted]"):
        return "Already deleted"
    else:
        comment.delete()
        check_deletion(comment_id)
        time.sleep(0.12)
        comment = reddit.comment(id=comment_id)
        if(check_deletion(comment_id)):
            # time.sleep(1)
            return "Deletion successful"
        else:
            # time.sleep(1)
            return "Deletion unsuccessful"


if __name__ == "__main__":

    if(reddit.user.me() == None):
        print("Authentication failed.")
        exit()
    
    
    # Read the CSV file
    comment_ids = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader) # Skip header

        for row in csv_reader:
            if row:  # Check if the row is not empty
                comment_ids.append(row[0])

    already_deleted = 0
    different_user = 0
    successful = 0
    unsuccessful = 0
    not_found = 0

    # Print the number of items to delete
    print(len(comment_ids))
    for i, comment_id in enumerate(comment_ids):

        if(i%10 == 0):
            print("Total:", i, ";", already_deleted, different_user, successful, unsuccessful, not_found)

        # Delete comment
        ret = delete_comment(comment_id)
        # Check return status
        if(ret == "Already deleted"):
            already_deleted += 1
        elif(ret == "Different user"):
            different_user += 1
        elif(ret == "Deletion successful"):
            successful += 1
        elif(ret == "Deletion unsuccessful"):
            print(".")
            time.sleep(0.4)
            ret2 = comment_status(comment_id)
            if(ret2 != "Exists"):
                successful += 1
                continue
            else:
                unsuccessful += 1

            print("Slow retry", comment_id)
            time.sleep(4)
            ret2 = delete_comment(comment_id)
            time.sleep(4)
            if(ret2 != "Exists"):
                print("retry worked")
                successful += 1
            else:
                print("Retry failed: ", comment_id)
                unsuccessful += 1

        elif(ret == "Not found"):
            not_found += 1
        