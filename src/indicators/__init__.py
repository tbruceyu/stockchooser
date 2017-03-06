import os

all_indicators = {}

my_dir = os.path.dirname(__file__)
for py in os.listdir(my_dir):
    if py == '__init__.py':
        continue

    if py.endswith('.py'):
        name = py[:-3]

        clsn = name.capitalize()
        while clsn.find('_') > 0:
            h = clsn.index('_')
            clsn = clsn[0:h] + clsn[h + 1:].capitalize()

        mod = __import__(__name__,
                         globals(),
                         locals(),
                         ['%s' % name])
        mod = getattr(mod, name)
        try:
            indicator = getattr(mod, clsn)()
        except AttributeError:
            raise SyntaxError('%s/%s does not define class %s' % (
                __name__, py, clsn))

        name = name.replace('_', '-')
        indicator.NAME = name
        all_indicators[name] = indicator
