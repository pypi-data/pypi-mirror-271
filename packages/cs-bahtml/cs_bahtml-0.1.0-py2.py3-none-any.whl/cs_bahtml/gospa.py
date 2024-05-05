from __future__ import division
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial.distance import euclidean
from scipy.optimize import linear_sum_assignment
#from awpy.analytics.nav import point_distance


def check_gospa_parameters(c, p, alpha):
    """ Check parameter bounds.

    If the parameter values are outside the allowable range specified in the
    definition of GOSPA, a ValueError is raised.
    """
    if alpha <= 0 or alpha > 2:
        raise ValueError("The value of alpha is outside the range (0, 2]")
    if c <= 0:
        raise ValueError("The cutoff distance c is outside the range (0, inf)")
    if p < 1:
        raise ValueError("The order p is outside the range [1, inf)")

def calculate_gospa(targets, tracks, c, p, alpha, map, euclidean_dist):
    """ GOSPA metric for multitarget tracking filters.
    
    The algorithm is of course symmetric and can be used for any pair of
    comparable sets, but the labels 'targets' and tracks' are used to denote
    them as this is one of the most common applications.

    Returns the total GOSPA, the target-to-track assignment and the decomposed
    contribution of assignment errors, missed targets and false tracks.

    Parameters
    ----------
    targets : iterable of elements
        Contains the elements of the first set.
    tracks : iterable of elements
        Contains the elements of the second set.
    c : float
        The maximum allowable localization error, and also determines the cost
        of a cardinality mismatch.
    p : float
        Order parameter. A high value of p penalizes outliers more.
    alpha : float, optional
        Defines the cost of a missing target or false track along with c. The
        default value is 2, which is the most suited value for tracking
        algorithms.
    assignment_cost_function : function, optional
        This is the metric for comparing tracks and targets, referred to as
        d(x,y) in the reference. If no parameter is given, euclidian distance
        between x and y is used.

    Returns
    -------
    gospa : float
        Total gospa.
    assignment : dictionary
        Contains the assignments on the form {target_idx : track_idx}.
    gospa_localization : float
        Localization error contribution.
    gospa_missed : float
        Number of missed target contribution.
    gospa_false : float
        Number of false tracks contribution.

    References
    ----------

    - A. S. Rahmathullah, A. F. Garcia-Fernandez and L. Svensson, Generalized
      optimal sub-pattern assignment metric, 20th International Conference on
      Information Fusion, 2017.
    - L. Svensson, Generalized optimal sub-pattern assignment metric (GOSPA),
      presentation, 2017. Available online: https://youtu.be/M79GTTytvCM
    """
    check_gospa_parameters(c, p, alpha)
    num_targets = len(targets)
    num_tracks = len(tracks)
    miss_cost = c**p/alpha
    if num_targets == 0: # All the tracks are false tracks
        gospa_false = miss_cost*num_tracks
        return gospa_false**(1/p), dict(), 0, 0, gospa_false
    elif num_tracks == 0: # All the targets are missed
        gospa_missed = miss_cost*num_targets
        return gospa_missed**(1/p), dict(), 0, gospa_missed, 0
    else: # There are elements in both sets. Compute cost matrix
        if euclidean_dist:
            cost_matrix = euclidean_distances(targets, tracks)**p
        else:
            cost_matrix = np.zeros((num_targets, num_tracks))
            for n_target in range(num_targets):
                for n_track in range(num_tracks):
                    # current_cost = point_distance(map,
                    #     targets[n_target], tracks[n_track],"geodesic")['distance']
                    # if current_cost == 0:
                    current_cost = euclidean(targets[n_target], tracks[n_track])

                    cost_matrix[n_target,n_track] = current_cost**p
        #cost_matrix = euclidean_distances(targets,tracks)**p
        cost_matrix = np.minimum(cost_matrix, miss_cost*alpha)
        target_assignment, track_assignment = linear_sum_assignment(cost_matrix)
        gospa_localization = 0
        target_to_track_assigments = dict()
        for target_idx, track_idx in zip(target_assignment, track_assignment):
            if cost_matrix[target_idx, track_idx] < alpha*miss_cost:
                gospa_localization += cost_matrix[target_idx, track_idx]
                target_to_track_assigments[target_idx] = track_idx
        num_assignments = len(target_to_track_assigments)
        num_missed = num_targets - num_assignments
        num_false = num_tracks - num_assignments
        gospa_missed = miss_cost*num_missed
        gospa_false = miss_cost*num_false
        gospa = (gospa_localization + gospa_missed + gospa_false)**(1/p) / max(num_targets,num_tracks)
        return (gospa,
                target_to_track_assigments,
                gospa_localization,
                gospa_missed,
                gospa_false)
    
def calculate_gospa_matrix(series, c, p, alpha, map, euclidean_dist = False):
    n = len(series)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i,n):
            if i==j:
                continue
            dist = calculate_gospa(series[i],series[j],c,p,alpha, map, euclidean_dist)[0]
            matrix[i,j] = dist
            matrix[j,i] = dist
    return matrix

def calculate_gospa_distance(frames, c, p, alpha, map, euclidean_dist):
    n = len(frames)
    dist=0
    for i in range(n):
        for j in range(i,n):
            if i==j:
                continue
            dist += calculate_gospa(frames[i],frames[j], c, p, alpha, map, euclidean_dist = euclidean_dist)[0]
    dist = dist/(n*(n-1)/2)
    
    return dist
