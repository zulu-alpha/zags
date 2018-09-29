"""Generate config files from environmental variables and launch Arma 3 server with them"""

import os
import sys
import logging
from subprocess import call
import jinja2


log = logging.getLogger()
log.setLevel(logging.INFO)

log.info(f'Arguments received: {sys.argv[1:]}')
call(sys.argv[1:])



#ENTRYPOINT ["./arma3server", "-config=./server.cfg"]
#CMD ["-port", "2302", "-filePatching"]