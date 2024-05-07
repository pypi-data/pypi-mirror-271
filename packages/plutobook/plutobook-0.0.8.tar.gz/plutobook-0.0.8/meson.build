project('plutobook-python', 'c', version: '0.0.1', license: 'MIT')

plutobook_dep = dependency('plutobook',
    required: true,
    fallback: ['plutobook', 'plutobook_dep']
)

py = import('python').find_installation(pure: false)

py.extension_module(
    'plutobook',
    'plutobook-module.c',
    dependencies: plutobook_dep,
    install: true
)
