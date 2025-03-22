from github import Github
import os
from dotenv import load_dotenv
import json


load_dotenv(verbose=True)

# Load token from environment variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")
USERNAME = "your_github_username"

# Authenticate with GitHub API
g = Github(GITHUB_TOKEN)
user = g.get_user()

# Load previous followers from a file (or create an empty list)
followers_file = "followers.json"
if os.path.exists(followers_file):
    with open(followers_file, "r") as f:
        previous_followers = json.load(f)
else:
    previous_followers = []


# Get current followers
current_followers = [follower.login for follower in user.get_followers()]

# Determine users who unfollowed
unfollowers = set(previous_followers) - set(current_followers)

# Unfollow only those who previously followed but now unfollowed
for unfollower in unfollowers:
    try:
        unfollow_user = g.get_user(unfollower)  # Convert to NamedUser
        user.remove_from_following(unfollow_user)
        print(f"Unfollowed {unfollower} (they unfollowed me first!)")
    except Exception as e:
        print(f"Error unfollowing {unfollower}: {e}")

# Save the new followers list
with open(followers_file, "w") as f:
    json.dump(current_followers, f)