# Ensure PyMySQL acts as MySQLdb for broad OS / platform compatibility
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
