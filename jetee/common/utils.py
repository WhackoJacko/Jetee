import re


def deep_merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                deep_merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception(u'Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def remove_special_characters(word):
    pattern = re.compile(u'[^\w]')
    word = pattern.sub(u'_', word)
    return word


def render_env_variables(env_variables):
    rendered_env_variables = u','.join([u'{}={}'.format(key, value) for key, value in env_variables.items()])
    return rendered_env_variables
