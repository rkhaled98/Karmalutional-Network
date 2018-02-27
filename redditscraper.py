import praw
from praw.models import MoreComments

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

reddit = praw.Reddit(client_id='wBnuJlXAeHDnKQ',
                     client_secret='BE_SL0MrlgAtKktUGGFYI_RXtjc', password='karmalutionalnet',
                     user_agent='karmalutionalNetwork', username='karmalutionalNetwork')

subreddit = reddit.subreddit('news')

new = subreddit.new(limit = 5)

for submission in new:
    if not submission.stickied:
        print('Title: {}, ups: {}, downs: {}, Have we visited?: {}'.format(submission.title,
                                                                           submission.ups,
                                                                           submission.downs,
                                                                           submission.visited))

        comments = {}
        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, MoreComments):
                continue
            comments[top_level_comment] = top_level_comment.score

        top_comment_id = keywithmaxval(comments)
        print(top_comment_id.body)
        print(top_comment_id.score)

f = open('')
