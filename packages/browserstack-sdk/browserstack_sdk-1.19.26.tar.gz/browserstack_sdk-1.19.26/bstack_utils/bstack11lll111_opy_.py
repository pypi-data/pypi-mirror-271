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
from browserstack_sdk.bstack11l111l1l_opy_ import bstack1l1l1ll1ll_opy_
from browserstack_sdk.bstack1l111llll1_opy_ import RobotHandler
def bstack1ll1l1111l_opy_(framework):
    if framework.lower() == bstack11l11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᇛ"):
        return bstack1l1l1ll1ll_opy_.version()
    elif framework.lower() == bstack11l11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᇜ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11l11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᇝ"):
        import behave
        return behave.__version__
    else:
        return bstack11l11l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᇞ")