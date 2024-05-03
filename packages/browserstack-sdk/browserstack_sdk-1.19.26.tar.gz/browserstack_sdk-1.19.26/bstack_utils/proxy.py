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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11ll11llll_opy_
def bstack11ll11ll1l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack11ll1l1111_opy_(bstack11ll11l1l1_opy_, bstack11ll11lll1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack11ll11l1l1_opy_):
        with open(bstack11ll11l1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11ll11ll1l_opy_(bstack11ll11l1l1_opy_):
        pac = get_pac(url=bstack11ll11l1l1_opy_)
    else:
        raise Exception(bstack11l11l_opy_ (u"ࠫࡕࡧࡣࠡࡨ࡬ࡰࡪࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺ࠺ࠡࡽࢀࠫี").format(bstack11ll11l1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11l11l_opy_ (u"ࠧ࠾࠮࠹࠰࠻࠲࠽ࠨึ"), 80))
        bstack11ll11l1ll_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11ll11l1ll_opy_ = bstack11l11l_opy_ (u"࠭࠰࠯࠲࠱࠴࠳࠶ࠧื")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11ll11lll1_opy_, bstack11ll11l1ll_opy_)
    return proxy_url
def bstack111l1111l_opy_(config):
    return bstack11l11l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻุࠪ") in config or bstack11l11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽูࠬ") in config
def bstack1l1l11111_opy_(config):
    if not bstack111l1111l_opy_(config):
        return
    if config.get(bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽฺࠬ")):
        return config.get(bstack11l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭฻"))
    if config.get(bstack11l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ฼")):
        return config.get(bstack11l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ฽"))
def bstack1ll111l1l_opy_(config, bstack11ll11lll1_opy_):
    proxy = bstack1l1l11111_opy_(config)
    proxies = {}
    if config.get(bstack11l11l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩ฾")) or config.get(bstack11l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫ฿")):
        if proxy.endswith(bstack11l11l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭เ")):
            proxies = bstack1l1l1l1l1_opy_(proxy, bstack11ll11lll1_opy_)
        else:
            proxies = {
                bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨแ"): proxy
            }
    return proxies
def bstack1l1l1l1l1_opy_(bstack11ll11l1l1_opy_, bstack11ll11lll1_opy_):
    proxies = {}
    global bstack11ll11ll11_opy_
    if bstack11l11l_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭โ") in globals():
        return bstack11ll11ll11_opy_
    try:
        proxy = bstack11ll1l1111_opy_(bstack11ll11l1l1_opy_, bstack11ll11lll1_opy_)
        if bstack11l11l_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦใ") in proxy:
            proxies = {}
        elif bstack11l11l_opy_ (u"ࠧࡎࡔࡕࡒࠥไ") in proxy or bstack11l11l_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧๅ") in proxy or bstack11l11l_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨๆ") in proxy:
            bstack11ll11l11l_opy_ = proxy.split(bstack11l11l_opy_ (u"ࠣࠢࠥ็"))
            if bstack11l11l_opy_ (u"ࠤ࠽࠳࠴ࠨ่") in bstack11l11l_opy_ (u"้ࠥࠦ").join(bstack11ll11l11l_opy_[1:]):
                proxies = {
                    bstack11l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ๊ࠪ"): bstack11l11l_opy_ (u"ࠧࠨ๋").join(bstack11ll11l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ์"): str(bstack11ll11l11l_opy_[0]).lower() + bstack11l11l_opy_ (u"ࠢ࠻࠱࠲ࠦํ") + bstack11l11l_opy_ (u"ࠣࠤ๎").join(bstack11ll11l11l_opy_[1:])
                }
        elif bstack11l11l_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣ๏") in proxy:
            bstack11ll11l11l_opy_ = proxy.split(bstack11l11l_opy_ (u"ࠥࠤࠧ๐"))
            if bstack11l11l_opy_ (u"ࠦ࠿࠵࠯ࠣ๑") in bstack11l11l_opy_ (u"ࠧࠨ๒").join(bstack11ll11l11l_opy_[1:]):
                proxies = {
                    bstack11l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬ๓"): bstack11l11l_opy_ (u"ࠢࠣ๔").join(bstack11ll11l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11l11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧ๕"): bstack11l11l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥ๖") + bstack11l11l_opy_ (u"ࠥࠦ๗").join(bstack11ll11l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11l11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪ๘"): proxy
            }
    except Exception as e:
        print(bstack11l11l_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ๙"), bstack11ll11llll_opy_.format(bstack11ll11l1l1_opy_, str(e)))
    bstack11ll11ll11_opy_ = proxies
    return proxies