from django.core.exceptions import ValidationError


def sessions_entered(convention):
    return convention.sessions.exists()


def validate_trimmed(value):
    if value.endswith(" ") or value.startswith(" "):
        raise ValidationError(
            'Value must not start or end with white space.',
            code='invalid',
        )


def round_scheduled(round):
    for performance in round.performances.all():
        if not performance.start_time:
            return False
    return True


def performances_finished(round):
    performances = round.performances.all()
    for performance in performances:
        if performance.status != performance.STATUS.finished:
            return False
    return True


def scores_validated(round):
    for performance in round.performances.all():
        for song in performance.songs.all():
            for score in song.scores.all():
                if score.status == score.STATUS.flagged:
                    return False
    return True


def song_entered(song):
    if song.title:
        return True
    else:
        return False


def score_entered(score):
    if score.points:
        return True
    else:
        return False


def songs_entered(performance):
    songs = performance.songs.all()
    for song in songs:
        if not song_entered(song):
            return False
    return True


def scores_entered(performance):
    songs = performance.songs.all()
    for song in songs:
        for score in song.scores.all():
            if not score_entered(score):
                return False
    return True
