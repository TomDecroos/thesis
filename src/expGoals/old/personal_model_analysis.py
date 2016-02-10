'''
Created on 9 Nov 2015

@author: Tom
'''




import warnings

from expGoals.old.cluster import get_kmeans_clusters
from expGoals.old.features import get_distance_to_goal
import matplotlib.pyplot as plt
import numpy as np


warnings.filterwarnings("ignore")

def plot_cluster_distance(k, shots, ax):
    p_min = min([get_distance_to_goal(shot) for shot in shots])
    p_max = max([get_distance_to_goal(shot) for shot in shots])
    p_interval = (p_max - p_min) / k
    intervals = [(p_min + i * p_interval, p_min + (i + 1) * p_interval) for i in range(0, k)]
    distances = []
    goals_p = []
    for (c_min, c_max) in intervals:
        d_shots = [shot for shot in shots if get_distance_to_goal(shot) >= c_min and get_distance_to_goal(shot) <= c_max]
        if len(d_shots) > 0:
            distances.append(sum([get_distance_to_goal(shot) for shot in d_shots]) / len(d_shots))
            goals_p.append(sum([shot.result for shot in d_shots]))
    ax.scatter(distances, goals_p)
    ax.set_xlabel("Distance to Goal")
    ax.set_ylabel("Nb of goals scored")


def plot_model_pred(shots, ax):
    x = ([get_distance_to_goal(s) for s in shots])
    c = (["r" if s.result else "b" for s in shots])
    # alpha =([1 if s.result else 0.1 for s in shots])
    pred = [shot.pred for shot in shots]
    # ds = np.linspace(min(x),max(x),100)
    # pred_shots = model.predict([Shot.dummy_shot(d) for d in ds])
    ax.scatter(x, pred, c=c, alpha=1)
    # ax.scatter(x,y)
    ax.set_xlim(left=0)
    ax.set_xlabel("Distance to Goal")
    ax.set_ylabel("Goals: actual and expected value")

 
def plot_cluster_binom(k, shots, ax):
    clusters = get_kmeans_clusters(k, shots)
    x = [c.min() for c in clusters]
    y = [c.binom_p() for c in clusters]
    w = [c.max() - c.min() for c in clusters]
    ax.bar(x, y, width=w, color='blue')
    ax.set_xlabel("Clusters by average expected goals")
    ax.set_ylabel("Odds that the cluster \n generated its actual goals")
    ax.set_title("Average binom value:" + str(np.mean(y)))

def plot_cluster_goals(k, shots, ax):
    clusters = get_kmeans_clusters(k, shots)
    x = [c.exp_goals_frac() for c in clusters]
    y = [c.goals_frac() for c in clusters]
    ax.scatter(x, y)
    ax.plot([min(x), max(x)], [min(x), max(x)])
    ax.set_xlabel("Clusters by average expected goals)")
    ax.set_ylabel("Percentage of goals scored in cluster")


def plot_my_shot_analysis(k, shots):
    print("Plotting results...")
    fig, ax = plt.subplots(2, 2)
    fig.set_size_inches(13, 10, forward=True)
    plot_cluster_distance(k, shots, ax[0, 0])
    plot_model_pred(shots, ax[1, 0])
    plot_cluster_goals(k, shots, ax[0, 1])
    plot_cluster_binom(k, shots, ax[1, 1])
    plt.tight_layout()

plt.show()
