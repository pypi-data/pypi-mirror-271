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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111llllll1_opy_, bstack111l1111_opy_, bstack111111ll_opy_, bstack1111ll1l1_opy_, \
    bstack111ll1lll1_opy_
def bstack1l11ll1ll_opy_(bstack1llll1l1ll1_opy_):
    for driver in bstack1llll1l1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l11l1_opy_(driver, status, reason=bstack11l11l_opy_ (u"ࠧࠨᒂ")):
    bstack111l11111_opy_ = Config.bstack1l11l1111_opy_()
    if bstack111l11111_opy_.bstack11ll1ll11l_opy_():
        return
    bstack1l111lll1_opy_ = bstack11ll1lll1_opy_(bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᒃ"), bstack11l11l_opy_ (u"ࠩࠪᒄ"), status, reason, bstack11l11l_opy_ (u"ࠪࠫᒅ"), bstack11l11l_opy_ (u"ࠫࠬᒆ"))
    driver.execute_script(bstack1l111lll1_opy_)
def bstack1l11ll1l11_opy_(page, status, reason=bstack11l11l_opy_ (u"ࠬ࠭ᒇ")):
    try:
        if page is None:
            return
        bstack111l11111_opy_ = Config.bstack1l11l1111_opy_()
        if bstack111l11111_opy_.bstack11ll1ll11l_opy_():
            return
        bstack1l111lll1_opy_ = bstack11ll1lll1_opy_(bstack11l11l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᒈ"), bstack11l11l_opy_ (u"ࠧࠨᒉ"), status, reason, bstack11l11l_opy_ (u"ࠨࠩᒊ"), bstack11l11l_opy_ (u"ࠩࠪᒋ"))
        page.evaluate(bstack11l11l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᒌ"), bstack1l111lll1_opy_)
    except Exception as e:
        print(bstack11l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᒍ"), e)
def bstack11ll1lll1_opy_(type, name, status, reason, bstack111ll1lll_opy_, bstack1l1l111l11_opy_):
    bstack1l1l1ll1l_opy_ = {
        bstack11l11l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᒎ"): type,
        bstack11l11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒏ"): {}
    }
    if type == bstack11l11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᒐ"):
        bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒑ")][bstack11l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᒒ")] = bstack111ll1lll_opy_
        bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒓ")][bstack11l11l_opy_ (u"ࠫࡩࡧࡴࡢࠩᒔ")] = json.dumps(str(bstack1l1l111l11_opy_))
    if type == bstack11l11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᒕ"):
        bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒖ")][bstack11l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒗ")] = name
    if type == bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᒘ"):
        bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᒙ")][bstack11l11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᒚ")] = status
        if status == bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒛ") and str(reason) != bstack11l11l_opy_ (u"ࠧࠨᒜ"):
            bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᒝ")][bstack11l11l_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᒞ")] = json.dumps(str(reason))
    bstack1lll11ll_opy_ = bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᒟ").format(json.dumps(bstack1l1l1ll1l_opy_))
    return bstack1lll11ll_opy_
def bstack1ll11lll11_opy_(url, config, logger, bstack1ll111ll1l_opy_=False):
    hostname = bstack111l1111_opy_(url)
    is_private = bstack1111ll1l1_opy_(hostname)
    try:
        if is_private or bstack1ll111ll1l_opy_:
            file_path = bstack111llllll1_opy_(bstack11l11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᒠ"), bstack11l11l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᒡ"), logger)
            if os.environ.get(bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᒢ")) and eval(
                    os.environ.get(bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᒣ"))):
                return
            if (bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᒤ") in config and not config[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᒥ")]):
                os.environ[bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᒦ")] = str(True)
                bstack1llll1l1lll_opy_ = {bstack11l11l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᒧ"): hostname}
                bstack111ll1lll1_opy_(bstack11l11l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᒨ"), bstack11l11l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᒩ"), bstack1llll1l1lll_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1ll11l1_opy_(caps, bstack1llll1ll111_opy_):
    if bstack11l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᒪ") in caps:
        caps[bstack11l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᒫ")][bstack11l11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᒬ")] = True
        if bstack1llll1ll111_opy_:
            caps[bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒭ")][bstack11l11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᒮ")] = bstack1llll1ll111_opy_
    else:
        caps[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᒯ")] = True
        if bstack1llll1ll111_opy_:
            caps[bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᒰ")] = bstack1llll1ll111_opy_
def bstack11ll111lll_opy_(bstack1l11l1111l_opy_):
    bstack1llll1l1l1l_opy_ = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᒱ"), bstack11l11l_opy_ (u"࠭ࠧᒲ"))
    if bstack1llll1l1l1l_opy_ == bstack11l11l_opy_ (u"ࠧࠨᒳ") or bstack1llll1l1l1l_opy_ == bstack11l11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᒴ"):
        threading.current_thread().testStatus = bstack1l11l1111l_opy_
    else:
        if bstack1l11l1111l_opy_ == bstack11l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᒵ"):
            threading.current_thread().testStatus = bstack1l11l1111l_opy_