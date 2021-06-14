def pytest_addoption(parser):
    parser.addoption("--t", action="store", default="light")


def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.t
    if "transformation_name" in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("transformation_name", [option_value])
