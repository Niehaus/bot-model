from api_connector import API
import json
import sys

if __name__ == '__main__':
    api = API()

    username = sys.argv[1]
    params = {"tweet.fields": "created_at",
              "exclude": "replies",
              "max_results": sys.argv[2]}

    endpoint_url = api.users_tweets_url(username)
    data = api.get_endpoint(endpoint_url, params=params)

    filename = f'timeline_{username}'
    with open(f'collected_files/timelines/{filename}.json', 'w+') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

