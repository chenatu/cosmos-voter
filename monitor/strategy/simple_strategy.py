import strategy
import voter
from alert import ali_sms_alert
from alert.level import Level
from voter import voter
import logging

log = logging.getLogger(__name__)


# this strategy adopts aliyun sms service
class SimpleStrategy(strategy.Strategy):

    # config from yaml
    def __init__(self, config):
        self.config = config
        self.alert = ali_sms_alert.buildAliSmsAlertFromConfig(config)
        self.currentLevel = Level.EARTH
        self.des = config["strategy"]["simple_strategy"]["des"]
        self.cosmos_addr = config["strategy"]["simple_strategy"]["cosmos_addr"]
        self.passphrase = config["strategy"]["simple_strategy"]["passphrase"]
        self.from_key = config["strategy"]["simple_strategy"]["from_key"]
        if "node" in config["strategy"]["simple_strategy"].keys():
            self.node = config["strategy"]["simple_strategy"]["node"]
        else:
            self.node = None
        # query last proposal id
        proposals = voter.query_proposals(node=self.node)
        self.last_proposal_id = max(proposals.keys())
        self.retry_times = 0
        if 'max_retry_times' in config["strategy"]["simple_strategy"].keys():
            self.max_retry_times = config["strategy"]["simple_strategy"]
            ["max_retry_times"]
        else:
            self.max_retry_times = 10

    def getDes(self, level):
        return self.des

    def getCurrentLevel(self):
        return self.currentLevel

    def getAlert(self, level):
        return self.alert

    def getContent(self, level):
        return "{\"type\":\"vote\",\"msg\":\"new proposal comes\"}"

    def shouldTrigger(self, level):
        if self.getCurrentLevel().value > Level.EARTH.value:
            return True
        else:
            return False

    def before(self):
        # query the proposals first to check whther there is a proposal
        proposals = voter.query_proposals(node=self.node)
        new_last_proposal_id = max(proposals.keys())
        if new_last_proposal_id > self.last_proposal_id:
            # check whether the last proposals are voted
            for proposal_id in range(self.last_proposal_id,
                                     new_last_proposal_id):
                try:
                    voter.query_vote(proposal_id, self.cosmos_addr,
                                     node=self.node)
                except Exception:
                    log.warn("can not query certain vote, "
                             + "check whether it is in voting period")
                    try:
                        vote_result = voter.query_votes(proposal_id,
                                                        node=self.node)
                        if vote_result
                        .startswith('Proposal not in voting period'):
                            log.info(
                                'proposal %d is not in voting period'
                                % proposal_id)
                        else:
                            # there is a pending vote
                            self.currentLevel = Level.SUN
                    except Exception, e:
                        if str(e).endswith("does not exist"):
                            log.info("%d does not exist" % proposal_id)
                        else:
                            log.error(str(e))
                            self.currentLevel = Level.SUN

    def onFail(self):
        self.retry_times += 1

    def onSuccess(self):
        self.retry_times = 0
        self.currentLevel = Level.EARTH

    def shouldFallback(self):
        return self.retry_times > self.max_retry_times

    def fallback(self):
        # trigger auto vote
        proposals = voter.query_proposals(node=self.node)
        new_last_proposal_id = max(proposals.keys())
        for proposal_id in range(self.last_proposal_id,
                                 new_last_proposal_id):
            voter.vote(self.from_key, "No", proposal_id, self.passphrase,
                       node=self.node)
