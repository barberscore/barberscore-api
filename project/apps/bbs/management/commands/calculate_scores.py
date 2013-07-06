from __future__ import division

from django.core.management.base import BaseCommand

from apps.bbs.models import Performance

class Command(BaseCommand):

    def handle(self, **options):

        performances = Performance.objects.filter(is_complete=True)

        for p in performances:
            points = p.contest.panel_size * 100
            p.score_one = p.mus_one + p.prs_one + p.sng_one
            p.score_two = p.mus_two + p.prs_two + p.sng_two
            p.total_score = p.score_one + p.score_two

            p.avg_mus_one = p.mus_one / points
            p.avg_prs_one = p.prs_one / points
            p.avg_sng_one = p.sng_one / points
            p.avg_mus_two = p.mus_two / points
            p.avg_prs_two = p.prs_two / points
            p.avg_sng_two = p.sng_two / points

            p.avg_score_one = p.score_one / (points * 3)
            p.avg_score_two = p.score_two / (points * 3)

            p.avg_total_score = p.total_score / (points * 6)

            p.save()

        self.stdout.write("Successfully calculated scores")
