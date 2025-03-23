from github import Github
import os
from dotenv import load_dotenv
import sqlite3


load_dotenv(verbose=True)

# Load token from environment variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")


# Authenticate with GitHub API
g = Github(GITHUB_TOKEN)
user = g.get_user()

# Initialize SQLite database
db_file = "followers.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


# Create table if it doesn’t exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        username TEXT PRIMARY KEY
    )
""")
conn.commit()

# Get current followers and following
followers = {f.login for f in user.get_followers()}
following = {f.login for f in user.get_following()}

# Fetch previously stored followers
cursor.execute("SELECT username FROM followers")
tracked_followers = {row[0] for row in cursor.fetchall()}

# New followers to track
new_followers = followers - tracked_followers
for follower in new_followers:
    cursor.execute("INSERT INTO followers (username) VALUES (?)", (follower,))
conn.commit()

# Users to unfollow (only those who were tracked and now unfollowed)
unfollowers = tracked_followers - followers
for unfollower in unfollowers:
    try:
        user.remove_from_following(g.get_user(unfollower))
        print(f"Unfollowed {unfollower} (they unfollowed me first!)")
        cursor.execute("DELETE FROM followers WHERE username = ?", (unfollower,))
    except Exception as e:
        print(f"Error unfollowing {unfollower}: {e}")
conn.commit()

# Follow back new followers
to_follow = followers - following
for username in to_follow:
    try:
        user.add_to_following(g.get_user(username))
        # print(f"Followed back: {username}")
    except Exception as e:
        print(f"Error following {username}: {e}")

# Close DB connection
conn.close()



