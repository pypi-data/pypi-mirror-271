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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1ll1l1111_opy_, bstack1111111l1_opy_, update, bstack1l11111l1_opy_,
                                       bstack111111l11_opy_, bstack1l1l1ll1l1_opy_, bstack1l11lll1_opy_, bstack11lll1l11_opy_,
                                       bstack1llll111_opy_, bstack1lll11llll_opy_, bstack1l1l1lll1_opy_, bstack1l11l11l_opy_,
                                       bstack111llll1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack11lllllll_opy_)
from browserstack_sdk.bstack11l111l1l_opy_ import bstack1l1l1ll1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack111ll1l1_opy_
from bstack_utils.capture import bstack11lll1llll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1l11l1ll_opy_, bstack1111l11ll_opy_, bstack1111l1111_opy_, \
    bstack1l1llll11l_opy_
from bstack_utils.helper import bstack111111ll_opy_, bstack1llll11l_opy_, bstack111l1ll1l1_opy_, bstack1lllll11_opy_, \
    bstack111l1l1l11_opy_, \
    bstack111llll1ll_opy_, bstack1l1ll1l1_opy_, bstack11ll1l1l1_opy_, bstack111ll11lll_opy_, bstack1111ll1l_opy_, Notset, \
    bstack1llll1ll1l_opy_, bstack111ll1ll1l_opy_, bstack111ll1111l_opy_, Result, bstack11l1111111_opy_, bstack111lll1l1l_opy_, bstack1l1111l11l_opy_, \
    bstack1l1lll11l_opy_, bstack1l1ll11111_opy_, bstack1l1ll111l1_opy_, bstack111ll1llll_opy_
from bstack_utils.bstack111l11l111_opy_ import bstack111l111l11_opy_
from bstack_utils.messages import bstack1llll1l111_opy_, bstack111l11ll1_opy_, bstack1llll1ll1_opy_, bstack1lllll1111_opy_, bstack1llll1ll11_opy_, \
    bstack1l1l11ll1l_opy_, bstack1ll111l1_opy_, bstack1lll11l1l_opy_, bstack11ll11l1l_opy_, bstack1l1l11l1l1_opy_, \
    bstack1l1111l1_opy_, bstack11l1l111_opy_
from bstack_utils.proxy import bstack1l1l11111_opy_, bstack1l1l1l1l1_opy_
from bstack_utils.bstack1lll1111l_opy_ import bstack11l1lll1ll_opy_, bstack11ll11l111_opy_, bstack11ll111l11_opy_, bstack11l1lllll1_opy_, \
    bstack11ll11111l_opy_, bstack11l1llll11_opy_, bstack11ll1111l1_opy_, bstack11ll1111_opy_, bstack11l1llllll_opy_
from bstack_utils.bstack1ll1l1l1ll_opy_ import bstack1llllllll_opy_
from bstack_utils.bstack1l1lllll1l_opy_ import bstack11ll1lll1_opy_, bstack1ll11lll11_opy_, bstack1ll1ll11l1_opy_, \
    bstack1ll1l11l1_opy_, bstack1l11ll1l11_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack1l111l1lll_opy_
from bstack_utils.bstack1lll1111_opy_ import bstack1ll1l1ll1l_opy_
import bstack_utils.bstack1llll11l1l_opy_ as bstack1lll1ll11_opy_
from bstack_utils.bstack1l1l1ll1_opy_ import bstack1l1l1ll1_opy_
bstack1l11l1ll1l_opy_ = None
bstack1lll11111l_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack1l11llllll_opy_ = None
bstack1l1l1111_opy_ = None
bstack1ll1ll11ll_opy_ = None
bstack1lll1l1ll1_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack11ll1l11l_opy_ = None
bstack1111l11l_opy_ = None
bstack111llll11_opy_ = None
bstack1l1l11lll_opy_ = bstack11l11l_opy_ (u"ࠧࠨᗙ")
CONFIG = {}
bstack11l111ll_opy_ = False
bstack1l11ll1111_opy_ = bstack11l11l_opy_ (u"ࠨࠩᗚ")
bstack1l11ll1ll1_opy_ = bstack11l11l_opy_ (u"ࠩࠪᗛ")
bstack1lll1l1l1l_opy_ = False
bstack1ll1111lll_opy_ = []
bstack11111l1ll_opy_ = bstack1l11l1ll_opy_
bstack1lll1l111l1_opy_ = bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᗜ")
bstack1lll11l11ll_opy_ = False
bstack1lll1l11_opy_ = {}
bstack1l1ll1l111_opy_ = False
logger = bstack111ll1l1_opy_.get_logger(__name__, bstack11111l1ll_opy_)
store = {
    bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗝ"): []
}
bstack1lll1l11l1l_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111111ll_opy_ = {}
current_test_uuid = None
def bstack1lll11l11l_opy_(page, bstack1lll1l1l11_opy_):
    try:
        page.evaluate(bstack11l11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᗞ"),
                      bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᗟ") + json.dumps(
                          bstack1lll1l1l11_opy_) + bstack11l11l_opy_ (u"ࠢࡾࡿࠥᗠ"))
    except Exception as e:
        print(bstack11l11l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᗡ"), e)
def bstack1llllll1ll_opy_(page, message, level):
    try:
        page.evaluate(bstack11l11l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᗢ"), bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨᗣ") + json.dumps(
            message) + bstack11l11l_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧᗤ") + json.dumps(level) + bstack11l11l_opy_ (u"ࠬࢃࡽࠨᗥ"))
    except Exception as e:
        print(bstack11l11l_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤᗦ"), e)
def pytest_configure(config):
    bstack111l11111_opy_ = Config.bstack1l11l1111_opy_()
    config.args = bstack1ll1l1ll1l_opy_.bstack1lll1lll111_opy_(config.args)
    bstack111l11111_opy_.bstack1l111l11l_opy_(bstack1l1ll111l1_opy_(config.getoption(bstack11l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᗧ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll11l1l1l_opy_ = item.config.getoption(bstack11l11l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᗨ"))
    plugins = item.config.getoption(bstack11l11l_opy_ (u"ࠤࡳࡰࡺ࡭ࡩ࡯ࡵࠥᗩ"))
    report = outcome.get_result()
    bstack1lll1l11ll1_opy_(item, call, report)
    if bstack11l11l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡲ࡯ࡹ࡬࡯࡮ࠣᗪ") not in plugins or bstack1111ll1l_opy_():
        return
    summary = []
    driver = getattr(item, bstack11l11l_opy_ (u"ࠦࡤࡪࡲࡪࡸࡨࡶࠧᗫ"), None)
    page = getattr(item, bstack11l11l_opy_ (u"ࠧࡥࡰࡢࡩࡨࠦᗬ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll11lll1l_opy_(item, report, summary, bstack1lll11l1l1l_opy_)
    if (page is not None):
        bstack1lll1l1l1l1_opy_(item, report, summary, bstack1lll11l1l1l_opy_)
def bstack1lll11lll1l_opy_(item, report, summary, bstack1lll11l1l1l_opy_):
    if report.when == bstack11l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᗭ") and report.skipped:
        bstack11l1llllll_opy_(report)
    if report.when in [bstack11l11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᗮ"), bstack11l11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᗯ")]:
        return
    if not bstack111l1ll1l1_opy_():
        return
    try:
        if (str(bstack1lll11l1l1l_opy_).lower() != bstack11l11l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᗰ")):
            item._driver.execute_script(
                bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠠࠨᗱ") + json.dumps(
                    report.nodeid) + bstack11l11l_opy_ (u"ࠫࢂࢃࠧᗲ"))
        os.environ[bstack11l11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨᗳ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11l11l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥ࠻ࠢࡾ࠴ࢂࠨᗴ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l11l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᗵ")))
    bstack1l11ll11l_opy_ = bstack11l11l_opy_ (u"ࠣࠤᗶ")
    bstack11l1llllll_opy_(report)
    if not passed:
        try:
            bstack1l11ll11l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11l11l_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᗷ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11ll11l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11l11l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᗸ")))
        bstack1l11ll11l_opy_ = bstack11l11l_opy_ (u"ࠦࠧᗹ")
        if not passed:
            try:
                bstack1l11ll11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l11l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᗺ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l11ll11l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᗻ")
                    + json.dumps(bstack11l11l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠡࠣᗼ"))
                    + bstack11l11l_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᗽ")
                )
            else:
                item._driver.execute_script(
                    bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᗾ")
                    + json.dumps(str(bstack1l11ll11l_opy_))
                    + bstack11l11l_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᗿ")
                )
        except Exception as e:
            summary.append(bstack11l11l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡤࡲࡳࡵࡴࡢࡶࡨ࠾ࠥࢁ࠰ࡾࠤᘀ").format(e))
def bstack1lll11l111l_opy_(test_name, error_message):
    try:
        bstack1lll1l1l1ll_opy_ = []
        bstack1ll11lll_opy_ = os.environ.get(bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᘁ"), bstack11l11l_opy_ (u"࠭࠰ࠨᘂ"))
        bstack1llll1l1ll_opy_ = {bstack11l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘃ"): test_name, bstack11l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᘄ"): error_message, bstack11l11l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᘅ"): bstack1ll11lll_opy_}
        bstack1lll1l111ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨᘆ"))
        if os.path.exists(bstack1lll1l111ll_opy_):
            with open(bstack1lll1l111ll_opy_) as f:
                bstack1lll1l1l1ll_opy_ = json.load(f)
        bstack1lll1l1l1ll_opy_.append(bstack1llll1l1ll_opy_)
        with open(bstack1lll1l111ll_opy_, bstack11l11l_opy_ (u"ࠫࡼ࠭ᘇ")) as f:
            json.dump(bstack1lll1l1l1ll_opy_, f)
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡧࡵࡷ࡮ࡹࡴࡪࡰࡪࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡲࡼࡸࡪࡹࡴࠡࡧࡵࡶࡴࡸࡳ࠻ࠢࠪᘈ") + str(e))
def bstack1lll1l1l1l1_opy_(item, report, summary, bstack1lll11l1l1l_opy_):
    if report.when in [bstack11l11l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᘉ"), bstack11l11l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᘊ")]:
        return
    if (str(bstack1lll11l1l1l_opy_).lower() != bstack11l11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᘋ")):
        bstack1lll11l11l_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11l11l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᘌ")))
    bstack1l11ll11l_opy_ = bstack11l11l_opy_ (u"ࠥࠦᘍ")
    bstack11l1llllll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l11ll11l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11l11l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᘎ").format(e)
                )
        try:
            if passed:
                bstack1l11ll1l11_opy_(getattr(item, bstack11l11l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᘏ"), None), bstack11l11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᘐ"))
            else:
                error_message = bstack11l11l_opy_ (u"ࠧࠨᘑ")
                if bstack1l11ll11l_opy_:
                    bstack1llllll1ll_opy_(item._page, str(bstack1l11ll11l_opy_), bstack11l11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢᘒ"))
                    bstack1l11ll1l11_opy_(getattr(item, bstack11l11l_opy_ (u"ࠩࡢࡴࡦ࡭ࡥࠨᘓ"), None), bstack11l11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᘔ"), str(bstack1l11ll11l_opy_))
                    error_message = str(bstack1l11ll11l_opy_)
                else:
                    bstack1l11ll1l11_opy_(getattr(item, bstack11l11l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᘕ"), None), bstack11l11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᘖ"))
                bstack1lll11l111l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11l11l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᘗ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11l11l_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᘘ"), default=bstack11l11l_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᘙ"), help=bstack11l11l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᘚ"))
    parser.addoption(bstack11l11l_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤᘛ"), default=bstack11l11l_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥᘜ"), help=bstack11l11l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦᘝ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11l11l_opy_ (u"ࠨ࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠣᘞ"), action=bstack11l11l_opy_ (u"ࠢࡴࡶࡲࡶࡪࠨᘟ"), default=bstack11l11l_opy_ (u"ࠣࡥ࡫ࡶࡴࡳࡥࠣᘠ"),
                         help=bstack11l11l_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳࠣᘡ"))
def bstack11lll11l1l_opy_(log):
    if not (log[bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘢ")] and log[bstack11l11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘣ")].strip()):
        return
    active = bstack1l111lll11_opy_()
    log = {
        bstack11l11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᘤ"): log[bstack11l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘥ")],
        bstack11l11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᘦ"): datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"ࠨ࡜ࠪᘧ"),
        bstack11l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘨ"): log[bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘩ")],
    }
    if active:
        if active[bstack11l11l_opy_ (u"ࠫࡹࡿࡰࡦࠩᘪ")] == bstack11l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᘫ"):
            log[bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘬ")] = active[bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘭ")]
        elif active[bstack11l11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘮ")] == bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺࠧᘯ"):
            log[bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘰ")] = active[bstack11l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘱ")]
    bstack1ll1l1ll1l_opy_.bstack111111lll_opy_([log])
def bstack1l111lll11_opy_():
    if len(store[bstack11l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᘲ")]) > 0 and store[bstack11l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘳ")][-1]:
        return {
            bstack11l11l_opy_ (u"ࠧࡵࡻࡳࡩࠬᘴ"): bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᘵ"),
            bstack11l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘶ"): store[bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᘷ")][-1]
        }
    if store.get(bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᘸ"), None):
        return {
            bstack11l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪᘹ"): bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࠫᘺ"),
            bstack11l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘻ"): store[bstack11l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᘼ")]
        }
    return None
bstack11lll11lll_opy_ = bstack11lll1llll_opy_(bstack11lll11l1l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll11l11ll_opy_
        item._1lll111ll11_opy_ = True
        bstack11l1ll111_opy_ = bstack1lll1ll11_opy_.bstack11l1ll11_opy_(CONFIG, bstack111llll1ll_opy_(item.own_markers))
        item._a11y_test_case = bstack11l1ll111_opy_
        if bstack1lll11l11ll_opy_:
            driver = getattr(item, bstack11l11l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᘽ"), None)
            item._a11y_started = bstack1lll1ll11_opy_.bstack1l1l1111ll_opy_(driver, bstack11l1ll111_opy_)
        if not bstack1ll1l1ll1l_opy_.on() or bstack1lll1l111l1_opy_ != bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᘾ"):
            return
        global current_test_uuid, bstack11lll11lll_opy_
        bstack11lll11lll_opy_.start()
        bstack11lll11ll1_opy_ = {
            bstack11l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᘿ"): uuid4().__str__(),
            bstack11l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙀ"): datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"࡚࠭ࠨᙁ")
        }
        current_test_uuid = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙂ")]
        store[bstack11l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᙃ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᙄ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l111111ll_opy_[item.nodeid] = {**_1l111111ll_opy_[item.nodeid], **bstack11lll11ll1_opy_}
        bstack1lll11l11l1_opy_(item, _1l111111ll_opy_[item.nodeid], bstack11l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙅ"))
    except Exception as err:
        print(bstack11l11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭ᙆ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1l11l1l_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111ll11lll_opy_():
        atexit.register(bstack1l11ll1ll_opy_)
        if not bstack1lll1l11l1l_opy_:
            try:
                bstack1lll11lllll_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack111ll1llll_opy_():
                    bstack1lll11lllll_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll11lllll_opy_:
                    signal.signal(s, bstack1lll111llll_opy_)
                bstack1lll1l11l1l_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11l11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡪ࡭ࡸࡺࡥࡳࠢࡶ࡭࡬ࡴࡡ࡭ࠢ࡫ࡥࡳࡪ࡬ࡦࡴࡶ࠾ࠥࠨᙇ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack11l1lll1ll_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11l11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᙈ")
    try:
        if not bstack1ll1l1ll1l_opy_.on():
            return
        bstack11lll11lll_opy_.start()
        uuid = uuid4().__str__()
        bstack11lll11ll1_opy_ = {
            bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙉ"): uuid,
            bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙊ"): datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"ࠩ࡝ࠫᙋ"),
            bstack11l11l_opy_ (u"ࠪࡸࡾࡶࡥࠨᙌ"): bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᙍ"),
            bstack11l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙎ"): bstack11l11l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᙏ"),
            bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᙐ"): bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᙑ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᙒ")] = item
        store[bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᙓ")] = [uuid]
        if not _1l111111ll_opy_.get(item.nodeid, None):
            _1l111111ll_opy_[item.nodeid] = {bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᙔ"): [], bstack11l11l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙕ"): []}
        _1l111111ll_opy_[item.nodeid][bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᙖ")].append(bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙗ")])
        _1l111111ll_opy_[item.nodeid + bstack11l11l_opy_ (u"ࠨ࠯ࡶࡩࡹࡻࡰࠨᙘ")] = bstack11lll11ll1_opy_
        bstack1lll1l1l11l_opy_(item, bstack11lll11ll1_opy_, bstack11l11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᙙ"))
    except Exception as err:
        print(bstack11l11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡷࡪࡺࡵࡱ࠼ࠣࡿࢂ࠭ᙚ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1lll1l11_opy_
        if CONFIG.get(bstack11l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᙛ"), False):
            if CONFIG.get(bstack11l11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᙜ"), bstack11l11l_opy_ (u"ࠨࡡࡶࡶࡲࠦᙝ")) == bstack11l11l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᙞ"):
                bstack1lll1l1ll11_opy_ = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᙟ"), None)
                bstack1ll1l11111_opy_ = bstack1lll1l1ll11_opy_ + bstack11l11l_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᙠ")
                driver = getattr(item, bstack11l11l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᙡ"), None)
                PercySDK.screenshot(driver, bstack1ll1l11111_opy_)
        if getattr(item, bstack11l11l_opy_ (u"ࠫࡤࡧ࠱࠲ࡻࡢࡷࡹࡧࡲࡵࡧࡧࠫᙢ"), False):
            bstack1l1l1ll1ll_opy_.bstack1ll111l111_opy_(getattr(item, bstack11l11l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᙣ"), None), bstack1lll1l11_opy_, logger, item)
        if not bstack1ll1l1ll1l_opy_.on():
            return
        bstack11lll11ll1_opy_ = {
            bstack11l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙤ"): uuid4().__str__(),
            bstack11l11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᙥ"): datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"ࠨ࡜ࠪᙦ"),
            bstack11l11l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᙧ"): bstack11l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᙨ"),
            bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᙩ"): bstack11l11l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᙪ"),
            bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᙫ"): bstack11l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᙬ")
        }
        _1l111111ll_opy_[item.nodeid + bstack11l11l_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫ᙭")] = bstack11lll11ll1_opy_
        bstack1lll1l1l11l_opy_(item, bstack11lll11ll1_opy_, bstack11l11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᙮"))
    except Exception as err:
        print(bstack11l11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩᙯ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll1l1ll1l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack11l1lllll1_opy_(fixturedef.argname):
        store[bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡯ࡴࡦ࡯ࠪᙰ")] = request.node
    elif bstack11ll11111l_opy_(fixturedef.argname):
        store[bstack11l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡣ࡭ࡣࡶࡷࡤ࡯ࡴࡦ࡯ࠪᙱ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙲ"): fixturedef.argname,
            bstack11l11l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᙳ"): bstack111l1l1l11_opy_(outcome),
            bstack11l11l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᙴ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᙵ")]
        if not _1l111111ll_opy_.get(current_test_item.nodeid, None):
            _1l111111ll_opy_[current_test_item.nodeid] = {bstack11l11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᙶ"): []}
        _1l111111ll_opy_[current_test_item.nodeid][bstack11l11l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᙷ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11l11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨᙸ"), str(err))
if bstack1111ll1l_opy_() and bstack1ll1l1ll1l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l111111ll_opy_[request.node.nodeid][bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᙹ")].bstack1llll1l11ll_opy_(id(step))
        except Exception as err:
            print(bstack11l11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰ࠻ࠢࡾࢁࠬᙺ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l111111ll_opy_[request.node.nodeid][bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᙻ")].bstack11lll1ll1l_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11l11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡹࡴࡦࡲࡢࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂ࠭ᙼ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11llll1l1l_opy_: bstack1l111l1lll_opy_ = _1l111111ll_opy_[request.node.nodeid][bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᙽ")]
            bstack11llll1l1l_opy_.bstack11lll1ll1l_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11l11l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᙾ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll1l111l1_opy_
        try:
            if not bstack1ll1l1ll1l_opy_.on() or bstack1lll1l111l1_opy_ != bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᙿ"):
                return
            global bstack11lll11lll_opy_
            bstack11lll11lll_opy_.start()
            driver = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ "), None)
            if not _1l111111ll_opy_.get(request.node.nodeid, None):
                _1l111111ll_opy_[request.node.nodeid] = {}
            bstack11llll1l1l_opy_ = bstack1l111l1lll_opy_.bstack1llll1111l1_opy_(
                scenario, feature, request.node,
                name=bstack11l1llll11_opy_(request.node, scenario),
                bstack11lllllll1_opy_=bstack1lllll11_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11l11l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᚁ"),
                tags=bstack11ll1111l1_opy_(feature, scenario),
                bstack1l11l111l1_opy_=bstack1ll1l1ll1l_opy_.bstack11llll1l11_opy_(driver) if driver and driver.session_id else {}
            )
            _1l111111ll_opy_[request.node.nodeid][bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᚂ")] = bstack11llll1l1l_opy_
            bstack1lll1l1111l_opy_(bstack11llll1l1l_opy_.uuid)
            bstack1ll1l1ll1l_opy_.bstack1l111l1111_opy_(bstack11l11l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᚃ"), bstack11llll1l1l_opy_)
        except Exception as err:
            print(bstack11l11l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯࠻ࠢࡾࢁࠬᚄ"), str(err))
def bstack1lll1l11111_opy_(bstack1lll11ll1ll_opy_):
    if bstack1lll11ll1ll_opy_ in store[bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᚅ")]:
        store[bstack11l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᚆ")].remove(bstack1lll11ll1ll_opy_)
def bstack1lll1l1111l_opy_(bstack1lll11l1111_opy_):
    store[bstack11l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᚇ")] = bstack1lll11l1111_opy_
    threading.current_thread().current_test_uuid = bstack1lll11l1111_opy_
@bstack1ll1l1ll1l_opy_.bstack1lll1lllll1_opy_
def bstack1lll1l11ll1_opy_(item, call, report):
    global bstack1lll1l111l1_opy_
    bstack1l1ll11ll_opy_ = bstack1lllll11_opy_()
    if hasattr(report, bstack11l11l_opy_ (u"ࠧࡴࡶࡲࡴࠬᚈ")):
        bstack1l1ll11ll_opy_ = bstack11l1111111_opy_(report.stop)
    elif hasattr(report, bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࠧᚉ")):
        bstack1l1ll11ll_opy_ = bstack11l1111111_opy_(report.start)
    try:
        if getattr(report, bstack11l11l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᚊ"), bstack11l11l_opy_ (u"ࠪࠫᚋ")) == bstack11l11l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᚌ"):
            bstack11lll11lll_opy_.reset()
        if getattr(report, bstack11l11l_opy_ (u"ࠬࡽࡨࡦࡰࠪᚍ"), bstack11l11l_opy_ (u"࠭ࠧᚎ")) == bstack11l11l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᚏ"):
            if bstack1lll1l111l1_opy_ == bstack11l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᚐ"):
                _1l111111ll_opy_[item.nodeid][bstack11l11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚑ")] = bstack1l1ll11ll_opy_
                bstack1lll11l11l1_opy_(item, _1l111111ll_opy_[item.nodeid], bstack11l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᚒ"), report, call)
                store[bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᚓ")] = None
            elif bstack1lll1l111l1_opy_ == bstack11l11l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠤᚔ"):
                bstack11llll1l1l_opy_ = _1l111111ll_opy_[item.nodeid][bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᚕ")]
                bstack11llll1l1l_opy_.set(hooks=_1l111111ll_opy_[item.nodeid].get(bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᚖ"), []))
                exception, bstack1l1111llll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1111llll_opy_ = [call.excinfo.exconly(), getattr(report, bstack11l11l_opy_ (u"ࠨ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠧᚗ"), bstack11l11l_opy_ (u"ࠩࠪᚘ"))]
                bstack11llll1l1l_opy_.stop(time=bstack1l1ll11ll_opy_, result=Result(result=getattr(report, bstack11l11l_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫᚙ"), bstack11l11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᚚ")), exception=exception, bstack1l1111llll_opy_=bstack1l1111llll_opy_))
                bstack1ll1l1ll1l_opy_.bstack1l111l1111_opy_(bstack11l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᚛"), _1l111111ll_opy_[item.nodeid][bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᚜")])
        elif getattr(report, bstack11l11l_opy_ (u"ࠧࡸࡪࡨࡲࠬ᚝"), bstack11l11l_opy_ (u"ࠨࠩ᚞")) in [bstack11l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᚟"), bstack11l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᚠ")]:
            bstack1l11111l11_opy_ = item.nodeid + bstack11l11l_opy_ (u"ࠫ࠲࠭ᚡ") + getattr(report, bstack11l11l_opy_ (u"ࠬࡽࡨࡦࡰࠪᚢ"), bstack11l11l_opy_ (u"࠭ࠧᚣ"))
            if getattr(report, bstack11l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᚤ"), False):
                hook_type = bstack11l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᚥ") if getattr(report, bstack11l11l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᚦ"), bstack11l11l_opy_ (u"ࠪࠫᚧ")) == bstack11l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᚨ") else bstack11l11l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᚩ")
                _1l111111ll_opy_[bstack1l11111l11_opy_] = {
                    bstack11l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᚪ"): uuid4().__str__(),
                    bstack11l11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᚫ"): bstack1l1ll11ll_opy_,
                    bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᚬ"): hook_type
                }
            _1l111111ll_opy_[bstack1l11111l11_opy_][bstack11l11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᚭ")] = bstack1l1ll11ll_opy_
            bstack1lll1l11111_opy_(_1l111111ll_opy_[bstack1l11111l11_opy_][bstack11l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚮ")])
            bstack1lll1l1l11l_opy_(item, _1l111111ll_opy_[bstack1l11111l11_opy_], bstack11l11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚯ"), report, call)
            if getattr(report, bstack11l11l_opy_ (u"ࠬࡽࡨࡦࡰࠪᚰ"), bstack11l11l_opy_ (u"࠭ࠧᚱ")) == bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᚲ"):
                if getattr(report, bstack11l11l_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩᚳ"), bstack11l11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᚴ")) == bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᚵ"):
                    bstack11lll11ll1_opy_ = {
                        bstack11l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᚶ"): uuid4().__str__(),
                        bstack11l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᚷ"): bstack1lllll11_opy_(),
                        bstack11l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᚸ"): bstack1lllll11_opy_()
                    }
                    _1l111111ll_opy_[item.nodeid] = {**_1l111111ll_opy_[item.nodeid], **bstack11lll11ll1_opy_}
                    bstack1lll11l11l1_opy_(item, _1l111111ll_opy_[item.nodeid], bstack11l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᚹ"))
                    bstack1lll11l11l1_opy_(item, _1l111111ll_opy_[item.nodeid], bstack11l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᚺ"), report, call)
    except Exception as err:
        print(bstack11l11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧᚻ"), str(err))
def bstack1lll11ll11l_opy_(test, bstack11lll11ll1_opy_, result=None, call=None, bstack11l1lllll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11llll1l1l_opy_ = {
        bstack11l11l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚼ"): bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᚽ")],
        bstack11l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪᚾ"): bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࠫᚿ"),
        bstack11l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᛀ"): test.name,
        bstack11l11l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᛁ"): {
            bstack11l11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᛂ"): bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᛃ"),
            bstack11l11l_opy_ (u"ࠫࡨࡵࡤࡦࠩᛄ"): inspect.getsource(test.obj)
        },
        bstack11l11l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᛅ"): test.name,
        bstack11l11l_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᛆ"): test.name,
        bstack11l11l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᛇ"): bstack1ll1l1ll1l_opy_.bstack1l11l111ll_opy_(test),
        bstack11l11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᛈ"): file_path,
        bstack11l11l_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᛉ"): file_path,
        bstack11l11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᛊ"): bstack11l11l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᛋ"),
        bstack11l11l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᛌ"): file_path,
        bstack11l11l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᛍ"): bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᛎ")],
        bstack11l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᛏ"): bstack11l11l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᛐ"),
        bstack11l11l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᛑ"): {
            bstack11l11l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᛒ"): test.nodeid
        },
        bstack11l11l_opy_ (u"ࠬࡺࡡࡨࡵࠪᛓ"): bstack111llll1ll_opy_(test.own_markers)
    }
    if bstack11l1lllll_opy_ in [bstack11l11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᛔ"), bstack11l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᛕ")]:
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᛖ")] = {
            bstack11l11l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᛗ"): bstack11lll11ll1_opy_.get(bstack11l11l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᛘ"), [])
        }
    if bstack11l1lllll_opy_ == bstack11l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᛙ"):
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛚ")] = bstack11l11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᛛ")
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᛜ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᛝ")]
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛞ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛟ")]
    if result:
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᛠ")] = result.outcome
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᛡ")] = result.duration * 1000
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛢ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛣ")]
        if result.failed:
            bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᛤ")] = bstack1ll1l1ll1l_opy_.bstack11ll1l111l_opy_(call.excinfo.typename)
            bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᛥ")] = bstack1ll1l1ll1l_opy_.bstack1lll1ll1l1l_opy_(call.excinfo, result)
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛦ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛧ")]
    if outcome:
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛨ")] = bstack111l1l1l11_opy_(outcome)
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᛩ")] = 0
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛪ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᛫")]
        if bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᛬")] == bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᛭"):
            bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᛮ")] = bstack11l11l_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᛯ")  # bstack1lll111l1ll_opy_
            bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᛰ")] = [{bstack11l11l_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᛱ"): [bstack11l11l_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᛲ")]}]
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛳ")] = bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛴ")]
    return bstack11llll1l1l_opy_
def bstack1lll11l1lll_opy_(test, bstack11llll1ll1_opy_, bstack11l1lllll_opy_, result, call, outcome, bstack1lll1l1ll1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᛵ")]
    hook_name = bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᛶ")]
    hook_data = {
        bstack11l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛷ"): bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᛸ")],
        bstack11l11l_opy_ (u"ࠨࡶࡼࡴࡪ࠭᛹"): bstack11l11l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ᛺"),
        bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ᛻"): bstack11l11l_opy_ (u"ࠫࢀࢃࠧ᛼").format(bstack11ll11l111_opy_(hook_name)),
        bstack11l11l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪ᛽"): {
            bstack11l11l_opy_ (u"࠭࡬ࡢࡰࡪࠫ᛾"): bstack11l11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ᛿"),
            bstack11l11l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᜀ"): None
        },
        bstack11l11l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᜁ"): test.name,
        bstack11l11l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᜂ"): bstack1ll1l1ll1l_opy_.bstack1l11l111ll_opy_(test, hook_name),
        bstack11l11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᜃ"): file_path,
        bstack11l11l_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᜄ"): file_path,
        bstack11l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜅ"): bstack11l11l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᜆ"),
        bstack11l11l_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᜇ"): file_path,
        bstack11l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜈ"): bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᜉ")],
        bstack11l11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᜊ"): bstack11l11l_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸ࠲ࡩࡵࡤࡷࡰࡦࡪࡸࠧᜋ") if bstack1lll1l111l1_opy_ == bstack11l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᜌ") else bstack11l11l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᜍ"),
        bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᜎ"): hook_type
    }
    bstack1lll11l1ll1_opy_ = bstack11lll1lll1_opy_(_1l111111ll_opy_.get(test.nodeid, None))
    if bstack1lll11l1ll1_opy_:
        hook_data[bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣ࡮ࡪࠧᜏ")] = bstack1lll11l1ll1_opy_
    if result:
        hook_data[bstack11l11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜐ")] = result.outcome
        hook_data[bstack11l11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᜑ")] = result.duration * 1000
        hook_data[bstack11l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜒ")] = bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜓ")]
        if result.failed:
            hook_data[bstack11l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ᜔࠭")] = bstack1ll1l1ll1l_opy_.bstack11ll1l111l_opy_(call.excinfo.typename)
            hook_data[bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦ᜕ࠩ")] = bstack1ll1l1ll1l_opy_.bstack1lll1ll1l1l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11l11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᜖")] = bstack111l1l1l11_opy_(outcome)
        hook_data[bstack11l11l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫ᜗")] = 100
        hook_data[bstack11l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᜘")] = bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᜙")]
        if hook_data[bstack11l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᜚")] == bstack11l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᜛"):
            hook_data[bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᜜")] = bstack11l11l_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪ᜝")  # bstack1lll111l1ll_opy_
            hook_data[bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᜞")] = [{bstack11l11l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᜟ"): [bstack11l11l_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᜠ")]}]
    if bstack1lll1l1ll1l_opy_:
        hook_data[bstack11l11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᜡ")] = bstack1lll1l1ll1l_opy_.result
        hook_data[bstack11l11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᜢ")] = bstack111ll1ll1l_opy_(bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜣ")], bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᜤ")])
        hook_data[bstack11l11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜥ")] = bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᜦ")]
        if hook_data[bstack11l11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᜧ")] == bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᜨ"):
            hook_data[bstack11l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᜩ")] = bstack1ll1l1ll1l_opy_.bstack11ll1l111l_opy_(bstack1lll1l1ll1l_opy_.exception_type)
            hook_data[bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᜪ")] = [{bstack11l11l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᜫ"): bstack111ll1111l_opy_(bstack1lll1l1ll1l_opy_.exception)}]
    return hook_data
def bstack1lll11l11l1_opy_(test, bstack11lll11ll1_opy_, bstack11l1lllll_opy_, result=None, call=None, outcome=None):
    bstack11llll1l1l_opy_ = bstack1lll11ll11l_opy_(test, bstack11lll11ll1_opy_, result, call, bstack11l1lllll_opy_, outcome)
    driver = getattr(test, bstack11l11l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᜬ"), None)
    if bstack11l1lllll_opy_ == bstack11l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᜭ") and driver:
        bstack11llll1l1l_opy_[bstack11l11l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᜮ")] = bstack1ll1l1ll1l_opy_.bstack11llll1l11_opy_(driver)
    if bstack11l1lllll_opy_ == bstack11l11l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᜯ"):
        bstack11l1lllll_opy_ = bstack11l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᜰ")
    bstack11llll1lll_opy_ = {
        bstack11l11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜱ"): bstack11l1lllll_opy_,
        bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᜲ"): bstack11llll1l1l_opy_
    }
    bstack1ll1l1ll1l_opy_.bstack11lllll1ll_opy_(bstack11llll1lll_opy_)
def bstack1lll1l1l11l_opy_(test, bstack11lll11ll1_opy_, bstack11l1lllll_opy_, result=None, call=None, outcome=None, bstack1lll1l1ll1l_opy_=None):
    hook_data = bstack1lll11l1lll_opy_(test, bstack11lll11ll1_opy_, bstack11l1lllll_opy_, result, call, outcome, bstack1lll1l1ll1l_opy_)
    bstack11llll1lll_opy_ = {
        bstack11l11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᜳ"): bstack11l1lllll_opy_,
        bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳ᜴࠭"): hook_data
    }
    bstack1ll1l1ll1l_opy_.bstack11lllll1ll_opy_(bstack11llll1lll_opy_)
def bstack11lll1lll1_opy_(bstack11lll11ll1_opy_):
    if not bstack11lll11ll1_opy_:
        return None
    if bstack11lll11ll1_opy_.get(bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ᜵"), None):
        return getattr(bstack11lll11ll1_opy_[bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ᜶")], bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᜷"), None)
    return bstack11lll11ll1_opy_.get(bstack11l11l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᜸"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll1l1ll1l_opy_.on():
            return
        places = [bstack11l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᜹"), bstack11l11l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ᜺"), bstack11l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭᜻")]
        bstack1l11111ll1_opy_ = []
        for bstack1lll1l11l11_opy_ in places:
            records = caplog.get_records(bstack1lll1l11l11_opy_)
            bstack1lll1l11lll_opy_ = bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᜼") if bstack1lll1l11l11_opy_ == bstack11l11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ᜽") else bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᜾")
            bstack1lll11ll111_opy_ = request.node.nodeid + (bstack11l11l_opy_ (u"ࠨࠩ᜿") if bstack1lll1l11l11_opy_ == bstack11l11l_opy_ (u"ࠩࡦࡥࡱࡲࠧᝀ") else bstack11l11l_opy_ (u"ࠪ࠱ࠬᝁ") + bstack1lll1l11l11_opy_)
            bstack1lll11l1111_opy_ = bstack11lll1lll1_opy_(_1l111111ll_opy_.get(bstack1lll11ll111_opy_, None))
            if not bstack1lll11l1111_opy_:
                continue
            for record in records:
                if bstack111lll1l1l_opy_(record.message):
                    continue
                bstack1l11111ll1_opy_.append({
                    bstack11l11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᝂ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack11l11l_opy_ (u"ࠬࡠࠧᝃ"),
                    bstack11l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᝄ"): record.levelname,
                    bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᝅ"): record.message,
                    bstack1lll1l11lll_opy_: bstack1lll11l1111_opy_
                })
        if len(bstack1l11111ll1_opy_) > 0:
            bstack1ll1l1ll1l_opy_.bstack111111lll_opy_(bstack1l11111ll1_opy_)
    except Exception as err:
        print(bstack11l11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬᝆ"), str(err))
def bstack1ll1l1l1l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1ll1l111_opy_
    bstack1l1l11l1_opy_ = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᝇ"), None) and bstack111111ll_opy_(
            threading.current_thread(), bstack11l11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᝈ"), None)
    bstack1lll1llll_opy_ = getattr(driver, bstack11l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᝉ"), None) != None and getattr(driver, bstack11l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᝊ"), None) == True
    if sequence == bstack11l11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᝋ") and driver != None:
      if not bstack1l1ll1l111_opy_ and bstack111l1ll1l1_opy_() and bstack11l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝌ") in CONFIG and CONFIG[bstack11l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᝍ")] == True and bstack1l1l1ll1_opy_.bstack1111lll1l_opy_(driver_command) and (bstack1lll1llll_opy_ or bstack1l1l11l1_opy_) and not bstack11lllllll_opy_(args):
        try:
          bstack1l1ll1l111_opy_ = True
          logger.debug(bstack11l11l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡽࢀࠫᝎ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11l11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡦࡴࡩࡳࡷࡳࠠࡴࡥࡤࡲࠥࢁࡽࠨᝏ").format(str(err)))
        bstack1l1ll1l111_opy_ = False
    if sequence == bstack11l11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᝐ"):
        if driver_command == bstack11l11l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩᝑ"):
            bstack1ll1l1ll1l_opy_.bstack1l1lllll11_opy_({
                bstack11l11l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬᝒ"): response[bstack11l11l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᝓ")],
                bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝔"): store[bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᝕")]
            })
def bstack1l11ll1ll_opy_():
    global bstack1ll1111lll_opy_
    bstack111ll1l1_opy_.bstack1l1ll1l1ll_opy_()
    logging.shutdown()
    bstack1ll1l1ll1l_opy_.bstack1l111ll1l1_opy_()
    for driver in bstack1ll1111lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll111llll_opy_(*args):
    global bstack1ll1111lll_opy_
    bstack1ll1l1ll1l_opy_.bstack1l111ll1l1_opy_()
    for driver in bstack1ll1111lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11l1ll1_opy_(self, *args, **kwargs):
    bstack1l11l1lll1_opy_ = bstack1l11l1ll1l_opy_(self, *args, **kwargs)
    bstack1ll1l1ll1l_opy_.bstack1llllll1l1_opy_(self)
    return bstack1l11l1lll1_opy_
def bstack1l1l1111l_opy_(framework_name):
    global bstack1l1l11lll_opy_
    global bstack1ll1l111l_opy_
    bstack1l1l11lll_opy_ = framework_name
    logger.info(bstack11l1l111_opy_.format(bstack1l1l11lll_opy_.split(bstack11l11l_opy_ (u"ࠪ࠱ࠬ᝖"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111l1ll1l1_opy_():
            Service.start = bstack1l11lll1_opy_
            Service.stop = bstack11lll1l11_opy_
            webdriver.Remote.__init__ = bstack1ll11l11_opy_
            webdriver.Remote.get = bstack1111lll1_opy_
            if not isinstance(os.getenv(bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ᝗")), str):
                return
            WebDriver.close = bstack1llll111_opy_
            WebDriver.quit = bstack1lllll1ll1_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111l1ll1l1_opy_() and bstack1ll1l1ll1l_opy_.on():
            webdriver.Remote.__init__ = bstack1ll11l1ll1_opy_
        bstack1ll1l111l_opy_ = True
    except Exception as e:
        pass
    bstack1l1l11111l_opy_()
    if os.environ.get(bstack11l11l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪ᝘")):
        bstack1ll1l111l_opy_ = eval(os.environ.get(bstack11l11l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫ᝙")))
    if not bstack1ll1l111l_opy_:
        bstack1l1l1lll1_opy_(bstack11l11l_opy_ (u"ࠢࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡱࡳࡹࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠤ᝚"), bstack1l1111l1_opy_)
    if bstack11l1l1l1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11ll1111l_opy_
        except Exception as e:
            logger.error(bstack1l1l11ll1l_opy_.format(str(e)))
    if bstack11l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᝛") in str(framework_name).lower():
        if not bstack111l1ll1l1_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack111111l11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1l1ll1l1_opy_
            Config.getoption = bstack1lll11lll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l11ll11_opy_
        except Exception as e:
            pass
def bstack1lllll1ll1_opy_(self):
    global bstack1l1l11lll_opy_
    global bstack1ll1111ll1_opy_
    global bstack1lll11111l_opy_
    try:
        if bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ᝜") in bstack1l1l11lll_opy_ and self.session_id != None and bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ᝝"), bstack11l11l_opy_ (u"ࠫࠬ᝞")) != bstack11l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᝟"):
            bstack1l11l1llll_opy_ = bstack11l11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᝠ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᝡ")
            bstack1l1ll11111_opy_(logger, True)
            if self != None:
                bstack1ll1l11l1_opy_(self, bstack1l11l1llll_opy_, bstack11l11l_opy_ (u"ࠨ࠮ࠣࠫᝢ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᝣ"), None)
        if item is not None and bstack1lll11l11ll_opy_:
            bstack1l1l1ll1ll_opy_.bstack1ll111l111_opy_(self, bstack1lll1l11_opy_, logger, item)
        threading.current_thread().testStatus = bstack11l11l_opy_ (u"ࠪࠫᝤ")
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᝥ") + str(e))
    bstack1lll11111l_opy_(self)
    self.session_id = None
def bstack1ll11l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1111ll1_opy_
    global bstack1lll111l1_opy_
    global bstack1lll1l1l1l_opy_
    global bstack1l1l11lll_opy_
    global bstack1l11l1ll1l_opy_
    global bstack1ll1111lll_opy_
    global bstack1l11ll1111_opy_
    global bstack1l11ll1ll1_opy_
    global bstack1lll11l11ll_opy_
    global bstack1lll1l11_opy_
    CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᝦ")] = str(bstack1l1l11lll_opy_) + str(__version__)
    command_executor = bstack11ll1l1l1_opy_(bstack1l11ll1111_opy_)
    logger.debug(bstack1lllll1111_opy_.format(command_executor))
    proxy = bstack111llll1_opy_(CONFIG, proxy)
    bstack1ll11lll_opy_ = 0
    try:
        if bstack1lll1l1l1l_opy_ is True:
            bstack1ll11lll_opy_ = int(os.environ.get(bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᝧ")))
    except:
        bstack1ll11lll_opy_ = 0
    bstack1ll1111111_opy_ = bstack1ll1l1111_opy_(CONFIG, bstack1ll11lll_opy_)
    logger.debug(bstack1lll11l1l_opy_.format(str(bstack1ll1111111_opy_)))
    bstack1lll1l11_opy_ = CONFIG.get(bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᝨ"))[bstack1ll11lll_opy_]
    if bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᝩ") in CONFIG and CONFIG[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᝪ")]:
        bstack1ll1ll11l1_opy_(bstack1ll1111111_opy_, bstack1l11ll1ll1_opy_)
    if bstack1lll1ll11_opy_.bstack1l1ll1llll_opy_(CONFIG, bstack1ll11lll_opy_) and bstack1lll1ll11_opy_.bstack1l11ll1lll_opy_(bstack1ll1111111_opy_, options):
        bstack1lll11l11ll_opy_ = True
        bstack1lll1ll11_opy_.set_capabilities(bstack1ll1111111_opy_, CONFIG)
    if desired_capabilities:
        bstack1llll11l11_opy_ = bstack1111111l1_opy_(desired_capabilities)
        bstack1llll11l11_opy_[bstack11l11l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᝫ")] = bstack1llll1ll1l_opy_(CONFIG)
        bstack1l11ll1l1_opy_ = bstack1ll1l1111_opy_(bstack1llll11l11_opy_)
        if bstack1l11ll1l1_opy_:
            bstack1ll1111111_opy_ = update(bstack1l11ll1l1_opy_, bstack1ll1111111_opy_)
        desired_capabilities = None
    if options:
        bstack1lll11llll_opy_(options, bstack1ll1111111_opy_)
    if not options:
        options = bstack1l11111l1_opy_(bstack1ll1111111_opy_)
    if proxy and bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᝬ")):
        options.proxy(proxy)
    if options and bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ᝭")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1ll1l1_opy_() < version.parse(bstack11l11l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᝮ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll1111111_opy_)
    logger.info(bstack1llll1ll1_opy_)
    if bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᝯ")):
        bstack1l11l1ll1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᝰ")):
        bstack1l11l1ll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩ᝱")):
        bstack1l11l1ll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l11l1ll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l1l11l1l_opy_ = bstack11l11l_opy_ (u"ࠪࠫᝲ")
        if bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᝳ")):
            bstack1l1l11l1l_opy_ = self.caps.get(bstack11l11l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ᝴"))
        else:
            bstack1l1l11l1l_opy_ = self.capabilities.get(bstack11l11l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨ᝵"))
        if bstack1l1l11l1l_opy_:
            bstack1l1lll11l_opy_(bstack1l1l11l1l_opy_)
            if bstack1l1ll1l1_opy_() <= version.parse(bstack11l11l_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ᝶")):
                self.command_executor._url = bstack11l11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ᝷") + bstack1l11ll1111_opy_ + bstack11l11l_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ᝸")
            else:
                self.command_executor._url = bstack11l11l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ᝹") + bstack1l1l11l1l_opy_ + bstack11l11l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ᝺")
            logger.debug(bstack111l11ll1_opy_.format(bstack1l1l11l1l_opy_))
        else:
            logger.debug(bstack1llll1l111_opy_.format(bstack11l11l_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨ᝻")))
    except Exception as e:
        logger.debug(bstack1llll1l111_opy_.format(e))
    bstack1ll1111ll1_opy_ = self.session_id
    if bstack11l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭᝼") in bstack1l1l11lll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11l11l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᝽"), None)
        if item:
            bstack1lll111ll1l_opy_ = getattr(item, bstack11l11l_opy_ (u"ࠨࡡࡷࡩࡸࡺ࡟ࡤࡣࡶࡩࡤࡹࡴࡢࡴࡷࡩࡩ࠭᝾"), False)
            if not getattr(item, bstack11l11l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᝿"), None) and bstack1lll111ll1l_opy_:
                setattr(store[bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧក")], bstack11l11l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬខ"), self)
        bstack1ll1l1ll1l_opy_.bstack1llllll1l1_opy_(self)
    bstack1ll1111lll_opy_.append(self)
    if bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨគ") in CONFIG and bstack11l11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫឃ") in CONFIG[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪង")][bstack1ll11lll_opy_]:
        bstack1lll111l1_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫច")][bstack1ll11lll_opy_][bstack11l11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឆ")]
    logger.debug(bstack1l1l11l1l1_opy_.format(bstack1ll1111ll1_opy_))
def bstack1111lll1_opy_(self, url):
    global bstack1ll11l1ll_opy_
    global CONFIG
    try:
        bstack1ll11lll11_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11ll11l1l_opy_.format(str(err)))
    try:
        bstack1ll11l1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack11l11ll1_opy_ = str(e)
            if any(err_msg in bstack11l11ll1_opy_ for err_msg in bstack1111l1111_opy_):
                bstack1ll11lll11_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11ll11l1l_opy_.format(str(err)))
        raise e
def bstack1l1l1l1ll1_opy_(item, when):
    global bstack1111l11l_opy_
    try:
        bstack1111l11l_opy_(item, when)
    except Exception as e:
        pass
def bstack11l11ll11_opy_(item, call, rep):
    global bstack111llll11_opy_
    global bstack1ll1111lll_opy_
    name = bstack11l11l_opy_ (u"ࠪࠫជ")
    try:
        if rep.when == bstack11l11l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩឈ"):
            bstack1ll1111ll1_opy_ = threading.current_thread().bstackSessionId
            bstack1lll11l1l1l_opy_ = item.config.getoption(bstack11l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧញ"))
            try:
                if (str(bstack1lll11l1l1l_opy_).lower() != bstack11l11l_opy_ (u"࠭ࡴࡳࡷࡨࠫដ")):
                    name = str(rep.nodeid)
                    bstack1l111lll1_opy_ = bstack11ll1lll1_opy_(bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨឋ"), name, bstack11l11l_opy_ (u"ࠨࠩឌ"), bstack11l11l_opy_ (u"ࠩࠪឍ"), bstack11l11l_opy_ (u"ࠪࠫណ"), bstack11l11l_opy_ (u"ࠫࠬត"))
                    os.environ[bstack11l11l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘࡤ࡚ࡅࡔࡖࡢࡒࡆࡓࡅࠨថ")] = name
                    for driver in bstack1ll1111lll_opy_:
                        if bstack1ll1111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l111lll1_opy_)
            except Exception as e:
                logger.debug(bstack11l11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ទ").format(str(e)))
            try:
                bstack11ll1111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨធ"):
                    status = bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨន") if rep.outcome.lower() == bstack11l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩប") else bstack11l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪផ")
                    reason = bstack11l11l_opy_ (u"ࠫࠬព")
                    if status == bstack11l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬភ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11l11l_opy_ (u"࠭ࡩ࡯ࡨࡲࠫម") if status == bstack11l11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧយ") else bstack11l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧរ")
                    data = name + bstack11l11l_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫល") if status == bstack11l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪវ") else name + bstack11l11l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧឝ") + reason
                    bstack1lll1l1111_opy_ = bstack11ll1lll1_opy_(bstack11l11l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧឞ"), bstack11l11l_opy_ (u"࠭ࠧស"), bstack11l11l_opy_ (u"ࠧࠨហ"), bstack11l11l_opy_ (u"ࠨࠩឡ"), level, data)
                    for driver in bstack1ll1111lll_opy_:
                        if bstack1ll1111ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1lll1l1111_opy_)
            except Exception as e:
                logger.debug(bstack11l11l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭អ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧឣ").format(str(e)))
    bstack111llll11_opy_(item, call, rep)
notset = Notset()
def bstack1lll11lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack11ll1l11l_opy_
    if str(name).lower() == bstack11l11l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫឤ"):
        return bstack11l11l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦឥ")
    else:
        return bstack11ll1l11l_opy_(self, name, default, skip)
def bstack11ll1111l_opy_(self):
    global CONFIG
    global bstack1ll1ll11ll_opy_
    try:
        proxy = bstack1l1l11111_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11l11l_opy_ (u"࠭࠮ࡱࡣࡦࠫឦ")):
                proxies = bstack1l1l1l1l1_opy_(proxy, bstack11ll1l1l1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1l1l111_opy_ = proxies.popitem()
                    if bstack11l11l_opy_ (u"ࠢ࠻࠱࠲ࠦឧ") in bstack1l1l1l111_opy_:
                        return bstack1l1l1l111_opy_
                    else:
                        return bstack11l11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤឨ") + bstack1l1l1l111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11l11l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡶࡲࡰࡺࡼࠤࡺࡸ࡬ࠡ࠼ࠣࡿࢂࠨឩ").format(str(e)))
    return bstack1ll1ll11ll_opy_(self)
def bstack11l1l1l1l_opy_():
    return (bstack11l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ឪ") in CONFIG or bstack11l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨឫ") in CONFIG) and bstack1llll11l_opy_() and bstack1l1ll1l1_opy_() >= version.parse(
        bstack1111l11ll_opy_)
def bstack1l1l1llll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lll111l1_opy_
    global bstack1lll1l1l1l_opy_
    global bstack1l1l11lll_opy_
    CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧឬ")] = str(bstack1l1l11lll_opy_) + str(__version__)
    bstack1ll11lll_opy_ = 0
    try:
        if bstack1lll1l1l1l_opy_ is True:
            bstack1ll11lll_opy_ = int(os.environ.get(bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ឭ")))
    except:
        bstack1ll11lll_opy_ = 0
    CONFIG[bstack11l11l_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨឮ")] = True
    bstack1ll1111111_opy_ = bstack1ll1l1111_opy_(CONFIG, bstack1ll11lll_opy_)
    logger.debug(bstack1lll11l1l_opy_.format(str(bstack1ll1111111_opy_)))
    if CONFIG.get(bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬឯ")):
        bstack1ll1ll11l1_opy_(bstack1ll1111111_opy_, bstack1l11ll1ll1_opy_)
    if bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬឰ") in CONFIG and bstack11l11l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨឱ") in CONFIG[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧឲ")][bstack1ll11lll_opy_]:
        bstack1lll111l1_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨឳ")][bstack1ll11lll_opy_][bstack11l11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ឴")]
    import urllib
    import json
    bstack11l1l1l1_opy_ = bstack11l11l_opy_ (u"ࠧࡸࡵࡶ࠾࠴࠵ࡣࡥࡲ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࡂࡧࡦࡶࡳ࠾ࠩ឵") + urllib.parse.quote(json.dumps(bstack1ll1111111_opy_))
    browser = self.connect(bstack11l1l1l1_opy_)
    return browser
def bstack1l1l11111l_opy_():
    global bstack1ll1l111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1l1llll_opy_
        bstack1ll1l111l_opy_ = True
    except Exception as e:
        pass
def bstack1lll11ll1l1_opy_():
    global CONFIG
    global bstack11l111ll_opy_
    global bstack1l11ll1111_opy_
    global bstack1l11ll1ll1_opy_
    global bstack1lll1l1l1l_opy_
    global bstack11111l1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧា")))
    bstack11l111ll_opy_ = eval(os.environ.get(bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪិ")))
    bstack1l11ll1111_opy_ = os.environ.get(bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡋ࡙ࡇࡥࡕࡓࡎࠪី"))
    bstack1l11l11l_opy_(CONFIG, bstack11l111ll_opy_)
    bstack11111l1ll_opy_ = bstack111ll1l1_opy_.bstack1111111l_opy_(CONFIG, bstack11111l1ll_opy_)
    global bstack1l11l1ll1l_opy_
    global bstack1lll11111l_opy_
    global bstack1l1l1l1l_opy_
    global bstack1l11lll1ll_opy_
    global bstack1l11llllll_opy_
    global bstack1l1l1111_opy_
    global bstack1lll1l1ll1_opy_
    global bstack1ll11l1ll_opy_
    global bstack1ll1ll11ll_opy_
    global bstack11ll1l11l_opy_
    global bstack1111l11l_opy_
    global bstack111llll11_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11l1ll1l_opy_ = webdriver.Remote.__init__
        bstack1lll11111l_opy_ = WebDriver.quit
        bstack1lll1l1ll1_opy_ = WebDriver.close
        bstack1ll11l1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧឹ") in CONFIG or bstack11l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩឺ") in CONFIG) and bstack1llll11l_opy_():
        if bstack1l1ll1l1_opy_() < version.parse(bstack1111l11ll_opy_):
            logger.error(bstack1ll111l1_opy_.format(bstack1l1ll1l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1ll1ll11ll_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l1l11ll1l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack11ll1l11l_opy_ = Config.getoption
        from _pytest import runner
        bstack1111l11l_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1llll1ll11_opy_)
    try:
        from pytest_bdd import reporting
        bstack111llll11_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹࡵࠠࡳࡷࡱࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡨࡷࡹࡹࠧុ"))
    bstack1l11ll1ll1_opy_ = CONFIG.get(bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫូ"), {}).get(bstack11l11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪួ"))
    bstack1lll1l1l1l_opy_ = True
    bstack1l1l1111l_opy_(bstack1l1llll11l_opy_)
if (bstack111ll11lll_opy_()):
    bstack1lll11ll1l1_opy_()
@bstack1l1111l11l_opy_(class_method=False)
def bstack1lll1l1l111_opy_(hook_name, event, bstack1lll11l1l11_opy_=None):
    if hook_name not in [bstack11l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪើ"), bstack11l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧឿ"), bstack11l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪៀ"), bstack11l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧេ"), bstack11l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫែ"), bstack11l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨៃ"), bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧោ"), bstack11l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫៅ")]:
        return
    node = store[bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧំ")]
    if hook_name in [bstack11l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࠪះ"), bstack11l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧៈ")]:
        node = store[bstack11l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬ៉")]
    elif hook_name in [bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ៊"), bstack11l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩ់")]:
        node = store[bstack11l11l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ៌")]
    if event == bstack11l11l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ៍"):
        hook_type = bstack11ll111l11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11llll1ll1_opy_ = {
            bstack11l11l_opy_ (u"ࠫࡺࡻࡩࡥࠩ៎"): uuid,
            bstack11l11l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ៏"): bstack1lllll11_opy_(),
            bstack11l11l_opy_ (u"࠭ࡴࡺࡲࡨࠫ័"): bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ៑"),
            bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨ្ࠫ"): hook_type,
            bstack11l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ៓"): hook_name
        }
        store[bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ។")].append(uuid)
        bstack1lll11lll11_opy_ = node.nodeid
        if hook_type == bstack11l11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ៕"):
            if not _1l111111ll_opy_.get(bstack1lll11lll11_opy_, None):
                _1l111111ll_opy_[bstack1lll11lll11_opy_] = {bstack11l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ៖"): []}
            _1l111111ll_opy_[bstack1lll11lll11_opy_][bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬៗ")].append(bstack11llll1ll1_opy_[bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៘")])
        _1l111111ll_opy_[bstack1lll11lll11_opy_ + bstack11l11l_opy_ (u"ࠨ࠯ࠪ៙") + hook_name] = bstack11llll1ll1_opy_
        bstack1lll1l1l11l_opy_(node, bstack11llll1ll1_opy_, bstack11l11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ៚"))
    elif event == bstack11l11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩ៛"):
        bstack1l11111l11_opy_ = node.nodeid + bstack11l11l_opy_ (u"ࠫ࠲࠭ៜ") + hook_name
        _1l111111ll_opy_[bstack1l11111l11_opy_][bstack11l11l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ៝")] = bstack1lllll11_opy_()
        bstack1lll1l11111_opy_(_1l111111ll_opy_[bstack1l11111l11_opy_][bstack11l11l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ៞")])
        bstack1lll1l1l11l_opy_(node, _1l111111ll_opy_[bstack1l11111l11_opy_], bstack11l11l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ៟"), bstack1lll1l1ll1l_opy_=bstack1lll11l1l11_opy_)
def bstack1lll111lll1_opy_():
    global bstack1lll1l111l1_opy_
    if bstack1111ll1l_opy_():
        bstack1lll1l111l1_opy_ = bstack11l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ០")
    else:
        bstack1lll1l111l1_opy_ = bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ១")
@bstack1ll1l1ll1l_opy_.bstack1lll1lllll1_opy_
def bstack1lll11llll1_opy_():
    bstack1lll111lll1_opy_()
    if bstack1llll11l_opy_():
        bstack1llllllll_opy_(bstack1ll1l1l1l1_opy_)
    try:
        bstack111l111l11_opy_(bstack1lll1l1l111_opy_)
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ២").format(e))
bstack1lll11llll1_opy_()