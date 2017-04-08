# Django
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
    for appearance in round.appearances.all():
        if not appearance.start_time:
            return False
    return True


def appearances_finished(round):
    appearances = round.appearances.all()
    for appearance in appearances:
        if appearance.status != appearance.STATUS.finished:
            return False
    return True


def scores_validated(round):
    for appearance in round.appearances.all():
        for song in appearance.songs.all():
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


def songs_entered(appearance):
    songs = appearance.songs.all()
    for song in songs:
        if not song_entered(song):
            return False
    return True


def scores_entered(appearance):
    songs = appearance.songs.all()
    for song in songs:
        for score in song.scores.all():
            if not score_entered(score):
                return False
    return True
