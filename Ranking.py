#!/usr/bin/python

from trueskill import Rating, rate_1vs1, setup, global_env
from math import sqrt

# Calculates the win probability of A vs B based on their
# respective ratings and our certainty of these.
def Pwin(rA=Rating(), rB=Rating()):
    deltaMu = rA.mu - rB.mu
    rsss = sqrt(rA.sigma**2 + rB.sigma**2)
    return global_env().cdf(deltaMu/rsss)

class Ranking:
  def __init__(self, name, games=[]):
    self.name = name
    self.gameCount = 0
    self.db = {}
    setup(draw_probability=0)
    for g in reversed(games):
      self.update(g)

  def _getRating(self, team):
    if team in self.db:
      return self.db[team]
    else:
      return Rating()

  # update ratings based on a game. 'game' is a tuple/list where
  # game[0] won agains game[1]
  def update(self, game):
    ratings = [self._getRating(t) for t in game]
    self.db[game[0]], self.db[game[1]] = rate_1vs1(ratings[0], ratings[1])
    self.gameCount += 1
    
  # Chance that t1 will win against t2 based on training data in db
  def winChance(self, t1, t2):
    return Pwin(self.db[t1], self.db[t2])

  # Ranking of the teams based on Rating and confidence
  def ranking(self):
    stats = [(t, self.db[t].mu, self.db[t].sigma, global_env().expose(self.db[t])) for t in self.db]
    return sorted(stats, key = lambda x: x[3], reverse=True)

