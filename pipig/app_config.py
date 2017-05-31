from config import BaseConfiguration, TestConfiguration, DebugConfiguration, TestDatabaseConfiguration


config_class = TestDatabaseConfiguration()

config_dir = 'config'
config_name = '.'.join([config_dir, config_class.NAME])

