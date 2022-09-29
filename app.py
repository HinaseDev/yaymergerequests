import os
import requests

from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
app_id = '<Your_App_Number_here>'
# Read the bot certificate
with open(
        os.path.normpath(os.path.expanduser('~/.certs/github/yaymergerequests.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)


@app.route("/", methods=['POST'])
def bot():
    # Get the event payload
    payload = request.json

    # Check if the event is a GitHub PR creation event
    if not all(k in payload.keys() for k in ['action', 'pull_request']) and \
            payload['action'] == 'closed' and payload['merged']:
        return "ok"

    owner = payload['repository']['owner']['login']
    repo_name = payload['repository']['name']

    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")

    issue = repo.get_issue(number=payload['pull_request']['number'])

    import random
    gifs = [
        "https://media1.giphy.com/media/3o7buiQeyYFamzRoR2/200.gif",
        "https://c.tenor.com/jIuUhw7sCaEAAAAC/younger-yay.gif",
        "https://media2.giphy.com/media/H61haLYYXzAINQXoyM/giphy.gif",
        "https://c.tenor.com/FUTQ597etoAAAAAC/yay.gif",
        "https://c.tenor.com/wJLU6k53L6MAAAAC/anime-yay.gif",
        "https://thumbs.gfycat.com/BrightAridDikkops-max-1mb.gif",
        "https://64.media.tumblr.com/48353c09e0d627565feeeb7f3843d1e4/tumblr_phwisbTrjg1u5vwmu_400.gif",
        "https://c.tenor.com/XNU2RcQ7350AAAAM/cool-amazing.gif",
        "https://c.tenor.com/s7Kiv91_TLAAAAAM/anime-girl-cheering.gif",
        "https://c.tenor.com/Fi5H8EfqtFAAAAAM/yay-yeah.gif"
    ]
    # Create a comment with the random meme
    issue.create_comment(f"![Congrats on verifying your PR!]({random.choice(gifs)})")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
