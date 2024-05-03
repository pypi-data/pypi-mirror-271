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
class bstack1llllllll_opy_:
    def __init__(self, handler):
        self._1llll1ll1l1_opy_ = None
        self.handler = handler
        self._1llll1lll11_opy_ = self.bstack1llll1ll1ll_opy_()
        self.patch()
    def patch(self):
        self._1llll1ll1l1_opy_ = self._1llll1lll11_opy_.execute
        self._1llll1lll11_opy_.execute = self.bstack1llll1ll11l_opy_()
    def bstack1llll1ll11l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11l11l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࠧᒀ"), driver_command, None, this, args)
            response = self._1llll1ll1l1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11l11l_opy_ (u"ࠨࡡࡧࡶࡨࡶࠧᒁ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1lll11_opy_.execute = self._1llll1ll1l1_opy_
    @staticmethod
    def bstack1llll1ll1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver