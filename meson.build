project(
    'logic',
    'cpp',
    default_options: ['cpp_std=c++20', 'b_ndebug=if-release'],
    license: 'MIT',
    license_files: 'LICENSE',
    version: '0.1.0',
)

py3 = import('python').find_installation(pure: false, required: true)
if not py3.language_version().version_compare('>=3.13')
    add_project_arguments('-DPY_SSIZE_T_CLEAN', language: 'cpp')
endif

add_project_arguments('-DGLM_FORCE_CXX17', language: 'cpp')

deps = [
    dependency('pybind11', required: true),
    dependency('glm', required: true),
]
srcs = files('logic/drone.cpp', 'logic/module.cpp', 'logic/vec3.cpp')

py3.extension_module('logic', sources: srcs, dependencies: deps, install: true)
