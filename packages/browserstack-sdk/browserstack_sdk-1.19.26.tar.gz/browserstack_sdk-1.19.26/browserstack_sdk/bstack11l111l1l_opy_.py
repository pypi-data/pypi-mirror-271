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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1llll11l1l_opy_ as bstack1lll1ll11_opy_
from browserstack_sdk.bstack1lll111ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll1ll11_opy_
class bstack1l1l1ll1ll_opy_:
    def __init__(self, args, logger, bstack11ll1llll1_opy_, bstack11ll1ll1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1llll1_opy_ = bstack11ll1llll1_opy_
        self.bstack11ll1ll1l1_opy_ = bstack11ll1ll1l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1l1l111ll_opy_ = []
        self.bstack11lll111ll_opy_ = None
        self.bstack11l11ll1l_opy_ = []
        self.bstack11ll1l1ll1_opy_ = self.bstack111ll1l1l_opy_()
        self.bstack11l1l1111_opy_ = -1
    def bstack11111l11l_opy_(self, bstack11ll1ll1ll_opy_):
        self.parse_args()
        self.bstack11ll1l1l1l_opy_()
        self.bstack11ll1lllll_opy_(bstack11ll1ll1ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11lll11111_opy_():
        import importlib
        if getattr(importlib, bstack11l11l_opy_ (u"ࠪࡪ࡮ࡴࡤࡠ࡮ࡲࡥࡩ࡫ࡲࠨฑ"), False):
            bstack11ll1lll11_opy_ = importlib.find_loader(bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ฒ"))
        else:
            bstack11ll1lll11_opy_ = importlib.util.find_spec(bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧณ"))
    def bstack11lll1111l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l1l1111_opy_ = -1
        if bstack11l11l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ด") in self.bstack11ll1llll1_opy_:
            self.bstack11l1l1111_opy_ = int(self.bstack11ll1llll1_opy_[bstack11l11l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧต")])
        try:
            bstack11lll111l1_opy_ = [bstack11l11l_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪถ"), bstack11l11l_opy_ (u"ࠩ࠰࠱ࡵࡲࡵࡨ࡫ࡱࡷࠬท"), bstack11l11l_opy_ (u"ࠪ࠱ࡵ࠭ธ")]
            if self.bstack11l1l1111_opy_ >= 0:
                bstack11lll111l1_opy_.extend([bstack11l11l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬน"), bstack11l11l_opy_ (u"ࠬ࠳࡮ࠨบ")])
            for arg in bstack11lll111l1_opy_:
                self.bstack11lll1111l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1l1l1l_opy_(self):
        bstack11lll111ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lll111ll_opy_ = bstack11lll111ll_opy_
        return bstack11lll111ll_opy_
    def bstack11ll11l11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11lll11111_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1llll1ll11_opy_)
    def bstack11ll1lllll_opy_(self, bstack11ll1ll1ll_opy_):
        bstack111l11111_opy_ = Config.bstack1l11l1111_opy_()
        if bstack11ll1ll1ll_opy_:
            self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪป"))
            self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠧࡕࡴࡸࡩࠬผ"))
        if bstack111l11111_opy_.bstack11ll1ll11l_opy_():
            self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧฝ"))
            self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠩࡗࡶࡺ࡫ࠧพ"))
        self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠪ࠱ࡵ࠭ฟ"))
        self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩภ"))
        self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧม"))
        self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ย"))
        if self.bstack11l1l1111_opy_ > 1:
            self.bstack11lll111ll_opy_.append(bstack11l11l_opy_ (u"ࠧ࠮ࡰࠪร"))
            self.bstack11lll111ll_opy_.append(str(self.bstack11l1l1111_opy_))
    def bstack11ll1ll111_opy_(self):
        bstack11l11ll1l_opy_ = []
        for spec in self.bstack1l1l111ll_opy_:
            bstack1l1llllll1_opy_ = [spec]
            bstack1l1llllll1_opy_ += self.bstack11lll111ll_opy_
            bstack11l11ll1l_opy_.append(bstack1l1llllll1_opy_)
        self.bstack11l11ll1l_opy_ = bstack11l11ll1l_opy_
        return bstack11l11ll1l_opy_
    def bstack111ll1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11ll1l1ll1_opy_ = True
            return True
        except Exception as e:
            self.bstack11ll1l1ll1_opy_ = False
        return self.bstack11ll1l1ll1_opy_
    def bstack1ll1l1l11l_opy_(self, bstack11ll1lll1l_opy_, bstack11111l11l_opy_):
        bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨฤ")] = self.bstack11ll1llll1_opy_
        multiprocessing.set_start_method(bstack11l11l_opy_ (u"ࠩࡶࡴࡦࡽ࡮ࠨล"))
        if bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ฦ") in self.bstack11ll1llll1_opy_:
            bstack1l1lll11_opy_ = []
            manager = multiprocessing.Manager()
            bstack1l1lllllll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11ll1llll1_opy_[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧว")]):
                bstack1l1lll11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11ll1lll1l_opy_,
                                                           args=(self.bstack11lll111ll_opy_, bstack11111l11l_opy_, bstack1l1lllllll_opy_)))
            i = 0
            bstack11ll1l1lll_opy_ = len(self.bstack11ll1llll1_opy_[bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ")])
            for t in bstack1l1lll11_opy_:
                os.environ[bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ษ")] = str(i)
                os.environ[bstack11l11l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨส")] = json.dumps(self.bstack11ll1llll1_opy_[bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫห")][i % bstack11ll1l1lll_opy_])
                i += 1
                t.start()
            for t in bstack1l1lll11_opy_:
                t.join()
            return list(bstack1l1lllllll_opy_)
    @staticmethod
    def bstack1ll111l111_opy_(driver, bstack1ll11l11ll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ฬ"), None)
        if item and getattr(item, bstack11l11l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࠬอ"), None) and not getattr(item, bstack11l11l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࡠࡦࡲࡲࡪ࠭ฮ"), False):
            logger.info(
                bstack11l11l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠦฯ"))
            bstack11lll11l11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1lll1ll11_opy_.bstack1l1lll1l11_opy_(driver, bstack11lll11l11_opy_, item.name, item.module.__name__, item.path, bstack1ll11l11ll_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)