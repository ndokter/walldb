from django.db import connection


class SeededRandomQuerySetMixin(object):

    def seeded_random(self, seed):
        """
        Allows random ordering using a seed. The seed should be a floating point
        number ranging from 0.0 to 1.0.

        Raises ValueError on wrong input
        """
        try:
            seed = float(seed)
        except (ValueError, TypeError):
            raise ValueError('seeded_random expects seed to be a floating point.')
        else:
            if 0.0 > seed > 1.0:
                raise ValueError(
                    'seeded_random expects floating point from 0.0 to 1.0'
                )

        if connection.vendor == 'postgresql':
            # This looks like it can cause a race condition when multiple
            # sessions start determining the seed which would mess up the
            # pagination. This doesn't seem to be the case after testing, but im
            # not sure why.
            cursor = connection.cursor()
            cursor.execute('SELECT setseed({});'.format(seed))
            cursor.close()

            return self.order_by('?')

        elif connection.vendor == 'mysql':
            # Mysql uses an integer as seed
            seed = int(seed * 1000)

            return self.extra(
                select={'random_ordering': "rand(%s)"},
                select_params=(seed,),
                order_by=['random_ordering']
            )

        raise NotImplementedError(
            "No seeded random implemented for database backend '{}'".format(
                connection.vendor
            )
        )
