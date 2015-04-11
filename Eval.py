#!/usr/bin/python
from HltvScrape import Scraper
from CsgoLoungeScrape import CsgoLoungeScraper
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

class MockBet:

  MINCONF = 5.0

  def __init__(self):
    self.money = 0.0
    self.sc = Scraper()
    self.sc.getGames(0, 1000)
    self.csgolounge = CsgoLoungeScraper()
    self.unknownTeams = set([])

  def bet(self, game, rk, favor):
    winner = game['winner'][0]
    loser = game['loser'][0]

    pred = rk.winChance(winner, loser) * 100
    winnerOdds = game['winner'][1]
    loserOdds = game['loser'][1]

    print "\nBet for {w}* vs {l}:".format(w=winner, l=loser)
    print "\tOdds: {wo}% : {lo}%".format(wo=winnerOdds, lo=loserOdds)
    print "\tPrediction: {pw}% : {pl}%".format(pw=pred, pl=100-pred)
    print "\tConfidence: {cw} : {cl}".format(cw=rk.confidence(winner), cl=rk.confidence(loser))

    unknowns = filter( lambda x : not rk.isKnown(x), [winner, loser])
    if(len(unknowns) > 0):
      print "\tNO BET: unknown team(s) {unkn}".format(unkn=(" and ".join(unknowns)))
      self.unknownTeams.update(unknowns)
      return False

    if(rk.confidence(winner) > self.MINCONF or rk.confidence(loser) > self.MINCONF):
      print "\tNO BET: confidence to low (> {mc})".format(mc=self.MINCONF)
      return False

    moneyBefore = self.money
    if (pred - winnerOdds) >= favor:
        amount = (pred - winnerOdds - favor) / 10.0 + 1
        winAmount = (loserOdds / float(winnerOdds)) * amount
        self.betTotal += amount
        self.money +=  winAmount
        print "\tSUCCESS: {before} + {win} -> {total}".format(win=winAmount, total=self.money, before=moneyBefore)
        return True
    if ((100 - pred) - loserOdds) >= favor:
        loss = ((100 - pred) - loserOdds - favor) / 10.0 + 1 
        self.betTotal += loss
        self.money -= loss
        print "\tFAIL: {before} - {l} -> {total}".format(total=self.money, l=loss, before=moneyBefore)
        return True

    print "\tNO BET: odds not favourable"
    return False

  def evaluate(self, betDays, rkDays=60, favor = 10):
    self.money = 0.0
    self.betTotal = 0.0
    rk = Ranking('bet', self.sc.getGamesForDays(rkDays, betDays)['all'])

    betGames = self.csgolounge.getGames(betDays)

    betCount = 0
    for game in betGames:
      betCount += self.bet(game, rk, favor)

    return (betCount, self.betTotal, self.money, self.money/self.betTotal)
