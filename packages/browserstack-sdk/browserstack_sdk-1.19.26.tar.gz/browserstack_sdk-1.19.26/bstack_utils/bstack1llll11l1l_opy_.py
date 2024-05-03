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
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11l1ll1lll_opy_ as bstack11l1l1ll11_opy_
from bstack_utils.bstack1l1l1ll1_opy_ import bstack1l1l1ll1_opy_
from bstack_utils.helper import bstack1lllll11_opy_, bstack111ll11l1_opy_, bstack11l1l1l1ll_opy_, bstack11l1ll11l1_opy_, bstack1llllllll1_opy_, get_host_info, bstack11l1ll1l1l_opy_, bstack1llll11l1_opy_, bstack1l1111l11l_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack1l1111l11l_opy_(class_method=False)
def _11l1l1l1l1_opy_(driver, bstack1ll11l11ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l11l_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩຍ"): caps.get(bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨຎ"), None),
        bstack11l11l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧຏ"): bstack1ll11l11ll_opy_.get(bstack11l11l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧຐ"), None),
        bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫຑ"): caps.get(bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫຒ"), None),
        bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩຓ"): caps.get(bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩດ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l11l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ຕ") + str(error))
  return response
def bstack1llll1111_opy_(config):
  return config.get(bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪຖ"), False) or any([p.get(bstack11l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫທ"), False) == True for p in config.get(bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨຘ"), [])])
def bstack1l1ll1llll_opy_(config, bstack1ll11lll_opy_):
  try:
    if not bstack111ll11l1_opy_(config):
      return False
    bstack11l1ll1l11_opy_ = config.get(bstack11l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ນ"), False)
    bstack11l1l11l1l_opy_ = config[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪບ")][bstack1ll11lll_opy_].get(bstack11l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨປ"), None)
    if bstack11l1l11l1l_opy_ != None:
      bstack11l1ll1l11_opy_ = bstack11l1l11l1l_opy_
    bstack11l1ll1ll1_opy_ = os.getenv(bstack11l11l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧຜ")) is not None and len(os.getenv(bstack11l11l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨຝ"))) > 0 and os.getenv(bstack11l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩພ")) != bstack11l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪຟ")
    return bstack11l1ll1l11_opy_ and bstack11l1ll1ll1_opy_
  except Exception as error:
    logger.debug(bstack11l11l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ຠ") + str(error))
  return False
def bstack11l1ll11_opy_(bstack11l1l1lll1_opy_, test_tags):
  bstack11l1l1lll1_opy_ = os.getenv(bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨມ"))
  if bstack11l1l1lll1_opy_ is None:
    return True
  bstack11l1l1lll1_opy_ = json.loads(bstack11l1l1lll1_opy_)
  try:
    include_tags = bstack11l1l1lll1_opy_[bstack11l11l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ຢ")] if bstack11l11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧຣ") in bstack11l1l1lll1_opy_ and isinstance(bstack11l1l1lll1_opy_[bstack11l11l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ຤")], list) else []
    exclude_tags = bstack11l1l1lll1_opy_[bstack11l11l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩລ")] if bstack11l11l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ຦") in bstack11l1l1lll1_opy_ and isinstance(bstack11l1l1lll1_opy_[bstack11l11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫວ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢຨ") + str(error))
  return False
def bstack1ll111ll11_opy_(config, bstack11l1l1l111_opy_, bstack11l1l11111_opy_, bstack11l1ll11ll_opy_):
  bstack11l1l11l11_opy_ = bstack11l1l1l1ll_opy_(config)
  bstack11l1l1111l_opy_ = bstack11l1ll11l1_opy_(config)
  if bstack11l1l11l11_opy_ is None or bstack11l1l1111l_opy_ is None:
    logger.error(bstack11l11l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩຩ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪສ"), bstack11l11l_opy_ (u"ࠪࡿࢂ࠭ຫ")))
    data = {
        bstack11l11l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩຬ"): config[bstack11l11l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪອ")],
        bstack11l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩຮ"): config.get(bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪຯ"), os.path.basename(os.getcwd())),
        bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫະ"): bstack1lllll11_opy_(),
        bstack11l11l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧັ"): config.get(bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭າ"), bstack11l11l_opy_ (u"ࠫࠬຳ")),
        bstack11l11l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬິ"): {
            bstack11l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ີ"): bstack11l1l1l111_opy_,
            bstack11l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪຶ"): bstack11l1l11111_opy_,
            bstack11l11l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬື"): __version__,
            bstack11l11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨຸࠫ"): bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰູࠪ"),
            bstack11l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮຺ࠫ"): bstack11l11l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧົ"),
            bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ຼ"): bstack11l1ll11ll_opy_
        },
        bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩຽ"): settings,
        bstack11l11l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩ຾"): bstack11l1ll1l1l_opy_(),
        bstack11l11l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ຿"): bstack1llllllll1_opy_(),
        bstack11l11l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬເ"): get_host_info(),
        bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ແ"): bstack111ll11l1_opy_(config)
    }
    headers = {
        bstack11l11l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫໂ"): bstack11l11l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩໃ"),
    }
    config = {
        bstack11l11l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬໄ"): (bstack11l1l11l11_opy_, bstack11l1l1111l_opy_),
        bstack11l11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ໅"): headers
    }
    response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧໆ"), bstack11l1l1ll11_opy_ + bstack11l11l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪ໇"), data, config)
    bstack11l1l1l11l_opy_ = response.json()
    if bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷ່ࠬ")]:
      parsed = json.loads(os.getenv(bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ້࠭"), bstack11l11l_opy_ (u"࠭ࡻࡾ໊ࠩ")))
      parsed[bstack11l11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ໋")] = bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭໌")][bstack11l11l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪໍ")]
      os.environ[bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ໎")] = json.dumps(parsed)
      bstack1l1l1ll1_opy_.bstack11l1ll111l_opy_(bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠫࡩࡧࡴࡢࠩ໏")][bstack11l11l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭໐")])
      bstack1l1l1ll1_opy_.bstack11l1l111l1_opy_(bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"࠭ࡤࡢࡶࡤࠫ໑")][bstack11l11l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ໒")])
      bstack1l1l1ll1_opy_.store()
      return bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠨࡦࡤࡸࡦ࠭໓")][bstack11l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ໔")], bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠪࡨࡦࡺࡡࠨ໕")][bstack11l11l_opy_ (u"ࠫ࡮ࡪࠧ໖")]
    else:
      logger.error(bstack11l11l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭໗") + bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ໘")])
      if bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໙")] == bstack11l11l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ໚"):
        for bstack11l1l11lll_opy_ in bstack11l1l1l11l_opy_[bstack11l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ໛")]:
          logger.error(bstack11l1l11lll_opy_[bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫໜ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧໝ") +  str(error))
    return None, None
def bstack111l11l1l_opy_():
  if os.getenv(bstack11l11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪໞ")) is None:
    return {
        bstack11l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ໟ"): bstack11l11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭໠"),
        bstack11l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໡"): bstack11l11l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨ໢")
    }
  data = {bstack11l11l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫ໣"): bstack1lllll11_opy_()}
  headers = {
      bstack11l11l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ໤"): bstack11l11l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭໥") + os.getenv(bstack11l11l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ໦")),
      bstack11l11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭໧"): bstack11l11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ໨")
  }
  response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠩࡓ࡙࡙࠭໩"), bstack11l1l1ll11_opy_ + bstack11l11l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬ໪"), data, { bstack11l11l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ໫"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l11l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨ໬") + datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"࡚࠭ࠨ໭"))
      return {bstack11l11l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ໮"): bstack11l11l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ໯"), bstack11l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ໰"): bstack11l11l_opy_ (u"ࠪࠫ໱")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l11l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢ໲") + str(error))
    return {
        bstack11l11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ໳"): bstack11l11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ໴"),
        bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ໵"): str(error)
    }
def bstack1l11ll1lll_opy_(caps, options):
  try:
    bstack11l1l1ll1l_opy_ = caps.get(bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ໶"), {}).get(bstack11l11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭໷"), caps.get(bstack11l11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ໸"), bstack11l11l_opy_ (u"ࠫࠬ໹")))
    if bstack11l1l1ll1l_opy_:
      logger.warn(bstack11l11l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ໺"))
      return False
    browser = caps.get(bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ໻"), bstack11l11l_opy_ (u"ࠧࠨ໼")).lower()
    if browser != bstack11l11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ໽"):
      logger.warn(bstack11l11l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧ໾"))
      return False
    browser_version = caps.get(bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ໿"), caps.get(bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ༀ")))
    if browser_version and browser_version != bstack11l11l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ༁") and int(browser_version.split(bstack11l11l_opy_ (u"࠭࠮ࠨ༂"))[0]) <= 94:
      logger.warn(bstack11l11l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠷࠲ࠧ༃"))
      return False
    if not options is None:
      bstack11l1lll111_opy_ = options.to_capabilities().get(bstack11l11l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭༄"), {})
      if bstack11l11l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭༅") in bstack11l1lll111_opy_.get(bstack11l11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ༆"), []):
        logger.warn(bstack11l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ༇"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ༈") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1l11ll1_opy_ = config.get(bstack11l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭༉"), {})
    bstack11l1l11ll1_opy_[bstack11l11l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ༊")] = os.getenv(bstack11l11l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭་"))
    bstack11l1lll1l1_opy_ = json.loads(os.getenv(bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ༌"), bstack11l11l_opy_ (u"ࠪࡿࢂ࠭།"))).get(bstack11l11l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ༎"))
    caps[bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ༏")] = True
    if bstack11l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ༐") in caps:
      caps[bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ༑")][bstack11l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ༒")] = bstack11l1l11ll1_opy_
      caps[bstack11l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ༓")][bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ༔")][bstack11l11l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ༕")] = bstack11l1lll1l1_opy_
    else:
      caps[bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ༖")] = bstack11l1l11ll1_opy_
      caps[bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ༗")][bstack11l11l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ༘")] = bstack11l1lll1l1_opy_
  except Exception as error:
    logger.debug(bstack11l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ༙") +  str(error))
def bstack1l1l1111ll_opy_(driver, bstack11l1lll11l_opy_):
  try:
    setattr(driver, bstack11l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ༚"), True)
    session = driver.session_id
    if session:
      bstack11l1l1llll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1l1llll_opy_ = False
      bstack11l1l1llll_opy_ = url.scheme in [bstack11l11l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣ༛"), bstack11l11l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ༜")]
      if bstack11l1l1llll_opy_:
        if bstack11l1lll11l_opy_:
          logger.info(bstack11l11l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧ༝"))
      return bstack11l1lll11l_opy_
  except Exception as e:
    logger.error(bstack11l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤ༞") + str(e))
    return False
def bstack1l1lll1l11_opy_(driver, class_name, name, module_name, path, bstack1ll11l11ll_opy_):
  try:
    bstack11lll11l11_opy_ = [class_name] if not class_name is None else []
    bstack11l11lllll_opy_ = {
        bstack11l11l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧ༟"): True,
        bstack11l11l_opy_ (u"ࠣࡶࡨࡷࡹࡊࡥࡵࡣ࡬ࡰࡸࠨ༠"): {
            bstack11l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ༡"): name,
            bstack11l11l_opy_ (u"ࠥࡸࡪࡹࡴࡓࡷࡱࡍࡩࠨ༢"): os.environ.get(bstack11l11l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆࠪ༣")),
            bstack11l11l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠢ༤"): str(path),
            bstack11l11l_opy_ (u"ࠨࡳࡤࡱࡳࡩࡑ࡯ࡳࡵࠤ༥"): [module_name, *bstack11lll11l11_opy_, name],
        },
        bstack11l11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ༦"): _11l1l1l1l1_opy_(driver, bstack1ll11l11ll_opy_)
    }
    logger.debug(bstack11l11l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ༧"))
    logger.debug(driver.execute_async_script(bstack1l1l1ll1_opy_.perform_scan, {bstack11l11l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ༨"): name}))
    logger.debug(driver.execute_async_script(bstack1l1l1ll1_opy_.bstack11l1ll1111_opy_, bstack11l11lllll_opy_))
    logger.info(bstack11l11l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ༩"))
  except Exception as bstack11l1l111ll_opy_:
    logger.error(bstack11l11l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ༪") + str(path) + bstack11l11l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢ༫") + str(bstack11l1l111ll_opy_))