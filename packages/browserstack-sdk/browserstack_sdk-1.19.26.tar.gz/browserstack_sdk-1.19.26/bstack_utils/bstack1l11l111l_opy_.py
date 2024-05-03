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
from collections import deque
from bstack_utils.constants import *
class bstack1l1lll1l1_opy_:
    def __init__(self):
        self._1llllll1lll_opy_ = deque()
        self._1llllll1l11_opy_ = {}
        self._1llllll11ll_opy_ = False
    def bstack1lllll1llll_opy_(self, test_name, bstack1lllll1l1ll_opy_):
        bstack1lllll1ll1l_opy_ = self._1llllll1l11_opy_.get(test_name, {})
        return bstack1lllll1ll1l_opy_.get(bstack1lllll1l1ll_opy_, 0)
    def bstack1llllll1ll1_opy_(self, test_name, bstack1lllll1l1ll_opy_):
        bstack1lllll1l11l_opy_ = self.bstack1lllll1llll_opy_(test_name, bstack1lllll1l1ll_opy_)
        self.bstack1llllll11l1_opy_(test_name, bstack1lllll1l1ll_opy_)
        return bstack1lllll1l11l_opy_
    def bstack1llllll11l1_opy_(self, test_name, bstack1lllll1l1ll_opy_):
        if test_name not in self._1llllll1l11_opy_:
            self._1llllll1l11_opy_[test_name] = {}
        bstack1lllll1ll1l_opy_ = self._1llllll1l11_opy_[test_name]
        bstack1lllll1l11l_opy_ = bstack1lllll1ll1l_opy_.get(bstack1lllll1l1ll_opy_, 0)
        bstack1lllll1ll1l_opy_[bstack1lllll1l1ll_opy_] = bstack1lllll1l11l_opy_ + 1
    def bstack1111lllll_opy_(self, bstack1lllll1l1l1_opy_, bstack1lllll1lll1_opy_):
        bstack1lllll1ll11_opy_ = self.bstack1llllll1ll1_opy_(bstack1lllll1l1l1_opy_, bstack1lllll1lll1_opy_)
        bstack1llllll111l_opy_ = bstack11l11l1111_opy_[bstack1lllll1lll1_opy_]
        bstack1llllll1111_opy_ = bstack11l11l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᑿ").format(bstack1lllll1l1l1_opy_, bstack1llllll111l_opy_, bstack1lllll1ll11_opy_)
        self._1llllll1lll_opy_.append(bstack1llllll1111_opy_)
    def bstack11ll11111_opy_(self):
        return len(self._1llllll1lll_opy_) == 0
    def bstack1llllll11l_opy_(self):
        bstack1llllll1l1l_opy_ = self._1llllll1lll_opy_.popleft()
        return bstack1llllll1l1l_opy_
    def capturing(self):
        return self._1llllll11ll_opy_
    def bstack1l1llll1l1_opy_(self):
        self._1llllll11ll_opy_ = True
    def bstack1lll1l11ll_opy_(self):
        self._1llllll11ll_opy_ = False