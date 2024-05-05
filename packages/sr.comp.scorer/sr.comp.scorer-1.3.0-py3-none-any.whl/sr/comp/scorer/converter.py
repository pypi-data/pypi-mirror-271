from __future__ import annotations

import copy
import imp
import sys
from pathlib import Path
from typing import cast, Type

from sr.comp.match_period import Match


class Converter:
    """
    Base class for converting between representations of a match's score.
    """

    def form_team_to_score(self, form, zone_id):
        """
        Prepare the part of the score dict for the given zone from the form data.
        """
        return {
            'zone': zone_id,
            'disqualified':
                form.get(f'disqualified_{zone_id}', None) is not None,
            'present':
                form.get(f'present_{zone_id}', None) is not None,
        }

    def form_to_score(self, match, form):
        """
        Prepare a score dict for the given match and form dict.

        This method is used to convert the submitted information for storage as
        YAML in the compstate.
        """
        zone_ids = range(len(match.teams))

        teams = {}
        for zone_id in zone_ids:
            tla = form.get(f'tla_{zone_id}', None)
            if tla:
                teams[tla] = self.form_team_to_score(form, zone_id)

        zones = list(zone_ids) + ['other']
        arena = {}
        for zone in zones:
            arena[zone] = {'tokens': form.get(f'tokens_{zone}', '')}

        return {
            'arena_id': match.arena,
            'match_number': match.num,
            'teams': teams,
            'arena_zones': arena,
        }

    def score_to_form(self, score):
        """
        Prepare a form dict for the given score dict.

        This method is used when there is an existing score for a match.
        """
        form = {}

        for tla, info in score['teams'].items():
            zone_id = info['zone']
            form[f'tla_{zone_id}'] = tla
            form[f'disqualified_{zone_id}'] = info.get('disqualified', False)
            form[f'present_{zone_id}'] = info.get('present', True)

        for zone, info in score.get('arena_zones', {}).items():
            form[f'tokens_{zone}'] = info['tokens'].upper()

        return form

    def match_to_form(self, match: Match) -> dict[str, str | bool]:
        """
        Prepare a fresh form dict for the given match.

        This method is used when there is no existing score for a match.
        """

        form: dict[str, str | bool] = {}

        for zone_id, tla in enumerate(match.teams):
            if tla:
                form[f'tla_{zone_id}'] = tla
                form[f'disqualified_{zone_id}'] = False
                form[f'present_{zone_id}'] = False

            form[f'tokens_{zone_id}'] = ''

        form['tokens'] = ''

        return form


def load_converter(compstate_path: Path) -> type[Converter]:
    """
    Load the score converter module from Compstate repo.

    :param Path compstate_path: The path to the compstate repo.
    """

    # Deep path hacks
    score_directory = compstate_path / 'scoring'
    converter_source = score_directory / 'converter.py'

    saved_path = copy.copy(sys.path)
    sys.path.append(str(score_directory))

    imported_library = imp.load_source('converter.py', str(converter_source))

    sys.path = saved_path

    converter = imported_library.Converter
    return cast(Type[Converter], converter)
