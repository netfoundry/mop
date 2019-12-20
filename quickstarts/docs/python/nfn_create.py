#!/usr/bin/python3

import os
import nf_token as nft
import nf_network as nfn
nft.clear_log()
token=nft.get_token(os.environ.get('ENVIRONMENT'))
nfn_url=nfn.create_network(os.environ.get('ENVIRONMENT'), os.environ.get('NFN_NAME'), token)
print(nfn_url)
