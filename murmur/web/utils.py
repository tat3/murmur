"""Utility functions."""

import json
import os
import threading
import datetime
from pytz import timezone

from queue import Queue
from requests_oauthlib import OAuth1Session


def merge_two_dicts(a, b):
    """Merge 2 dictionaries."""
    c = a.copy()
    c.update(b)
    return c


class TwitterClient:
    """Client to get data from Twitter."""

    def __init__(self, user_social=None):
        """Return client instance with tokens."""
        if user_social:
            self.AT = user_social.access_token['oauth_token']
            self.AS = user_social.access_token['oauth_token_secret']
        else:
            self.AT = os.environ['tw_at']
            self.AS = os.environ['tw_as']

        self.CK = os.environ['SOCIAL_AUTH_TWITTER_KEY']
        self.CS = os.environ['SOCIAL_AUTH_TWITTER_SECRET']

        self.session = OAuth1Session(self.CK, self.CS, self.AT, self.AS)

        self.urls = {
            'timeline':
                'https://api.twitter.com/1.1/statuses/home_timeline.json',
            'favlist': 'https://api.twitter.com/1.1/favorites/list.json',
            'user': 'https://api.twitter.com/1.1/users/show.json',
            'oembed': 'https://publish.twitter.com/oembed',
            'request_token': 'https://twitter.com/oauth/request_token',
            'access_token': 'https://twitter.com/oauth/access_token',
            'authorize': 'https://twitter.com/oauth/authorize',
            'account_verified':
                'https://api.twitter.com/1.1/account/verify_credentials.json',
            'tweet': 'https://api.twitter.com/1.1/statuses/show.json',
            'update': 'https://api.twitter.com/1.1/statuses/update.json'
        }

    def timeline(self):
        """Show self timeline."""
        res = self.session.get(self.urls['timeline'], params={})
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)

    def favlist(self, user_id, page=1, count=100):
        """Show someone's favorite list."""
        params = {
            'user_id': user_id,
            'count': count,
            'page': page,
        }
        res = self.session.get(self.urls['favlist'], params=params)
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)

    def user_from_screen_name(self, screen_name):
        """Show user's profile from screen_name."""
        params = {
            'screen_name': screen_name,
        }
        res = self.session.get(self.urls['user'], params=params)
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)

    def show_tweets(self, tweets):
        """Print given tweets."""
        for item in tweets:
            print(item['text'])

    def show_user(self, user):
        """Print given user's profile."""
        print('User ID: {}'.format(user['id_str']))
        print('Screen Name: {}'.format(user['screen_name']))
        print('Name: {}'.format(user['name']))

    def user_id_from_screen_name(self, screen_name):
        """Show user's id from screen_name."""
        try:
            user = self.user_from_screen_name(screen_name)
        except:
            raise Exception()
        return user['id_str']

    def html_embedded(self, tweet, q):
        """Add HTML data for Twitter widget on single tweet."""
        # Remove private account
        if tweet['user']['protected']:
            q.put({})
            return

        url = 'https://twitter.com/{screen_name}/status/{tweet_id}'.format(
            screen_name=tweet['user']['screen_name'], tweet_id=tweet['id_str'])
        params = {
            'url': url,
            'maxwidth': 300,
        }
        res = self.session.get(self.urls['oembed'], params=params)
        if res.status_code != 200:
            return ''
        q.put(json.loads(res.text)['html'])

    def add_htmls_embedded(self, tweets):
        """Add HTML data for Twitter widget on tweets."""
        threads = []
        queues = []
        for tweet in tweets:
            q = Queue()
            queues.append(q)
            th = threading.Thread(target=self.html_embedded, args=(tweet, q))
            th.start()
            threads.append(th)
        tweets_add = []
        for th, q, tweet in zip(threads, queues, tweets):
            th.join()
            if tweet['user']['protected']:
                continue
            tweet_add = merge_two_dicts(tweet, {'html_embedded': q.get()})
            tweets_add.append(tweet_add)

        return tweets_add

    def tweet_from_id(self, tweet_id):
        """Get tweet from id_str."""
        params = {
            'id': tweet_id,
        }
        res = self.session.get(self.urls['tweet'], params=params)
        if res.status_code != 200:
            raise Exception()
        return json.loads(res.text)

    def status_update(self, text):
        """Update status."""
        params = {"status": text}
        res = self.session.post(self.urls['update'], params=params)
        print(res)
        if res.status_code != 200:
            raise Exception()
        return True


def is_pc(request):
    """Whether user agent is pc or not."""
    from user_agents import parse
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)

    return not user_agent.is_mobile
    # return True


def ignore_exceptions(func, items):
    """Ignore exceptions with multi-thread."""
    def carry_out(func, item, q):
        """For each execusion."""
        try:
            q.put(func(item))
        except:
            q.put(None)

    threads = []
    queues = []
    for item in items:
        q = Queue()
        queues.append(q)
        th = threading.Thread(target=carry_out, args=(func, item, q))
        th.start()
        threads.append(th)
    result = []
    for th, q, item in zip(threads, queues, items):
        th.join()
        res = q.get()
        if res:
            result.append(res)
    print(len(items))
    return result


def parse_datetime(string):
    """Convert string to datetime object."""
    dt = datetime.datetime.strptime(string, '%a %b %d %H:%M:%S +0000 %Y')
    return dt.astimezone(timezone('Asia/Tokyo'))

if __name__ == '__main__':

    user_id = '1212759744'
    screen_name = 'kemomimi_oukoku'

    twitter = TwitterClient()

    # user = twitter.user_from_screen_name(screen_name)
    # user_id = user['id_str']
    # twitter.show_user(user)

    # tweets = twitter.timeline()
    tweets = twitter.favlist(user_id)
    # twitter.show_tweets(tweets)
    # tweets = twitter.add_htmls_embedded(tweets)
    print(tweets[0]["favorite_count"])

    # print(twitter.issue_request_url())
