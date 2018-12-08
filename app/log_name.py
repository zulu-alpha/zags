"""Create log filename for use from bash. Requires CONFIG_HOSTNAME environmental variable"""
import os
import datetime


PATH_LOG = '/arma3/logs'

def make_log_filename():
    """Generates unique and readable filename for the log file"""
    hostname = os.getenv('CONFIG_HOSTNAME')
    timestamp = datetime.datetime.utcnow().isoformat()
    return f'{PATH_LOG}/[{hostname}]__{timestamp}.log'

if __name__ == '__main__':
    print(make_log_filename())
