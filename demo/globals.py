import os
import random
import string

import media_platform

unique_path = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))

demo_path = '/python-demo/' + unique_path
resources_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/resources')

project_id = 'wixmp-38be4d0b88020d170fae2a8d'
client = media_platform.Client(
    domain=project_id + '.appspot.com',
    app_id='3966649e6f1a4a9db374a88dc63a6132',
    shared_secret=''
)