# Scripts de Coleta - Twitter API

Versão do Python >= 3.8

## Coleta de Timeline

O script recupera até n `(<max_tweets>)` tweets de um usuário atráves de seu username, ou seja, o `@` daquele usuário,
ou diretamente pelo seu Twitter Id, utilize o comando a seguir:

    python timeline_collect <username/user_id> <max_tweets>

O conteúdo pesquisado será encontrado no diretório `collected_files/timelines`
e o arquivo será nomeado como `timeline_<username/user_id>.json` e será da seguinte forma:
    
    {
    "data": [
        {
            "created_at": "2021-05-26T00:00:00.000Z",
            "id": "1397341714340204544",
            "text": "O @SenadorRogerio desmentiu a Capit\u00e3 Cloroquina ao vivo na #CPIdaCovid!
                    Mayra Pinheiro prestou depoimento hoje e sua fun\u00e7\u00e3o ficou clara: 
                    blindar e proteger Bolsonaro. \n\n\ud83d\udcc3 Saiba mais: 
                    https://t.co/Dr8jk7q2Hk https://t.co/LWMglNHEXD"
        },
        .
        .
        .
        {
            ...
        }
    }