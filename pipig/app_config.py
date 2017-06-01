from config import BaseConfiguration, TestConfiguration, DebugConfiguration, TestDatabaseConfiguration


config_class = BaseConfiguration()

config_dir = 'config'
config_name = '.'.join([config_dir, config_class.NAME])

