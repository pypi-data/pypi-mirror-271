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
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l111llll1_opy_ import RobotHandler
from bstack_utils.capture import bstack11lll1llll_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack1l111lll1l_opy_, bstack1l111l11l1_opy_, bstack1l111l1lll_opy_
from bstack_utils.bstack1lll1111_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack111111ll_opy_, bstack1lllll11_opy_, Result, \
    bstack1l1111l11l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭൅"): [],
        bstack11l11l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩെ"): [],
        bstack11l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨേ"): []
    }
    bstack1l1111l1l1_opy_ = []
    bstack1l111l1l11_opy_ = []
    @staticmethod
    def bstack11lll11l1l_opy_(log):
        if not (log[bstack11l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ൈ")] and log[bstack11l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ൉")].strip()):
            return
        active = bstack1ll1l1ll1l_opy_.bstack1l111lll11_opy_()
        log = {
            bstack11l11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ൊ"): log[bstack11l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧോ")],
            bstack11l11l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬൌ"): datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"ࠪ࡞്ࠬ"),
            bstack11l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൎ"): log[bstack11l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭൏")],
        }
        if active:
            if active[bstack11l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ൐")] == bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ൑"):
                log[bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ൒")] = active[bstack11l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ൓")]
            elif active[bstack11l11l_opy_ (u"ࠪࡸࡾࡶࡥࠨൔ")] == bstack11l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࠩൕ"):
                log[bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬൖ")] = active[bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ൗ")]
        bstack1ll1l1ll1l_opy_.bstack111111lll_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111lllll_opy_ = None
        self._11llllll1l_opy_ = None
        self._1l111111ll_opy_ = OrderedDict()
        self.bstack11lll11lll_opy_ = bstack11lll1llll_opy_(self.bstack11lll11l1l_opy_)
    @bstack1l1111l11l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l1111ll1l_opy_()
        if not self._1l111111ll_opy_.get(attrs.get(bstack11l11l_opy_ (u"ࠧࡪࡦࠪ൘")), None):
            self._1l111111ll_opy_[attrs.get(bstack11l11l_opy_ (u"ࠨ࡫ࡧࠫ൙"))] = {}
        bstack1l111l11ll_opy_ = bstack1l111l1lll_opy_(
                bstack11llll11l1_opy_=attrs.get(bstack11l11l_opy_ (u"ࠩ࡬ࡨࠬ൚")),
                name=name,
                bstack11lllllll1_opy_=bstack1lllll11_opy_(),
                file_path=os.path.relpath(attrs[bstack11l11l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൛")], start=os.getcwd()) if attrs.get(bstack11l11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ൜")) != bstack11l11l_opy_ (u"ࠬ࠭൝") else bstack11l11l_opy_ (u"࠭ࠧ൞"),
                framework=bstack11l11l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭ൟ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l11l_opy_ (u"ࠨ࡫ࡧࠫൠ"), None)
        self._1l111111ll_opy_[attrs.get(bstack11l11l_opy_ (u"ࠩ࡬ࡨࠬൡ"))][bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ൢ")] = bstack1l111l11ll_opy_
    @bstack1l1111l11l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1l1111ll11_opy_()
        self._11llll111l_opy_(messages)
        for bstack1l11111111_opy_ in self.bstack1l1111l1l1_opy_:
            bstack1l11111111_opy_[bstack11l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ൣ")][bstack11l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ൤")].extend(self.store[bstack11l11l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ൥")])
            bstack1ll1l1ll1l_opy_.bstack11lllll1ll_opy_(bstack1l11111111_opy_)
        self.bstack1l1111l1l1_opy_ = []
        self.store[bstack11l11l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭൦")] = []
    @bstack1l1111l11l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lll11lll_opy_.start()
        if not self._1l111111ll_opy_.get(attrs.get(bstack11l11l_opy_ (u"ࠨ࡫ࡧࠫ൧")), None):
            self._1l111111ll_opy_[attrs.get(bstack11l11l_opy_ (u"ࠩ࡬ࡨࠬ൨"))] = {}
        driver = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ൩"), None)
        bstack11llll1l1l_opy_ = bstack1l111l1lll_opy_(
            bstack11llll11l1_opy_=attrs.get(bstack11l11l_opy_ (u"ࠫ࡮ࡪࠧ൪")),
            name=name,
            bstack11lllllll1_opy_=bstack1lllll11_opy_(),
            file_path=os.path.relpath(attrs[bstack11l11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ൫")], start=os.getcwd()),
            scope=RobotHandler.bstack1l11l111ll_opy_(attrs.get(bstack11l11l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭൬"), None)),
            framework=bstack11l11l_opy_ (u"ࠧࡓࡱࡥࡳࡹ࠭൭"),
            tags=attrs[bstack11l11l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭൮")],
            hooks=self.store[bstack11l11l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨ൯")],
            bstack1l11l111l1_opy_=bstack1ll1l1ll1l_opy_.bstack11llll1l11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l11l_opy_ (u"ࠥࡿࢂࠦ࡜࡯ࠢࡾࢁࠧ൰").format(bstack11l11l_opy_ (u"ࠦࠥࠨ൱").join(attrs[bstack11l11l_opy_ (u"ࠬࡺࡡࡨࡵࠪ൲")]), name) if attrs[bstack11l11l_opy_ (u"࠭ࡴࡢࡩࡶࠫ൳")] else name
        )
        self._1l111111ll_opy_[attrs.get(bstack11l11l_opy_ (u"ࠧࡪࡦࠪ൴"))][bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ൵")] = bstack11llll1l1l_opy_
        threading.current_thread().current_test_uuid = bstack11llll1l1l_opy_.bstack11llllll11_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l11l_opy_ (u"ࠩ࡬ࡨࠬ൶"), None)
        self.bstack1l111l1111_opy_(bstack11l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ൷"), bstack11llll1l1l_opy_)
    @bstack1l1111l11l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lll11lll_opy_.reset()
        bstack1l11l1111l_opy_ = bstack1l1111l111_opy_.get(attrs.get(bstack11l11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ൸")), bstack11l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭൹"))
        self._1l111111ll_opy_[attrs.get(bstack11l11l_opy_ (u"࠭ࡩࡥࠩൺ"))][bstack11l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൻ")].stop(time=bstack1lllll11_opy_(), duration=int(attrs.get(bstack11l11l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ർ"), bstack11l11l_opy_ (u"ࠩ࠳ࠫൽ"))), result=Result(result=bstack1l11l1111l_opy_, exception=attrs.get(bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫൾ")), bstack1l1111llll_opy_=[attrs.get(bstack11l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬൿ"))]))
        self.bstack1l111l1111_opy_(bstack11l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ඀"), self._1l111111ll_opy_[attrs.get(bstack11l11l_opy_ (u"࠭ࡩࡥࠩඁ"))][bstack11l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪං")], True)
        self.store[bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬඃ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack1l1111l11l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l1111ll1l_opy_()
        current_test_id = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ඄"), None)
        bstack11llll1111_opy_ = current_test_id if bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬඅ"), None) else bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧආ"), None)
        if attrs.get(bstack11l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪඇ"), bstack11l11l_opy_ (u"࠭ࠧඈ")).lower() in [bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ඉ"), bstack11l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪඊ")]:
            hook_type = bstack1l11l11l11_opy_(attrs.get(bstack11l11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧඋ")), bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧඌ"), None))
            hook_name = bstack11l11l_opy_ (u"ࠫࢀࢃࠧඍ").format(attrs.get(bstack11l11l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬඎ"), bstack11l11l_opy_ (u"࠭ࠧඏ")))
            if hook_type in [bstack11l11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫඐ"), bstack11l11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫඑ")]:
                hook_name = bstack11l11l_opy_ (u"ࠩ࡞ࡿࢂࡣࠠࡼࡿࠪඒ").format(bstack11lllll1l1_opy_.get(hook_type), attrs.get(bstack11l11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪඓ"), bstack11l11l_opy_ (u"ࠫࠬඔ")))
            bstack11llll1ll1_opy_ = bstack1l111l11l1_opy_(
                bstack11llll11l1_opy_=bstack11llll1111_opy_ + bstack11l11l_opy_ (u"ࠬ࠳ࠧඕ") + attrs.get(bstack11l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫඖ"), bstack11l11l_opy_ (u"ࠧࠨ඗")).lower(),
                name=hook_name,
                bstack11lllllll1_opy_=bstack1lllll11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ඘")), start=os.getcwd()),
                framework=bstack11l11l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨ඙"),
                tags=attrs[bstack11l11l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨක")],
                scope=RobotHandler.bstack1l11l111ll_opy_(attrs.get(bstack11l11l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫඛ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11llll1ll1_opy_.bstack11llllll11_opy_()
            threading.current_thread().current_hook_id = bstack11llll1111_opy_ + bstack11l11l_opy_ (u"ࠬ࠳ࠧග") + attrs.get(bstack11l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫඝ"), bstack11l11l_opy_ (u"ࠧࠨඞ")).lower()
            self.store[bstack11l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬඟ")] = [bstack11llll1ll1_opy_.bstack11llllll11_opy_()]
            if bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ච"), None):
                self.store[bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧඡ")].append(bstack11llll1ll1_opy_.bstack11llllll11_opy_())
            else:
                self.store[bstack11l11l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪජ")].append(bstack11llll1ll1_opy_.bstack11llllll11_opy_())
            if bstack11llll1111_opy_:
                self._1l111111ll_opy_[bstack11llll1111_opy_ + bstack11l11l_opy_ (u"ࠬ࠳ࠧඣ") + attrs.get(bstack11l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫඤ"), bstack11l11l_opy_ (u"ࠧࠨඥ")).lower()] = { bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫඦ"): bstack11llll1ll1_opy_ }
            bstack1ll1l1ll1l_opy_.bstack1l111l1111_opy_(bstack11l11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪට"), bstack11llll1ll1_opy_)
        else:
            bstack1l111l111l_opy_ = {
                bstack11l11l_opy_ (u"ࠪ࡭ࡩ࠭ඨ"): uuid4().__str__(),
                bstack11l11l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩඩ"): bstack11l11l_opy_ (u"ࠬࢁࡽࠡࡽࢀࠫඪ").format(attrs.get(bstack11l11l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ණ")), attrs.get(bstack11l11l_opy_ (u"ࠧࡢࡴࡪࡷࠬඬ"), bstack11l11l_opy_ (u"ࠨࠩත"))) if attrs.get(bstack11l11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧථ"), []) else attrs.get(bstack11l11l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪද")),
                bstack11l11l_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫධ"): attrs.get(bstack11l11l_opy_ (u"ࠬࡧࡲࡨࡵࠪන"), []),
                bstack11l11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ඲"): bstack1lllll11_opy_(),
                bstack11l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧඳ"): bstack11l11l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩප"),
                bstack11l11l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧඵ"): attrs.get(bstack11l11l_opy_ (u"ࠪࡨࡴࡩࠧබ"), bstack11l11l_opy_ (u"ࠫࠬභ"))
            }
            if attrs.get(bstack11l11l_opy_ (u"ࠬࡲࡩࡣࡰࡤࡱࡪ࠭ම"), bstack11l11l_opy_ (u"࠭ࠧඹ")) != bstack11l11l_opy_ (u"ࠧࠨය"):
                bstack1l111l111l_opy_[bstack11l11l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩර")] = attrs.get(bstack11l11l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪ඼"))
            if not self.bstack1l111l1l11_opy_:
                self._1l111111ll_opy_[self._1l11111lll_opy_()][bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ල")].add_step(bstack1l111l111l_opy_)
                threading.current_thread().current_step_uuid = bstack1l111l111l_opy_[bstack11l11l_opy_ (u"ࠫ࡮ࡪࠧ඾")]
            self.bstack1l111l1l11_opy_.append(bstack1l111l111l_opy_)
    @bstack1l1111l11l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1l1111ll11_opy_()
        self._11llll111l_opy_(messages)
        current_test_id = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡪࠧ඿"), None)
        bstack11llll1111_opy_ = current_test_id if current_test_id else bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩව"), None)
        bstack1l11l11111_opy_ = bstack1l1111l111_opy_.get(attrs.get(bstack11l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧශ")), bstack11l11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩෂ"))
        bstack1l111ll1ll_opy_ = attrs.get(bstack11l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪස"))
        if bstack1l11l11111_opy_ != bstack11l11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫහ") and not attrs.get(bstack11l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬළ")) and self._1l111lllll_opy_:
            bstack1l111ll1ll_opy_ = self._1l111lllll_opy_
        bstack11lll1ll11_opy_ = Result(result=bstack1l11l11111_opy_, exception=bstack1l111ll1ll_opy_, bstack1l1111llll_opy_=[bstack1l111ll1ll_opy_])
        if attrs.get(bstack11l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪෆ"), bstack11l11l_opy_ (u"࠭ࠧ෇")).lower() in [bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭෈"), bstack11l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ෉")]:
            bstack11llll1111_opy_ = current_test_id if current_test_id else bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨ්ࠬ"), None)
            if bstack11llll1111_opy_:
                bstack1l11111l11_opy_ = bstack11llll1111_opy_ + bstack11l11l_opy_ (u"ࠥ࠱ࠧ෋") + attrs.get(bstack11l11l_opy_ (u"ࠫࡹࡿࡰࡦࠩ෌"), bstack11l11l_opy_ (u"ࠬ࠭෍")).lower()
                self._1l111111ll_opy_[bstack1l11111l11_opy_][bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෎")].stop(time=bstack1lllll11_opy_(), duration=int(attrs.get(bstack11l11l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬා"), bstack11l11l_opy_ (u"ࠨ࠲ࠪැ"))), result=bstack11lll1ll11_opy_)
                bstack1ll1l1ll1l_opy_.bstack1l111l1111_opy_(bstack11l11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫෑ"), self._1l111111ll_opy_[bstack1l11111l11_opy_][bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ි")])
        else:
            bstack11llll1111_opy_ = current_test_id if current_test_id else bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢ࡭ࡩ࠭ී"), None)
            if bstack11llll1111_opy_ and len(self.bstack1l111l1l11_opy_) == 1:
                current_step_uuid = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡵࡧࡳࡣࡺࡻࡩࡥࠩු"), None)
                self._1l111111ll_opy_[bstack11llll1111_opy_][bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෕")].bstack11lll1ll1l_opy_(current_step_uuid, duration=int(attrs.get(bstack11l11l_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬූ"), bstack11l11l_opy_ (u"ࠨ࠲ࠪ෗"))), result=bstack11lll1ll11_opy_)
            else:
                self.bstack1l111ll11l_opy_(attrs)
            self.bstack1l111l1l11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l11l_opy_ (u"ࠩ࡫ࡸࡲࡲࠧෘ"), bstack11l11l_opy_ (u"ࠪࡲࡴ࠭ෙ")) == bstack11l11l_opy_ (u"ࠫࡾ࡫ࡳࠨේ"):
                return
            self.messages.push(message)
            bstack1l11111ll1_opy_ = []
            if bstack1ll1l1ll1l_opy_.bstack1l111lll11_opy_():
                bstack1l11111ll1_opy_.append({
                    bstack11l11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨෛ"): bstack1lllll11_opy_(),
                    bstack11l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧො"): message.get(bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨෝ")),
                    bstack11l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧෞ"): message.get(bstack11l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨෟ")),
                    **bstack1ll1l1ll1l_opy_.bstack1l111lll11_opy_()
                })
                if len(bstack1l11111ll1_opy_) > 0:
                    bstack1ll1l1ll1l_opy_.bstack111111lll_opy_(bstack1l11111ll1_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1ll1l1ll1l_opy_.bstack1l111ll1l1_opy_()
    def bstack1l111ll11l_opy_(self, bstack1l111ll111_opy_):
        if not bstack1ll1l1ll1l_opy_.bstack1l111lll11_opy_():
            return
        kwname = bstack11l11l_opy_ (u"ࠪࡿࢂࠦࡻࡾࠩ෠").format(bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ෡")), bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠬࡧࡲࡨࡵࠪ෢"), bstack11l11l_opy_ (u"࠭ࠧ෣"))) if bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠧࡢࡴࡪࡷࠬ෤"), []) else bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ෥"))
        error_message = bstack11l11l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠡࡾࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࡀࠠ࡝ࠤࡾ࠶ࢂࡢࠢࠣ෦").format(kwname, bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ෧")), str(bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෨"))))
        bstack1l1111111l_opy_ = bstack11l11l_opy_ (u"ࠧࡱࡷ࡯ࡣࡰࡩ࠿ࠦ࡜ࠣࡽ࠳ࢁࡡࠨࠠࡽࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡠࠧࢁ࠱ࡾ࡞ࠥࠦ෩").format(kwname, bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෪")))
        bstack11lll1l1ll_opy_ = error_message if bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ෫")) else bstack1l1111111l_opy_
        bstack11lllll111_opy_ = {
            bstack11l11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ෬"): self.bstack1l111l1l11_opy_[-1].get(bstack11l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭෭"), bstack1lllll11_opy_()),
            bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ෮"): bstack11lll1l1ll_opy_,
            bstack11l11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ෯"): bstack11l11l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ෰") if bstack1l111ll111_opy_.get(bstack11l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭෱")) == bstack11l11l_opy_ (u"ࠧࡇࡃࡌࡐࠬෲ") else bstack11l11l_opy_ (u"ࠨࡋࡑࡊࡔ࠭ෳ"),
            **bstack1ll1l1ll1l_opy_.bstack1l111lll11_opy_()
        }
        bstack1ll1l1ll1l_opy_.bstack111111lll_opy_([bstack11lllll111_opy_])
    def _1l11111lll_opy_(self):
        for bstack11llll11l1_opy_ in reversed(self._1l111111ll_opy_):
            bstack11lll1l111_opy_ = bstack11llll11l1_opy_
            data = self._1l111111ll_opy_[bstack11llll11l1_opy_][bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ෴")]
            if isinstance(data, bstack1l111l11l1_opy_):
                if not bstack11l11l_opy_ (u"ࠪࡉࡆࡉࡈࠨ෵") in data.bstack11lll1l1l1_opy_():
                    return bstack11lll1l111_opy_
            else:
                return bstack11lll1l111_opy_
    def _11llll111l_opy_(self, messages):
        try:
            bstack11llllllll_opy_ = BuiltIn().get_variable_value(bstack11l11l_opy_ (u"ࠦࠩࢁࡌࡐࡉࠣࡐࡊ࡜ࡅࡍࡿࠥ෶")) in (bstack1l1111lll1_opy_.DEBUG, bstack1l1111lll1_opy_.TRACE)
            for message, bstack1l111l1l1l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l11l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭෷"))
                level = message.get(bstack11l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ෸"))
                if level == bstack1l1111lll1_opy_.FAIL:
                    self._1l111lllll_opy_ = name or self._1l111lllll_opy_
                    self._11llllll1l_opy_ = bstack1l111l1l1l_opy_.get(bstack11l11l_opy_ (u"ࠢ࡮ࡧࡶࡷࡦ࡭ࡥࠣ෹")) if bstack11llllllll_opy_ and bstack1l111l1l1l_opy_ else self._11llllll1l_opy_
        except:
            pass
    @classmethod
    def bstack1l111l1111_opy_(self, event: str, bstack1l111l1ll1_opy_: bstack1l111lll1l_opy_, bstack11lll1l11l_opy_=False):
        if event == bstack11l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ෺"):
            bstack1l111l1ll1_opy_.set(hooks=self.store[bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭෻")])
        if event == bstack11l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ෼"):
            event = bstack11l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭෽")
        if bstack11lll1l11l_opy_:
            bstack11llll1lll_opy_ = {
                bstack11l11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ෾"): event,
                bstack1l111l1ll1_opy_.bstack1l111111l1_opy_(): bstack1l111l1ll1_opy_.bstack11lllll11l_opy_(event)
            }
            self.bstack1l1111l1l1_opy_.append(bstack11llll1lll_opy_)
        else:
            bstack1ll1l1ll1l_opy_.bstack1l111l1111_opy_(event, bstack1l111l1ll1_opy_)
class Messages:
    def __init__(self):
        self._1l11111l1l_opy_ = []
    def bstack1l1111ll1l_opy_(self):
        self._1l11111l1l_opy_.append([])
    def bstack1l1111ll11_opy_(self):
        return self._1l11111l1l_opy_.pop() if self._1l11111l1l_opy_ else list()
    def push(self, message):
        self._1l11111l1l_opy_[-1].append(message) if self._1l11111l1l_opy_ else self._1l11111l1l_opy_.append([message])
class bstack1l1111lll1_opy_:
    FAIL = bstack11l11l_opy_ (u"࠭ࡆࡂࡋࡏࠫ෿")
    ERROR = bstack11l11l_opy_ (u"ࠧࡆࡔࡕࡓࡗ࠭฀")
    WARNING = bstack11l11l_opy_ (u"ࠨ࡙ࡄࡖࡓ࠭ก")
    bstack1l1111l1ll_opy_ = bstack11l11l_opy_ (u"ࠩࡌࡒࡋࡕࠧข")
    DEBUG = bstack11l11l_opy_ (u"ࠪࡈࡊࡈࡕࡈࠩฃ")
    TRACE = bstack11l11l_opy_ (u"࡙ࠫࡘࡁࡄࡇࠪค")
    bstack11llll11ll_opy_ = [FAIL, ERROR]
def bstack11lll1lll1_opy_(bstack11lll11ll1_opy_):
    if not bstack11lll11ll1_opy_:
        return None
    if bstack11lll11ll1_opy_.get(bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨฅ"), None):
        return getattr(bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩฆ")], bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬง"), None)
    return bstack11lll11ll1_opy_.get(bstack11l11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭จ"), None)
def bstack1l11l11l11_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨฉ"), bstack11l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬช")]:
        return
    if hook_type.lower() == bstack11l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪซ"):
        if current_test_uuid is None:
            return bstack11l11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩฌ")
        else:
            return bstack11l11l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫญ")
    elif hook_type.lower() == bstack11l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩฎ"):
        if current_test_uuid is None:
            return bstack11l11l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫฏ")
        else:
            return bstack11l11l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ฐ")