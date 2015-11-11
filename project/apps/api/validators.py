from django.core.exceptions import ValidationError


q80 = [0.886,0.679,0.557,0.482,0.434,0.399,0.370,0.349,0.332,0.318,0.305,0.294,0.285,0.277,0.269,0.263,0.258,0.252,0.247,0.242,0.238,0.234,0.230,0.227,0.224,0.220,0.218,0.215]

q90 = [
    0.941, 0.765, 0.642, 0.56, 0.507, 0.468, 0.437, 0.412, 0.392, 0.376, 0.361, 0.349, 0.338, 0.329, 0.32, 0.313, 0.306, 0.3, 0.295, 0.29, 0.285, 0.281, 0.277, 0.273, 0.269, 0.266, 0.263, 0.26
]

q95 = [
    0.97, 0.829, 0.71, 0.625, 0.568, 0.526, 0.493, 0.466, 0.444, 0.426, 0.41, 0.396, 0.384, 0.374, 0.365, 0.356, 0.349, 0.342, 0.337, 0.331, 0.326, 0.321, 0.317, 0.312, 0.308, 0.305, 0.301, 0.29
]

q99 = [
    0.994, 0.926, 0.821, 0.74, 0.68, 0.634, 0.598, 0.568, 0.542, 0.522, 0.503, 0.488, 0.475, 0.463, 0.452, 0.442, 0.433, 0.425, 0.418, 0.411, 0.404, 0.399, 0.393, 0.388, 0.384, 0.38, 0.376, 0.372
]

Q80 = {n:q for n,q in zip(range(3,len(q80)+1), q80)}
Q90 = {n:q for n,q in zip(range(3,len(q90)+1), q90)}
Q95 = {n:q for n,q in zip(range(3,len(q95)+1), q95)}
Q99 = {n:q for n,q in zip(range(3,len(q99)+1), q99)}


def dixon(performance, left=True, right=True, q_dict=Q90):
    """
    Keyword arguments:
        data = A ordered or unordered list of data points (int or float).
        left = Q-test of minimum value in the ordered list if True.
        right = Q-test of maximum value in the ordered list if True.
        q_dict = A dictionary of Q-values for a given confidence level,
            where the dict. keys are sample sizes N, and the associated values
            are the corresponding critical Q values. E.g.,
            {3: 0.97, 4: 0.829, 5: 0.71, 6: 0.625, ...}

    Returns a list of 2 values for the outliers, or None.
    E.g.,
       for [1,1,1] -> [None, None]
       for [5,1,1] -> [None, 5]
       for [5,1,5] -> [1, None]

    """
    for song in performance.songs.all():
        scores = song.scores.all()
        assert(left or right), 'At least one of the variables, `left` or `right`, must be True.'
        assert(len(scores) >= 3), 'At least 3 data points are required'
        assert(len(scores) <= max(q_dict.keys())), 'Sample size too large'
        data = [round(score.points * .01, 2) for score in scores]
        sdata = sorted(data)
        Q_mindiff, Q_maxdiff = (0, 0), (0, 0)

        if left:
            Q_min = (sdata[1] - sdata[0])
            try:
                Q_min /= (sdata[-1] - sdata[0])
            except ZeroDivisionError:
                pass
            Q_mindiff = (Q_min - q_dict[len(data)], sdata[0])

        if right:
            Q_max = abs((sdata[-2] - sdata[-1]))
            try:
                Q_max /= abs((sdata[0] - sdata[-1]))
            except ZeroDivisionError:
                pass
            Q_maxdiff = (Q_max - q_dict[len(data)], sdata[-1])

        if not Q_mindiff[0] > 0 and not Q_maxdiff[0] > 0:
            outliers = [None, None]

        elif Q_mindiff[0] == Q_maxdiff[0]:
            outliers = [Q_mindiff[1], Q_maxdiff[1]]

        elif Q_mindiff[0] > Q_maxdiff[0]:
            outliers = [Q_mindiff[1], None]

        else:
            outliers = [None, Q_maxdiff[1]]
        #  Set default
        song.status = song.STATUS.passed
        for score in scores:
            score.status = score.STATUS.passed
            if round(score.points * .01, 2) in outliers:
                score.status = score.STATUS.flagged
                score.song.status = score.song.STATUS.flagged
            score.save()
        song.save()
    return "Performance Tested"


def validate_trimmed(value):
    if value.endswith(" ") or value.startswith(" "):
        raise ValidationError(
            'Value must not start or end with white space.',
            code='invalid',
        )


def is_prepped(contest):
    return all([
        contest.organization,
        contest.level,
        contest.kind,
        contest.goal,
        contest.year,
        contest.panel,
        contest.rounds,
    ])


def is_impaneled(contest):
    for panelist in contest.panelists.contest():
        if not panelist.person:
            return False
    return True


def is_scheduled(contest):
    for session in contest.sessions.all():
        if not session.start:
            return False
    return True


def has_contestants(contest):
    return contest.contestants.exists()
