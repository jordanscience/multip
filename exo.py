"""Crée par Jordan pour sa soeur Rachel le 26.12.2018 """

from random import randint
import operator
import os
import random
import conf
import pickle
from timeout_decorator import timeout
import time

SCORE_MIN = 80
MAX_TOTAL_TEMPS = 300
MAX_QUESTION_TEMPS = 30
MALUS_ERREUR = 5
BONUS_BONNE_REPONSE = 10


class Exo(object):
    def __init__(self, nom='Rachel'):
        self.nom = nom
        self.score = 0
        self.fail = 0
        self.scores_dict = None  # TODO: Finish it

    @timeout(MAX_TOTAL_TEMPS)
    def exercice(self):
        debut = time.time()
        while self.score < SCORE_MIN:
            try:
                self.question()
            except TimeoutError as e:
                print("Temps écoulé pour cette question, tu perds {} points !".format(MALUS_ERREUR))
                self.score -= MALUS_ERREUR
                print("Nouveau score: {}".format(self.score))
                continue
        fin = time.time()
        print("BRAVOOOOOOO {}! \n".format(self.nom))
        print("C'est fini! Tu t'es trompé {} fois".format(self.fail))
        print("\n")
        print("Tu as mis {} secondes".format(round(fin - debut)))

    @timeout(MAX_QUESTION_TEMPS)
    def question(self):
        my_list = [self.question_multiplication, self.question_addition]
        random.choice(my_list)()

    def question_multiplication(self):
        a = randint(2, 10)
        b = randint(2, 10)
        bonne_reponse = False
        while not bonne_reponse:
            reponse = input('{} * {}: \n'.format(a, b))
            if int(reponse) == a * b:
                print('BONNE REPONSE')
                self.score += BONUS_BONNE_REPONSE

                print('Nouveau score: {} \n'.format(self.score))
                bonne_reponse = True
            else:
                print('Non ! Essaie encore')
                self.score -= MALUS_ERREUR

                self.fail += 1

    def question_addition(self):
        a = randint(2, 1000)
        b = randint(1, min(a, 100))
        bonne_reponse = False
        ops = {"+": operator.add, "-": operator.sub}
        op = random.choice(list(ops.keys()))
        while not bonne_reponse:
            reponse = input('{} {} {}: \n'.format(a, op, b))
            if int(reponse) == ops.get(op)(a, b):
                print('BONNE REPONSE')
                self.score += BONUS_BONNE_REPONSE

                print('Nouveau score: {} \n'.format(self.score))
                bonne_reponse = True
            else:
                print('Non ! Essaie encore')
                self.score -= MALUS_ERREUR
                self.fail += 1

    @staticmethod
    def explication():
        print("***REGLES DU JEU****\n")
        print("SCORE A ATTEINDRE : {} points\n".format(SCORE_MIN))
        print("GAIN BONNE REPONSE : {} points\n".format(BONUS_BONNE_REPONSE))
        print("PERTE MAUVAISE REPONSE : {} points\n".format(MALUS_ERREUR))

        print("TEMPS LIMITE DU JEU: {} secondes \n".format(MAX_TOTAL_TEMPS))
        print("TEMPS LIMITE D'UNE QUESTION: {} secondes\n".format(MAX_QUESTION_TEMPS))

        print("Bonne chance !\n")
        print('Début dans 3 secondes...')
        time.sleep(3)
        print('GO!!! \n')

    def save_score(self):
        self.scores_dict[self.nom] = self.score

    def display_score(self):
        print(self.scores_dict)

    def dump_score(self):
        with open('conf.SCORES_PKL', 'wb') as handle:
            pickle.dump(self.scores_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_score(self):
        if self.scores_dict == {}:
            return {}
        if os.path.isfile(conf.SCORES_PKL):
            with open(conf.SCORES_PKL, 'rb') as handle:
                b = pickle.load(handle)
            return b
        return {}


if __name__ == '__main__':
    # nom = input("Entre ton nom cher Padawan !: \n")
    exo = Exo(nom='Rachel')
    exo.display_score()
    exo.explication()
    exo.exercice()
