import tweepy
import os
import sys
import json
import time

FOLLOWING_DIR = 'followers_data'
USER_INFO_DIR = 'twitter-users'
SUSPENDED_FILE = 'suspended-users'
MAX_FRIENDS = 500

if not os.path.exists(FOLLOWING_DIR):
    os.mkdir(FOLLOWING_DIR)

if not os.path.exists(USER_INFO_DIR):
    os.mkdir(USER_INFO_DIR)

enc = lambda x: x.encode('ascii', errors='ignore')

CONSUMER_KEY='uEbv4WTyoQO3Bvt77hTzUDOli'
CONSUMER_SECRET='uAh7qknF62Na3CUtdafwzqfCGyESJWFxzIkLRPnG7h2bszisO7'
ACCESS_TOKEN='2809772576-7GtBXQvM8UpbAc2RbqqpRw4Muoi8m8jV3Cv0NGY'
ACCESS_TOKEN_SECRET='JCaEvCM9q8FdqngP5IdUYu4119UV6l5RoXdOf1AA4bi5w'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

suspended_users = []

api = tweepy.API(auth)

def get_follower_ids(center, visited_list=[]):

    if center in visited_list:
        print 'already visited'
        return visited_list

    if center in suspended_users:
        print 'user suspended'
        return visited_list

    visited_list.append(center)

    #try:
    if True: 
        userfname = os.path.join(USER_INFO_DIR, str(center) + '.json')
        if not os.path.exists(userfname):
            print 'Getting user details for user id %s' % str(center)
            while True:
                try:
                    user = api.get_user(center)
                    d = {'name': user.name,
                        'screen_name': user.screen_name,
                        'id': user.id,
                        'friends_count': user.friends_count,
                        'followers_count': user.followers_count,
                        'followers_ids': user.followers_ids()}

                    with open(userfname, 'w') as outf:
                        outf.write(json.dumps(d, indent=1))

                    user = d
                    break
                except tweepy.TweepError, error:
                    print type(error)

                    if str(error) == 'Not authorized.':
                        print 'Can''t access user data - not authorized.'
                        return visited_list

                    

                    errorObj = error[0][0]

                    print errorObj

                    if errorObj['message'] == 'User has been suspended.':
                        print 'User suspended.'
                        suspended_users.append(center)
                        with open(SUSPENDED_FILE, 'w') as outf:
                            outf.write(json.dumps(suspended_users))
                        return visited_list


                    if errorObj['message'] == 'Rate limit exceeded':
                        print 'Rate limited. Sleeping for 15 minutes.'
                        time.sleep(15 * 60 + 15)
                        continue

                    return visited_list
        else:
            user = json.loads(file(userfname).read())

        screen_name = enc(user['screen_name'])
        fname = os.path.join(FOLLOWING_DIR, screen_name + '.csv')
        friendids = []
        ids = []
        j = 1
        if not os.path.exists(fname):
            print 'No cached data for screen name "%s"' % screen_name
            with open(fname, 'w') as outf:
                params = (enc(user['name']), screen_name)
                print 'Retrieving friends for user "%s" (%s)' % params
                try:
                    if (len(friendids) == 0):
                        for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name).pages():
                            friendids.extend(page)
                    print "Retrieved %d friends" % len(friendids)
                    for i in range(j, len(friendids) + 1):
                        j = i
                        ids.append(friendids[i - 1])
                        if (i % 100 == 0):
                            items = api.lookup_users(user_ids=ids)
                            for item in items:
                                params = (item.id, enc(item.screen_name), enc(item.name))
                                outf.write('%s\t%s\t%s\n' % params)
                            ids = []
                    if (len(ids) > 0):
                        items = api.lookup_users(user_ids=ids)
                        for item in items:
                            params = (item.id, enc(item.screen_name), enc(item.name))
                            outf.write('%s\t%s\t%s\n' % params)



                except tweepy.TweepError as e:
                    print e
                    # hit rate limit, sleep for 15 minutes
                    print 'Rate limited. Sleeping for 15 minutes.'
                    time.sleep(15 * 60 + 15)

        else:
            friendids = [int(line.strip().split('\t')[0]) for line in file(fname)]

        print 'Found %d friends for %s' % (len(friendids), screen_name)

    # except Exception, error:
    #     print 'Error retrieving followers for user id: ', center
    #     print error
    #     sys.exit(1)

    return visited_list

if __name__ == '__main__':
    data_file = open(sys.argv[1])
    users = json.loads(data_file.readline())
    if os.path.exists(SUSPENDED_FILE):
        with open(SUSPENDED_FILE) as su_file:
            suspended_users = json.loads(su_file.readline())

    visited_list = []
    for i in range(0,50):
        visited_list = get_follower_ids(users[i]['user'], visited_list)
    # now we do lookups to get user info for each user