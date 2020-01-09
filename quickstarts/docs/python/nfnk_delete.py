#!/usr/bin/python3

import os
import nf_token as nft
import nf_network as nfn
nft.clear_log()
token=nft.get_token(os.environ.get('ENVIRONMENT'), os.environ.get('SMOKE_TEST_USER'), os.environ.get('SMOKE_TEST_PASS'))
nfn_url=nfn.find_network(os.environ.get('ENVIRONMENT'), os.environ.get('NFN_NAME'), token)
nfn.delete_network(nfn_url, token)
print(nfn_url)
