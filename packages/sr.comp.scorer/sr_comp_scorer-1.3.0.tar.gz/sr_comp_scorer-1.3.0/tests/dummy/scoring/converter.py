from sr.comp.scorer import Converter as BaseConverter


class Converter(BaseConverter):
    def form_team_to_score(self, form, zone_id):
        def owns_slot(slot_number):
            owner = int(form.get('slot_bottoms_{}'.format(slot_number), -1))
            return owner == zone_id

        return {
            **super().form_team_to_score(form, zone_id),
            'robot_moved':
                form.get('robot_moved_{}'.format(zone_id), None) is not None,
            'upright_tokens': int(form['upright_tokens_{}'.format(zone_id)]),
            'zone_tokens': {
                i: int(form['zone_tokens_{}_{}'.format(i, zone_id)])
                for i in range(4)
            },
            'slot_bottoms': {
                x: 1 if owns_slot(x) else 0
                for x in range(8)
            },
        }

    def form_to_score(self, match, form):
        score = super().form_to_score(match, form)
        # This score format doesn't record any arena data, only team data
        del score['arena_zones']
        return score

    def score_to_form(self, score):
        form = super().score_to_form(score)

        for info in score['teams'].values():
            zone_id = info['zone']

            form['robot_moved_{}'.format(zone_id)] = info.get('robot_moved', True)
            form['upright_tokens_{}'.format(zone_id)] = info.get('upright_tokens', True)

            for j in range(4):
                form['zone_tokens_{}_{}'.format(j, zone_id)] = info['zone_tokens'][j]

            for j in range(8):
                if info['slot_bottoms'][j]:
                    form['slot_bottoms_{}'.format(j)] = zone_id

        return form
