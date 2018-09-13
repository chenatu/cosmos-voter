import logging
import os
from subprocess import Popen, PIPE

log = logging.getLogger(__name__)

GOBIN = os.environ['GOBIN']

if GOBIN is not None:
    GAIACLI_EXEC = GOBIN + '/gaiacli'
else:
    GAIACLI_EXEC = 'gaiacli'


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


# check if gaiacli exists
if which(GAIACLI_EXEC) is None:
    errMsg = "client of cosmos gaiacli does not exist, check whether gaiacli "\
        "is in GOBIN or PATH"
    log.error(errMsg)
    raise Exception(errMsg)


def vote(fromKey, option, proposal_id, passphrase, chain_id=None,
         isAsync=False, fee=None, gas=None, memo=None, node=None,
         sequence=None):
    # constuct voting command line
    cmd = [GAIACLI_EXEC, "gov", "vote", "--from=%s" % fromKey,
           "--option=%s" % option, "--proposal-id=%d" % proposal_id]

    if chain_id:
        cmd.append("--chain-id=%s" % chain_id)
    if isAsync:
        cmd.append("--async")
    if fee:
        cmd.append("--fee=%s" % fee)
    if gas:
        cmd.append("--gas=%s" % gas)
    if memo:
        cmd.append("--memo=%s" % memo)
    if node:
        cmd.append("--node=%s" % node)
    if sequence:
        cmd.append("--sequence=%s" % sequence)
    log.info("start to vote: %s" % cmd)
    __call(cmd, input=passphrase)


def query_proposals(chain_id=None, depositor=None, height=None, latest=None,
                    node=None, status=None, voter=None):
    cmd = [GAIACLI_EXEC, "gov", "query-proposals"]
    if chain_id:
        cmd.append("--chain-id=%s" % chain_id)
    if depositor:
        cmd.append("--depositor=%s" % depositor)
    if height:
        cmd.append("--height=%d" % height)
    if latest:
        cmd.append("--latest=%s" % latest)
    if node:
        cmd.append("--node=%s" % node)
    if voter:
        cmd.append("--voter=%s" % voter)
    log.info("start to query proposals: %s" % cmd)
    response = __call(cmd)
    # parse response
    if response:
        lines = response.splitlines()
        proposals = dict()
        for line in lines:
            loc = line.index('-')
            proposals[int(line[:(loc-1)])] = line[(loc+2):]
        return proposals
    else:
        return None


# query certain proposal, return result decoded with json lib
def query_proposal(proposal_id, chain_id=None, height=None, node=None):
    cmd = [GAIACLI_EXEC, "gov", "query-proposal",
           "--proposal-id=%d" % proposal_id]
    if chain_id:
        cmd.append("--chain-id=%s" % chain_id)
    if height:
        cmd.append("--height=%d" % height)
    if node:
        cmd.append("--node=%s" % node)
    log.info("start to query proposal: %s" % cmd)
    import json
    response = __call(cmd)
    return json.loads(response)


# TODO: validate the output
def query_vote(proposal_id, voter, chain_id=None, height=None, node=None):
    cmd = [GAIACLI_EXEC, "gov", "query-vote",
           "--proposal-id=%d" % proposal_id, "--voter=%s" % voter]
    if chain_id:
        cmd.append("--chain-id=%s" % chain_id)
    if height:
        cmd.append("--height=%d" % height)
    if node:
        cmd.append("--node=%s" % node)
    log.info("start to query proposal: %s" % cmd)
    return __call(cmd)


# TODO: validate the output
def query_votes(proposal_id, chain_id=None, height=None, node=None):
    cmd = [GAIACLI_EXEC, "gov", "query-votes",
           "--proposal-id=%d" % proposal_id]
    if chain_id:
        cmd.append("--chain-id=%s" % chain_id)
    if height:
        cmd.append("--height=%d" % height)
    if node:
        cmd.append("--node=%s" % node)
    log.info("start to query proposal: %s" % cmd)
    return __call(cmd)


def __call(cmd, input=None):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(input=input)
    rc = p.returncode
    if rc == 0:
        log.debug(stdout)
        return stdout
    else:
        raise Exception(stderr)
