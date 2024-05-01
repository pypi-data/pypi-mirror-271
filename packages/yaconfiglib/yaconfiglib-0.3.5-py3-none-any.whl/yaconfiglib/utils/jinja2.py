import typing as _ty

from jinja2 import Environment, Template

from . import log as _log

DEFAULT_ENV = Environment(extensions=["jinja2.ext.do"])


def load_template(
    source: str,
    name: str = None,
    filename: str = None,
    environment: Environment = None,
    globals: _ty.MutableMapping = None,
):
    environment = environment or DEFAULT_ENV
    code = environment.compile(source, name, filename)
    return Template.from_code(environment, code, environment.make_globals(globals))


def compile(
    code: str, environment: Environment = None, globals: _ty.MutableMapping = None
):
    return load_template(code, environment=environment, globals=globals).render


def eval(
    code: str,
    environment: Environment = None,
    globals: _ty.MutableMapping = None,
):
    template = load_template(
        "{% do _meta.__setitem__('result', " + code + ") %}",
        environment=environment,
        globals=globals,
    )

    def eval_(**kwargs):
        _meta = {}
        template.render(_meta=_meta, **kwargs)
        return _meta["result"]

    return eval_


def interpolate(data: object, globals: dict = None, logger: _log.Logger = None):
    globals = {} if globals is None else globals
    logger = logger or _log.getLogger(None)
    logger.debug(
        'interpolate "%s" of type %s ...'
        % (
            data,
            type(data),
        )
    )
    if isinstance(data, str):
        _template = data.removeprefix("{{").removesuffix("}}")
        if not "{{" in _template and _template != data:
            template = eval(_template)
        else:
            template = compile(data)

        _data = template(**globals)
        if not data == _data:
            logger.debug(
                'interpolated "%s" to "%s" (type: %s)'
                % (
                    data,
                    _data,
                    type(data),
                )
            )
        data = _data
    elif isinstance(data, _ty.Mapping):
        if not isinstance(data, _ty.MutableMapping):
            data = {**data}
        keys = list(data.keys())
        for key in keys:
            value = data.pop(key)
            key = interpolate(key, globals, logger)
            data[key] = interpolate(value, globals, logger)

    elif isinstance(data, _ty.Iterable):
        if not isinstance(data, _ty.MutableSequence):
            data = [*data]
        for idx, value in enumerate(data):
            data[idx] = interpolate(value, globals, logger)

    return data
