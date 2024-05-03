# coding: UTF-8
import sys
bstack1111111_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack11ll1ll_opy_ = 7
def bstack11l11l_opy_ (bstack1l111_opy_):
    global bstack1lll11_opy_
    bstack11l11_opy_ = ord (bstack1l111_opy_ [-1])
    bstack11l111l_opy_ = bstack1l111_opy_ [:-1]
    bstack1ll1_opy_ = bstack11l11_opy_ % len (bstack11l111l_opy_)
    bstack1ll1l1_opy_ = bstack11l111l_opy_ [:bstack1ll1_opy_] + bstack11l111l_opy_ [bstack1ll1_opy_:]
    if bstack1111111_opy_:
        bstack11111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack1l1llll_opy_ + bstack11l11_opy_) % bstack11ll1ll_opy_) for bstack1l1llll_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11111l_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack1l1llll_opy_ + bstack11l11_opy_) % bstack11ll1ll_opy_) for bstack1l1llll_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11111l_opy_)
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1llll1_opy_, bstack11ll1ll1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1llll1_opy_ = bstack11ll1llll1_opy_
        self.bstack11ll1ll1l1_opy_ = bstack11ll1ll1l1_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11l111ll_opy_(bstack11ll1l11ll_opy_):
        bstack11ll1l1l11_opy_ = []
        if bstack11ll1l11ll_opy_:
            tokens = str(os.path.basename(bstack11ll1l11ll_opy_)).split(bstack11l11l_opy_ (u"ࠨ࡟ࠣะ"))
            camelcase_name = bstack11l11l_opy_ (u"ࠢࠡࠤั").join(t.title() for t in tokens)
            suite_name, bstack11ll1l11l1_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l1l11_opy_.append(suite_name)
        return bstack11ll1l1l11_opy_
    @staticmethod
    def bstack11ll1l111l_opy_(typename):
        if bstack11l11l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦา") in typename:
            return bstack11l11l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥำ")
        return bstack11l11l_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦิ")