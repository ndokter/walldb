from django.db import connection


class SeededRandomQuerySetMixin(object):

    def seeded_random(self, seed):
        """
        Allows random ordering using a seed making it deterministic. This can be
        useful for paginated random results for example where an external source
        controls the seed.

        The seed should be a floating point
        number ranging from 0.0 to 1.0.
        """
        assert isinstance(seed, float), \
            'seeded_random expects seed to be a floating point'

        if 0.0 < seed > 1.0:
            raise ValueError(
                'seeded_random expects a floating point from 0.0 to 1.0'
            )

        if connection.vendor == 'postgresql':
            # The Postgres setseed seems to be session bound, but i could not
            # confirm this. I did some simple testing myself with sleep and
            # different sessions did not seem to interfere with eachother.

            # The Postgres implementation uses a seperate query to set the
            # internal seed for Postgres' random number generator.
            cursor = connection.cursor()
            cursor.execute('SELECT setseed({});'.format(seed))
            cursor.close()

            return self.order_by('?')

        elif connection.vendor == 'mysql':
            # Mysql uses an integer as the seed
            seed = int(seed * 1000)

            # The Mysql implementation adds an extra part to the queryset.
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
