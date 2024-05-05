__version__ = '0.3'
__author__ = 'bailu'
__com__ = 'China telecom Shannxi'
__mail__ = 'yabailu@chinatelecom.cn'
__tel__ = '15399117834'


import pkg_resources

# 全局变量存储 JAR 文件路径
JAR_FILES = [pkg_resources.resource_filename('xcloudmanager', f'resources/{jar_name}') for jar_name in [
    'XCloudJDBC-2.10.6.7.jar', 'slf4j-api-1.7.5.jar', 'slf4j-log4j12-1.7.5.jar', 
    'slf4j-simple-1.7.5.jar', 'log4j-1.2.17.jar', 'libthrift-0.9.2.jar', 
    'XCloudJDBC_SP_Procedure_Parser-0.1.3.jar', 'lz4-1.3.0.jar'
]]