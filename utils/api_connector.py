import configparser
import requests


class API:
    def __init__(self):
        self.bearer_token = self.auth()
        self.headers = {
            "Authorization": "Bearer {}".format(self.bearer_token)
        }

    @staticmethod
    def auth():
        # temporary config getter will be replaced by gitsecrets
        config = configparser.RawConfigParser()
        config.sections()
        config.read('../config.cfg')

        return config['DEFAULT']['bearer_token']

    def get_endpoint(self, url, params):
        response = requests.request("GET", url, headers=self.headers, params=params)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    def get_user_id(self, username):
        get_user_id_url = f'https://api.twitter.com/2/users/by/username/{username}'
        user_lookup_info = self.get_endpoint(get_user_id_url, params={})

        return user_lookup_info['data']['id']

    def users_tweets_url(self, username, user_id=None):
        """
        URL utiliza api/v2 e não possui limite de requisição
        diária, é limitada apenas pelo volume de consumo que sua
        licença de desenvolvedor permite. Consulte suas permissões
        em https://developer.twitter.com/

        :return: Retorna URL do endpoint que devolve os tweets de um
                 usuário buscado pelo seu id ou username
        """
        if not user_id:
            user_id = self.get_user_id(username)
        return "https://api.twitter.com/2/users/{}/tweets".format(user_id)
