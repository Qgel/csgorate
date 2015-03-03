#!/usr/bin/python
from HltvScrape import Scraper
from Ranking import Ranking

def sse(ranking, games):
  sse = 0
  for game in games:
    pred = ranking.winChance(game[0], game[1])
    sse += (1 - pred) ** 2
  return sse

def guesses(ranking, games):
  r = [0, 0]
  for game in games:
    pred = ranking.winChance(game[0], game[1])
    if pred > 0.75: r[0] += 1
    if pred < 0.25: r[1] += 1
  return r

class Evaluator:
  def __init__(self):
    self.sc = Scraper()
    self.sc.getGames(0, 1500)

  def evaluate(self, train, mapName = 'all'):
    rk = Ranking('200', self.sc.getGames(200,train)[mapName])
    print "sse> {0}".format(sse(rk, self.sc.getGames(0, 200)[mapName]))
    g = guesses(rk, self.sc.getGames(0, 200)[mapName])
    print "guesses> correct: {0} wrong: {1}".format(g[0], g[1])


