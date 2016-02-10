from scipy.stats.morestats import binom_test
from sklearn.cluster import KMeans
from statistics import mean,stdev

def get_kmeans_clusters(k, shots):
    cluster_indexes = KMeans(k,random_state=0).fit_predict([[shot.pred] for shot in shots])
    #print(len(cluster_indexes))
    #print([c for c in cluster_indexes if c != 1 and c != 0])
    clusters = []
    for i in range(0,k):
        clustershots = [shot for (shot,c_i) in zip(shots,cluster_indexes) if c_i == i]
        clusters.append(Cluster(clustershots))
    return clusters

def get_interval_clusters(k,shots):
    p_min = min([shot.pred for shot in shots])
    p_max = max([shot.pred for shot in shots])
    p_interval = (p_max - p_min)/k
    clusterintervals = [(p_min+i*p_interval,p_min+(i+1)*p_interval) for i in range(0,k)]
    clusters = []
    for (c_min,c_max) in clusterintervals:
        clustershots = [shot for shot in shots if shot.pred >= c_min and shot.pred <= c_max]
        clusters.append(Cluster(clustershots))
    return clusters

def test_shot_predictions(k,shots):
    ps = [(c.exp_goals(),c.binom_p(),c.goals()/c.n()) for c in get_kmeans_clusters(k,shots)]
    return ps

class Cluster():
    def __init__(self,shots):
        self.shots = shots
    def binom_p(self):
        return binom_test(self.goals(), self.n(), self.exp_goals_frac())
    def goals(self):
        return sum([shot.result for shot in self.shots])
    def n(self):
        return len(self.shots)
    def exp_goals(self):
        return sum([shot.pred for shot in self.shots])
    def goals_frac(self):
        return mean([shot.result for shot in self.shots])
    def exp_goals_frac(self):
        return mean([shot.pred for shot in self.shots])
    def exp_goals_std(self):
        return stdev([shot.pred for shot in self.shots])
    def min(self):
        return min([shot.pred for shot in self.shots])
    def max(self):
        return max([shot.pred for shot in self.shots])