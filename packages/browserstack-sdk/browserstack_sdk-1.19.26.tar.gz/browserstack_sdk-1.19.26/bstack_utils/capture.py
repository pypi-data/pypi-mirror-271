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
import sys
class bstack11lll1llll_opy_:
    def __init__(self, handler):
        self._11l11ll111_opy_ = sys.stdout.write
        self._11l11l1lll_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l11l1ll1_opy_
        sys.stdout.error = self.bstack11l11l1l1l_opy_
    def bstack11l11l1ll1_opy_(self, _str):
        self._11l11ll111_opy_(_str)
        if self.handler:
            self.handler({bstack11l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬཁ"): bstack11l11l_opy_ (u"ࠧࡊࡐࡉࡓࠬག"), bstack11l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩགྷ"): _str})
    def bstack11l11l1l1l_opy_(self, _str):
        self._11l11l1lll_opy_(_str)
        if self.handler:
            self.handler({bstack11l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨང"): bstack11l11l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩཅ"), bstack11l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཆ"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l11ll111_opy_
        sys.stderr.write = self._11l11l1lll_opy_