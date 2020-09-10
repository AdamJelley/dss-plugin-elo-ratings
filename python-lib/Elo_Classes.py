import numpy as np


class Team(object):
    def __init__(self,teamId,rank=1000,scored=0):
        self.teamId = teamId
        self.rank = rank
        self.scored = scored
        self.new_rank = 0
        self.perf = 0
        
class Match(object):
    def __init__(self,matchId,level,homeTeam,awayTeam,homeTeam_goals,awayTeam_goals):
        self.matchId = matchId
        self.level = level
        self.homeTeam = homeTeam
        self.homeTeam.scored = homeTeam_goals
        self.awayTeam = awayTeam
        self.awayTeam.scored = awayTeam_goals
        self.proba = 0
        self.goalDiff = self.homeTeam.scored - self.awayTeam.scored
        self.home = 0
        self.away = 0
        self.probaHome = 0
        self.probaAway = 0
        
    def get_res_match(self):
        if self.homeTeam.scored > self.awayTeam.scored:
            self.homeTeam.perf = 1
            self.awayTeam.perf = 0
        elif self.homeTeam.scored == self.awayTeam.scored:
            self.homeTeam.perf = 0.5
            self.awayTeam.perf = 0.5
        else:
            self.homeTeam.perf = 0
            self.awayTeam.perf = 1 
        return 1
    
    def get_proba(self):
        self.probaHome = 1.0/(1+np.power(10,(self.awayTeam.rank - (self.homeTeam.rank))/400.0))  
        self.probaAway = 1.0 - self.probaHome
        return 1

    def G_index(self, avg_goalDiff):
        """ Weighting the result so that the defeat is not linear (8-0 or 6-0 is roughly the same : you got destroyed).
            Here use custom G function defined to be constant (1) in case of W/D/L, give diminishing returns with score difference
            and fit world football index as closely as possible.
        """
### Generalised G_index Factor
#        G = max(1, 1.6*np.log((np.abs(self.goalDiff)/avg_goalDiff)+1))
#        return G
    
### World Football specific  G_index factor ###

        if self.goalDiff==0 or np.abs(self.goalDiff) == 1:
            return 1
        elif np.abs(self.goalDiff) == 2:
            return 3/2.0
        else :
            return (11+np.abs(self.goalDiff))/8.0
        
    def get_point(self, avg_goalDiff):
        self.get_proba()
        
        self.pointHome = round(self.level * self.G_index(avg_goalDiff) *(self.homeTeam.perf - self.probaHome))
        self.pointAway = round(self.level * self.G_index(avg_goalDiff) *(self.awayTeam.perf - self.probaAway))
        return 1
    
    def update_team_rank(self, avg_goalDiff):
        self.get_res_match()
        self.get_point(avg_goalDiff)

        self.homeTeam.new_rank = self.homeTeam.rank + self.pointHome
        self.awayTeam.new_rank = self.awayTeam.rank + self.pointAway
        return 1
    
    def write_rankings(self):
        return {"matchId":self.matchId
               ,"homeTeam_goals":self.homeTeam.scored
               ,"awayTeam_goals":self.awayTeam.scored 
               ,"homeTeamId":self.homeTeam.teamId
               ,"awayTeamId":self.awayTeam.teamId
               ,"homeTeam_rank":self.homeTeam.rank
               ,"awayTeam_rank":self.awayTeam.rank
               ,"homeTeam_new_rank":self.homeTeam.new_rank
               ,"awayTeam_new_rank":self.awayTeam.new_rank
               ,"rank_change_home":self.pointHome
               ,"ELOprob_home":self.probaHome
               ,"ELOprob_away":self.probaAway
               ,"rank_change_away":self.pointAway}