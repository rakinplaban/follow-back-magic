from github import Github
import os

# Load token from environment variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")
USERNAME = "your_github_username"

# Authenticate with GitHub API
g = Github(GITHUB_TOKEN)
user = g.get_user()

# Get current followers and following
current_followers = {follower.login for follower in user.get_followers()}
current_following = {following.login for following in user.get_following()}

# Follow back new followers
for follower in current_followers - current_following:
    print(f"Following {follower} back...")
    user.add_to_following(follower)

# Unfollow those who unfollowed
for following in current_following - current_followers:
    print(f"Unfollowing {following}...")
    user.remove_from_following(following)
