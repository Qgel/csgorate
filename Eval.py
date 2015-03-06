#!/usr/bin/python
from HltvScrape import Scraper
from Ranking import Ranking
from datetime import datetime, timedelta
import pylab as pl

def sse(ranking, games):
  sse = 0.0
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

  def evaluate(self, rk, testSet):
    print "num> {0}".format(len(testSet))
    print "sse> {0}".format(sse(rk, testSet))
    g = guesses(rk, testSet)
    print "guesses> correct: {0} wrong: {1}".format(g[0], g[1])
    return (sse(rk, testSet), g[0], g[1])

  def nEval(self, train, mapName = 'all'):
    rk = Ranking('200', self.sc.getGames(100,train)[mapName])
    testSet = self.sc.getGames(0, 100)[mapName]
    return self.evaluate(rk, testSet)

  def tEval(self, train, mapName = 'all', testDays = 60):
    rk = Ranking('we', self.sc.getGamesForDays(train, testDays)[mapName])
    testSet = self.sc.getGamesForDays(testDays)[mapName]
    return self.evaluate(rk, testSet)

  def sweep(self, start, end, mapName = 'all', testDays = 60, plot = False):
    r = []
    for train in range(start, end+1, 10):
      r.append(self.tEval(train, mapName, testDays)) 

    if plot:
      plots = pl.plot(range(start, end+1, 10), r)
      pl.show(plots[0])
    return r
