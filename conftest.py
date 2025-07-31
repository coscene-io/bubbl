# 必须在 conftest.py 用 parser.addini 注册 jwt_token
# pytest.ini 必须配置 jwt_token
# 之后 pytestconfig.getini("jwt_token") 才能正常读取，不会报 unknown configuration value
def pytest_addoption(parser):
    parser.addini("jwt_token", "JWT token for browser localStorage", default="")
    # parser.addini("jwt_token1", "JWT token for browser localStorage", default="")
    # parser.addini("jwt_token2", "JWT token for browser localStorage", default="")