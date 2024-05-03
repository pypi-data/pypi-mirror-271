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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11l1ll1l1l_opy_, bstack1llllllll1_opy_, get_host_info, bstack11l1l1l1ll_opy_, bstack11l1ll11l1_opy_, bstack111ll11ll1_opy_, \
    bstack11l1111l11_opy_, bstack111lll11l1_opy_, bstack1llll11l1_opy_, bstack111ll1l1l1_opy_, bstack1l1ll111l1_opy_, bstack1l1111l11l_opy_, bstack111l1l1l1_opy_
from bstack_utils.bstack1lllll1111l_opy_ import bstack1llll1lllll_opy_
from bstack_utils.bstack11llll1l1l_opy_ import bstack1l111lll1l_opy_
import bstack_utils.bstack1llll11l1l_opy_ as bstack1lll1ll11_opy_
from bstack_utils.constants import bstack11l111l111_opy_
bstack1lll1ll1111_opy_ = [
    bstack11l11l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᓴ"), bstack11l11l_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧᓵ"), bstack11l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓶ"), bstack11l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᓷ"),
    bstack11l11l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓸ"), bstack11l11l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᓹ"), bstack11l11l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᓺ")
]
bstack1lll1l1llll_opy_ = bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᓻ")
logger = logging.getLogger(__name__)
class bstack1ll1l1ll1l_opy_:
    bstack1lllll1111l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def launch(cls, bs_config, bstack1lll1l1lll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1llll1l_opy_()
        bstack11l1l11l11_opy_ = bstack11l1l1l1ll_opy_(bs_config)
        bstack11l1l1111l_opy_ = bstack11l1ll11l1_opy_(bs_config)
        bstack1l1l111l_opy_ = False
        bstack1ll111ll1_opy_ = False
        if bstack11l11l_opy_ (u"ࠪࡥࡵࡶࠧᓼ") in bs_config:
            bstack1l1l111l_opy_ = True
        else:
            bstack1ll111ll1_opy_ = True
        bstack1l1l1l1l11_opy_ = {
            bstack11l11l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᓽ"): cls.bstack111llllll_opy_(bstack1lll1l1lll1_opy_.get(bstack11l11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᓾ"), bstack11l11l_opy_ (u"࠭ࠧᓿ"))),
            bstack11l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᔀ"): bstack1lll1ll11_opy_.bstack1llll1111_opy_(bs_config),
            bstack11l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᔁ"): bs_config.get(bstack11l11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᔂ"), False),
            bstack11l11l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᔃ"): bstack1ll111ll1_opy_,
            bstack11l11l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪᔄ"): bstack1l1l111l_opy_
        }
        data = {
            bstack11l11l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬᔅ"): bstack11l11l_opy_ (u"࠭ࡪࡴࡱࡱࠫᔆ"),
            bstack11l11l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ᔇ"): bs_config.get(bstack11l11l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᔈ"), bstack11l11l_opy_ (u"ࠩࠪᔉ")),
            bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᔊ"): bs_config.get(bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᔋ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᔌ"): bs_config.get(bstack11l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᔍ")),
            bstack11l11l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᔎ"): bs_config.get(bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᔏ"), bstack11l11l_opy_ (u"ࠩࠪᔐ")),
            bstack11l11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࠧᔑ"): datetime.datetime.now().isoformat(),
            bstack11l11l_opy_ (u"ࠫࡹࡧࡧࡴࠩᔒ"): bstack111ll11ll1_opy_(bs_config),
            bstack11l11l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᔓ"): get_host_info(),
            bstack11l11l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᔔ"): bstack1llllllll1_opy_(),
            bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᔕ"): os.environ.get(bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᔖ")),
            bstack11l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᔗ"): os.environ.get(bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᔘ"), False),
            bstack11l11l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᔙ"): bstack11l1ll1l1l_opy_(),
            bstack11l11l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪᔚ"): bstack1l1l1l1l11_opy_,
            bstack11l11l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᔛ"): {
                bstack11l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᔜ"): bstack1lll1l1lll1_opy_.get(bstack11l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᔝ"), bstack11l11l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᔞ")),
                bstack11l11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔟ"): bstack1lll1l1lll1_opy_.get(bstack11l11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔠ")),
                bstack11l11l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᔡ"): bstack1lll1l1lll1_opy_.get(bstack11l11l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᔢ"))
            }
        }
        config = {
            bstack11l11l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᔣ"): (bstack11l1l11l11_opy_, bstack11l1l1111l_opy_),
            bstack11l11l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᔤ"): cls.default_headers()
        }
        response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᔥ"), cls.request_url(bstack11l11l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵࠪᔦ")), data, config)
        if response.status_code != 200:
            os.environ[bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᔧ")] = bstack11l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᔨ")
            os.environ[bstack11l11l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᔩ")] = bstack11l11l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᔪ")
            os.environ[bstack11l11l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᔫ")] = bstack11l11l_opy_ (u"ࠩࡱࡹࡱࡲࠧᔬ")
            os.environ[bstack11l11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᔭ")] = bstack11l11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᔮ")
            os.environ[bstack11l11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᔯ")] = bstack11l11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔰ")
            bstack1lll1ll1lll_opy_ = response.json()
            if bstack1lll1ll1lll_opy_ and bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᔱ")]:
                error_message = bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᔲ")]
                if bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬᔳ")] == bstack11l11l_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡌࡒ࡛ࡇࡌࡊࡆࡢࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࠨᔴ"):
                    logger.error(error_message)
                elif bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᔵ")] == bstack11l11l_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠫᔶ"):
                    logger.info(error_message)
                elif bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔷ")] == bstack11l11l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡓࡅࡍࡢࡈࡊࡖࡒࡆࡅࡄࡘࡊࡊࠧᔸ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l11l_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᔹ"))
            return [None, None, None]
        bstack1lll1ll1lll_opy_ = response.json()
        os.environ[bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᔺ")] = bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᔻ")]
        if cls.bstack111llllll_opy_(bstack1lll1l1lll1_opy_.get(bstack11l11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬᔼ"), bstack11l11l_opy_ (u"ࠬ࠭ᔽ"))) is True:
            logger.debug(bstack11l11l_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪᔾ"))
            os.environ[bstack11l11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ᔿ")] = bstack11l11l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᕀ")
            if bstack1lll1ll1lll_opy_.get(bstack11l11l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᕁ")):
                os.environ[bstack11l11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᕂ")] = bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠫ࡯ࡽࡴࠨᕃ")]
                os.environ[bstack11l11l_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩᕄ")] = json.dumps({
                    bstack11l11l_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨᕅ"): bstack11l1l11l11_opy_,
                    bstack11l11l_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩᕆ"): bstack11l1l1111l_opy_
                })
            if bstack1lll1ll1lll_opy_.get(bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᕇ")):
                os.environ[bstack11l11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨᕈ")] = bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᕉ")]
            if bstack1lll1ll1lll_opy_.get(bstack11l11l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᕊ")):
                os.environ[bstack11l11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᕋ")] = str(bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᕌ")])
        return [bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠧ࡫ࡹࡷࠫᕍ")], bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᕎ")], bstack1lll1ll1lll_opy_[bstack11l11l_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᕏ")]]
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack11l11l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᕐ")] == bstack11l11l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕑ") or os.environ[bstack11l11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᕒ")] == bstack11l11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᕓ"):
            print(bstack11l11l_opy_ (u"ࠧࡆ࡚ࡆࡉࡕ࡚ࡉࡐࡐࠣࡍࡓࠦࡳࡵࡱࡳࡆࡺ࡯࡬ࡥࡗࡳࡷࡹࡸࡥࡢ࡯ࠣࡖࡊࡗࡕࡆࡕࡗࠤ࡙ࡕࠠࡕࡇࡖࡘࠥࡕࡂࡔࡇࡕ࡚ࡆࡈࡉࡍࡋࡗ࡝ࠥࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᕔ"))
            return {
                bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᕕ"): bstack11l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᕖ"),
                bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᕗ"): bstack11l11l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᕘ")
            }
        else:
            cls.bstack1lllll1111l_opy_.shutdown()
            data = {
                bstack11l11l_opy_ (u"ࠬࡹࡴࡰࡲࡢࡸ࡮ࡳࡥࠨᕙ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack11l11l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᕚ"): cls.default_headers()
            }
            bstack111l1l1l1l_opy_ = bstack11l11l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨᕛ").format(os.environ[bstack11l11l_opy_ (u"ࠣࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠢᕜ")])
            bstack1lll1ll111l_opy_ = cls.request_url(bstack111l1l1l1l_opy_)
            response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠩࡓ࡙࡙࠭ᕝ"), bstack1lll1ll111l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l11l_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤᕞ"))
    @classmethod
    def bstack1l111ll1l1_opy_(cls):
        if cls.bstack1lllll1111l_opy_ is None:
            return
        cls.bstack1lllll1111l_opy_.shutdown()
    @classmethod
    def bstack1ll11ll1l1_opy_(cls):
        if cls.on():
            print(
                bstack11l11l_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᕟ").format(os.environ[bstack11l11l_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦᕠ")]))
    @classmethod
    def bstack1lll1llll1l_opy_(cls):
        if cls.bstack1lllll1111l_opy_ is not None:
            return
        cls.bstack1lllll1111l_opy_ = bstack1llll1lllll_opy_(cls.bstack1lll1ll11ll_opy_)
        cls.bstack1lllll1111l_opy_.start()
    @classmethod
    def bstack11lllll1ll_opy_(cls, bstack1l111l1ll1_opy_, bstack1lll1lll1l1_opy_=bstack11l11l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᕡ")):
        if not cls.on():
            return
        bstack11l1lllll_opy_ = bstack1l111l1ll1_opy_[bstack11l11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᕢ")]
        bstack1llll11111l_opy_ = {
            bstack11l11l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᕣ"): bstack11l11l_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕤ"),
            bstack11l11l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᕥ"): bstack11l11l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕦ"),
            bstack11l11l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᕧ"): bstack11l11l_opy_ (u"࠭ࡔࡦࡵࡷࡣࡘࡱࡩࡱࡲࡨࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᕨ"),
            bstack11l11l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᕩ"): bstack11l11l_opy_ (u"ࠨࡎࡲ࡫ࡤ࡛ࡰ࡭ࡱࡤࡨࠬᕪ"),
            bstack11l11l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᕫ"): bstack11l11l_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡕࡷࡥࡷࡺ࡟ࡖࡲ࡯ࡳࡦࡪࠧᕬ"),
            bstack11l11l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᕭ"): bstack11l11l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡉࡳࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᕮ"),
            bstack11l11l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᕯ"): bstack11l11l_opy_ (u"ࠧࡄࡄࡗࡣ࡚ࡶ࡬ࡰࡣࡧࠫᕰ")
        }.get(bstack11l1lllll_opy_)
        if bstack1lll1lll1l1_opy_ == bstack11l11l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᕱ"):
            cls.bstack1lll1llll1l_opy_()
            cls.bstack1lllll1111l_opy_.add(bstack1l111l1ll1_opy_)
        elif bstack1lll1lll1l1_opy_ == bstack11l11l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᕲ"):
            cls.bstack1lll1ll11ll_opy_([bstack1l111l1ll1_opy_], bstack1lll1lll1l1_opy_)
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def bstack1lll1ll11ll_opy_(cls, bstack1l111l1ll1_opy_, bstack1lll1lll1l1_opy_=bstack11l11l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᕳ")):
        config = {
            bstack11l11l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᕴ"): cls.default_headers()
        }
        response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠬࡖࡏࡔࡖࠪᕵ"), cls.request_url(bstack1lll1lll1l1_opy_), bstack1l111l1ll1_opy_, config)
        bstack11l1l1l11l_opy_ = response.json()
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def bstack111111lll_opy_(cls, bstack1l11111ll1_opy_):
        bstack1lll1ll1ll1_opy_ = []
        for log in bstack1l11111ll1_opy_:
            bstack1lll1lll11l_opy_ = {
                bstack11l11l_opy_ (u"࠭࡫ࡪࡰࡧࠫᕶ"): bstack11l11l_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩᕷ"),
                bstack11l11l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕸ"): log[bstack11l11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᕹ")],
                bstack11l11l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᕺ"): log[bstack11l11l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᕻ")],
                bstack11l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬᕼ"): {},
                bstack11l11l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕽ"): log[bstack11l11l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᕾ")],
            }
            if bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕿ") in log:
                bstack1lll1lll11l_opy_[bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖀ")] = log[bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖁ")]
            elif bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖂ") in log:
                bstack1lll1lll11l_opy_[bstack11l11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖃ")] = log[bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖄ")]
            bstack1lll1ll1ll1_opy_.append(bstack1lll1lll11l_opy_)
        cls.bstack11lllll1ll_opy_({
            bstack11l11l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖅ"): bstack11l11l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᖆ"),
            bstack11l11l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᖇ"): bstack1lll1ll1ll1_opy_
        })
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def bstack1lll1ll1l11_opy_(cls, steps):
        bstack1lll1llllll_opy_ = []
        for step in steps:
            bstack1lll1ll11l1_opy_ = {
                bstack11l11l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᖈ"): bstack11l11l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᖉ"),
                bstack11l11l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᖊ"): step[bstack11l11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᖋ")],
                bstack11l11l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᖌ"): step[bstack11l11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᖍ")],
                bstack11l11l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖎ"): step[bstack11l11l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖏ")],
                bstack11l11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᖐ"): step[bstack11l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᖑ")]
            }
            if bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖒ") in step:
                bstack1lll1ll11l1_opy_[bstack11l11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖓ")] = step[bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖔ")]
            elif bstack11l11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖕ") in step:
                bstack1lll1ll11l1_opy_[bstack11l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖖ")] = step[bstack11l11l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖗ")]
            bstack1lll1llllll_opy_.append(bstack1lll1ll11l1_opy_)
        cls.bstack11lllll1ll_opy_({
            bstack11l11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᖘ"): bstack11l11l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᖙ"),
            bstack11l11l_opy_ (u"ࠧ࡭ࡱࡪࡷࠬᖚ"): bstack1lll1llllll_opy_
        })
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def bstack1l1lllll11_opy_(cls, screenshot):
        cls.bstack11lllll1ll_opy_({
            bstack11l11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᖛ"): bstack11l11l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᖜ"),
            bstack11l11l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᖝ"): [{
                bstack11l11l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᖞ"): bstack11l11l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧᖟ"),
                bstack11l11l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᖠ"): datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"࡛ࠧࠩᖡ"),
                bstack11l11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖢ"): screenshot[bstack11l11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨᖣ")],
                bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖤ"): screenshot[bstack11l11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖥ")]
            }]
        }, bstack1lll1lll1l1_opy_=bstack11l11l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᖦ"))
    @classmethod
    @bstack1l1111l11l_opy_(class_method=True)
    def bstack1llllll1l1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11lllll1ll_opy_({
            bstack11l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᖧ"): bstack11l11l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᖨ"),
            bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᖩ"): {
                bstack11l11l_opy_ (u"ࠤࡸࡹ࡮ࡪࠢᖪ"): cls.current_test_uuid(),
                bstack11l11l_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤᖫ"): cls.bstack11llll1l11_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack11l11l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᖬ"), None) is None or os.environ[bstack11l11l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᖭ")] == bstack11l11l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᖮ"):
            return False
        return True
    @classmethod
    def bstack111llllll_opy_(cls, framework=bstack11l11l_opy_ (u"ࠢࠣᖯ")):
        if framework not in bstack11l111l111_opy_:
            return False
        bstack1lll1lll1ll_opy_ = not bstack111l1l1l1_opy_()
        return bstack1l1ll111l1_opy_(cls.bs_config.get(bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᖰ"), bstack1lll1lll1ll_opy_))
    @staticmethod
    def request_url(url):
        return bstack11l11l_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᖱ").format(bstack1lll1l1llll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack11l11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᖲ"): bstack11l11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᖳ"),
            bstack11l11l_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨᖴ"): bstack11l11l_opy_ (u"࠭ࡴࡳࡷࡨࠫᖵ")
        }
        if os.environ.get(bstack11l11l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᖶ"), None):
            headers[bstack11l11l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᖷ")] = bstack11l11l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᖸ").format(os.environ[bstack11l11l_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦᖹ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖺ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖻ"), None)
    @staticmethod
    def bstack1l111lll11_opy_():
        if getattr(threading.current_thread(), bstack11l11l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖼ"), None):
            return {
                bstack11l11l_opy_ (u"ࠧࡵࡻࡳࡩࠬᖽ"): bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᖾ"),
                bstack11l11l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖿ"): getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᗀ"), None)
            }
        if getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᗁ"), None):
            return {
                bstack11l11l_opy_ (u"ࠬࡺࡹࡱࡧࠪᗂ"): bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᗃ"),
                bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᗄ"): getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᗅ"), None)
            }
        return None
    @staticmethod
    def bstack11llll1l11_opy_(driver):
        return {
            bstack111lll11l1_opy_(): bstack11l1111l11_opy_(driver)
        }
    @staticmethod
    def bstack1lll1ll1l1l_opy_(exception_info, report):
        return [{bstack11l11l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᗆ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1l111l_opy_(typename):
        if bstack11l11l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᗇ") in typename:
            return bstack11l11l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᗈ")
        return bstack11l11l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᗉ")
    @staticmethod
    def bstack1lll1lllll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1l1ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l11l111ll_opy_(test, hook_name=None):
        bstack1llll111111_opy_ = test.parent
        if hook_name in [bstack11l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᗊ"), bstack11l11l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᗋ"), bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᗌ"), bstack11l11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᗍ")]:
            bstack1llll111111_opy_ = test
        scope = []
        while bstack1llll111111_opy_ is not None:
            scope.append(bstack1llll111111_opy_.name)
            bstack1llll111111_opy_ = bstack1llll111111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1llll11_opy_(hook_type):
        if hook_type == bstack11l11l_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣᗎ"):
            return bstack11l11l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣᗏ")
        elif hook_type == bstack11l11l_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤᗐ"):
            return bstack11l11l_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨᗑ")
    @staticmethod
    def bstack1lll1lll111_opy_(bstack1l1l111ll_opy_):
        try:
            if not bstack1ll1l1ll1l_opy_.on():
                return bstack1l1l111ll_opy_
            if os.environ.get(bstack11l11l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧᗒ"), None) == bstack11l11l_opy_ (u"ࠣࡶࡵࡹࡪࠨᗓ"):
                tests = os.environ.get(bstack11l11l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨᗔ"), None)
                if tests is None or tests == bstack11l11l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᗕ"):
                    return bstack1l1l111ll_opy_
                bstack1l1l111ll_opy_ = tests.split(bstack11l11l_opy_ (u"ࠫ࠱࠭ᗖ"))
                return bstack1l1l111ll_opy_
        except Exception as exc:
            print(bstack11l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨᗗ"), str(exc))
        return bstack1l1l111ll_opy_
    @classmethod
    def bstack1l111l1111_opy_(cls, event: str, bstack1l111l1ll1_opy_: bstack1l111lll1l_opy_):
        bstack11llll1lll_opy_ = {
            bstack11l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᗘ"): event,
            bstack1l111l1ll1_opy_.bstack1l111111l1_opy_(): bstack1l111l1ll1_opy_.bstack11lllll11l_opy_(event)
        }
        bstack1ll1l1ll1l_opy_.bstack11lllll1ll_opy_(bstack11llll1lll_opy_)