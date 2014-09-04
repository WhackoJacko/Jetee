import re


def remove_special_characters(word):
    pattern = re.compile(u'[^\w]')
    word = pattern.sub(u'_', word)
    return word


def render_env_variables(env_variables):
    rendered_env_variables = u','.join([u'{}="{}"'.format(key, value) for key, value in env_variables.items()])
    if rendered_env_variables:
        rendered_env_variables = u'export %s; bash' % rendered_env_variables
    return rendered_env_variables