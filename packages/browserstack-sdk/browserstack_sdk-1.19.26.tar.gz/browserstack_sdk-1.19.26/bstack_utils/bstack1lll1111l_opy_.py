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
import re
from bstack_utils.bstack1l1lllll1l_opy_ import bstack11ll111lll_opy_
def bstack11l1llll1l_opy_(fixture_name):
    if fixture_name.startswith(bstack11l11l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ๚")):
        return bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ๛")
    elif fixture_name.startswith(bstack11l11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ๜")):
        return bstack11l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨ๝")
    elif fixture_name.startswith(bstack11l11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ๞")):
        return bstack11l11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨ๟")
    elif fixture_name.startswith(bstack11l11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ๠")):
        return bstack11l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨ๡")
def bstack11ll1111ll_opy_(fixture_name):
    return bool(re.match(bstack11l11l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬ๢"), fixture_name))
def bstack11l1lllll1_opy_(fixture_name):
    return bool(re.match(bstack11l11l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ๣"), fixture_name))
def bstack11ll11111l_opy_(fixture_name):
    return bool(re.match(bstack11l11l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩ๤"), fixture_name))
def bstack11ll111ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11l11l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ๥")):
        return bstack11l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ๦"), bstack11l11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ๧")
    elif fixture_name.startswith(bstack11l11l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭๨")):
        return bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭๩"), bstack11l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ๪")
    elif fixture_name.startswith(bstack11l11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ๫")):
        return bstack11l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧ๬"), bstack11l11l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ๭")
    elif fixture_name.startswith(bstack11l11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ๮")):
        return bstack11l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨ๯"), bstack11l11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ๰")
    return None, None
def bstack11ll11l111_opy_(hook_name):
    if hook_name in [bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ๱"), bstack11l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ๲")]:
        return hook_name.capitalize()
    return hook_name
def bstack11ll111l11_opy_(hook_name):
    if hook_name in [bstack11l11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫ๳"), bstack11l11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪ๴")]:
        return bstack11l11l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ๵")
    elif hook_name in [bstack11l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ๶"), bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ๷")]:
        return bstack11l11l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ๸")
    elif hook_name in [bstack11l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭๹"), bstack11l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ๺")]:
        return bstack11l11l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨ๻")
    elif hook_name in [bstack11l11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧ๼"), bstack11l11l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ๽")]:
        return bstack11l11l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ๾")
    return hook_name
def bstack11l1llll11_opy_(node, scenario):
    if hasattr(node, bstack11l11l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪ๿")):
        parts = node.nodeid.rsplit(bstack11l11l_opy_ (u"ࠤ࡞ࠦ຀"))
        params = parts[-1]
        return bstack11l11l_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥກ").format(scenario.name, params)
    return scenario.name
def bstack11ll111111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11l11l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ຂ")):
            examples = list(node.callspec.params[bstack11l11l_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫ຃")].values())
        return examples
    except:
        return []
def bstack11ll1111l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack11l1llllll_opy_(report):
    try:
        status = bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ຄ")
        if report.passed or (report.failed and hasattr(report, bstack11l11l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤ຅"))):
            status = bstack11l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨຆ")
        elif report.skipped:
            status = bstack11l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪງ")
        bstack11ll111lll_opy_(status)
    except:
        pass
def bstack11ll1111_opy_(status):
    try:
        bstack11ll111l1l_opy_ = bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪຈ")
        if status == bstack11l11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫຉ"):
            bstack11ll111l1l_opy_ = bstack11l11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬຊ")
        elif status == bstack11l11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ຋"):
            bstack11ll111l1l_opy_ = bstack11l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨຌ")
        bstack11ll111lll_opy_(bstack11ll111l1l_opy_)
    except:
        pass
def bstack11l1lll1ll_opy_(item=None, report=None, summary=None, extra=None):
    return