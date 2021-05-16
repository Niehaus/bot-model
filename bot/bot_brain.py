"""
author: Bárbara Boechat
date: 29/04/2021

Este pacote contém diferentes personalidades que podem
ser atribuídas a um actions. E ferramentas para que uma nova
personalidade seja criada também.

Uma personalidade pode ser traduzida como funções de avaliação
de conteúdo que devem auxiliar o actions na sua tomada de decisão
durante uma execução.
"""


class Brain:
    def __init__(self, name):
        self.name = name

    def evaluate_timeline(self):
        ...

    def evaluate_interaction(self):
        ...
