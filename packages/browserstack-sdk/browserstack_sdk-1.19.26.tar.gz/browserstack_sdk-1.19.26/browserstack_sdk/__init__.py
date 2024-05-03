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
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1111llll1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l11l111l_opy_ import bstack1l1lll1l1_opy_
import time
import requests
def bstack1l11l1l1l_opy_():
  global CONFIG
  headers = {
        bstack11l11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11l11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1ll111l1l_opy_(CONFIG, bstack1lll1lllll_opy_)
  try:
    response = requests.get(bstack1lll1lllll_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1llll11_opy_ = response.json()[bstack11l11l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1ll1l11l_opy_.format(response.json()))
      return bstack1l1llll11_opy_
    else:
      logger.debug(bstack11l1ll1l1_opy_.format(bstack11l11l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack11l1ll1l1_opy_.format(e))
def bstack1ll111llll_opy_(hub_url):
  global CONFIG
  url = bstack11l11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11l11l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11l11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11l11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1ll111l1l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1l11ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack111l1l11l_opy_.format(hub_url, e))
def bstack1ll1ll1lll_opy_():
  try:
    global bstack1l11ll1111_opy_
    bstack1l1llll11_opy_ = bstack1l11l1l1l_opy_()
    bstack1l111lll_opy_ = []
    results = []
    for bstack1lll111lll_opy_ in bstack1l1llll11_opy_:
      bstack1l111lll_opy_.append(bstack111l11l11_opy_(target=bstack1ll111llll_opy_,args=(bstack1lll111lll_opy_,)))
    for t in bstack1l111lll_opy_:
      t.start()
    for t in bstack1l111lll_opy_:
      results.append(t.join())
    bstack11llllll1_opy_ = {}
    for item in results:
      hub_url = item[bstack11l11l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11l11l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11llllll1_opy_[hub_url] = latency
    bstack111l1ll1_opy_ = min(bstack11llllll1_opy_, key= lambda x: bstack11llllll1_opy_[x])
    bstack1l11ll1111_opy_ = bstack111l1ll1_opy_
    logger.debug(bstack1lllllllll_opy_.format(bstack111l1ll1_opy_))
  except Exception as e:
    logger.debug(bstack1l11l11lll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack111ll1l1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l1l11l1_opy_, bstack1llll11l1_opy_, bstack1ll1llll1_opy_, bstack111111ll_opy_, bstack111ll11l1_opy_, \
  Notset, bstack1llll1ll1l_opy_, \
  bstack1lllll11ll_opy_, bstack1l1111111_opy_, bstack1ll111lll_opy_, bstack1llllllll1_opy_, bstack1111ll1l_opy_, bstack1llll11l_opy_, \
  bstack111l1l1l1_opy_, \
  bstack1l11lll111_opy_, bstack11l1llll1_opy_, bstack1l1lll11l_opy_, bstack1l11l11l1_opy_, \
  bstack1l1ll11111_opy_, bstack1l11l1l1_opy_, bstack1l1ll111l1_opy_
from bstack_utils.bstack11lll111_opy_ import bstack1ll1l1111l_opy_
from bstack_utils.bstack1ll1l1l1ll_opy_ import bstack1llllllll_opy_
from bstack_utils.bstack1l1lllll1l_opy_ import bstack1ll1l11l1_opy_, bstack1l11ll1l11_opy_
from bstack_utils.bstack1lll1111_opy_ import bstack1ll1l1ll1l_opy_
from bstack_utils.bstack1l1l1ll1_opy_ import bstack1l1l1ll1_opy_
from bstack_utils.proxy import bstack1l1l1l1l1_opy_, bstack1ll111l1l_opy_, bstack1l1l11111_opy_, bstack111l1111l_opy_
import bstack_utils.bstack1llll11l1l_opy_ as bstack1lll1ll11_opy_
from browserstack_sdk.bstack11l111l1l_opy_ import *
from browserstack_sdk.bstack1lll111ll_opy_ import *
from bstack_utils.bstack1lll1111l_opy_ import bstack11ll1111_opy_
bstack11ll111ll_opy_ = bstack11l11l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack11111l1l_opy_ = bstack11l11l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack11l1l1l11_opy_ = None
CONFIG = {}
bstack11111llll_opy_ = {}
bstack1l11l1l11_opy_ = {}
bstack1ll1111ll1_opy_ = None
bstack1lll1lll1_opy_ = None
bstack1lll111l1_opy_ = None
bstack1l11llll1l_opy_ = -1
bstack1ll11llll1_opy_ = 0
bstack11111l1ll_opy_ = bstack1l11l1ll_opy_
bstack11llll1ll_opy_ = 1
bstack1lll1l1l1l_opy_ = False
bstack11111lll_opy_ = False
bstack1l1l11lll_opy_ = bstack11l11l_opy_ (u"ࠨࠩࢂ")
bstack1l11ll1ll1_opy_ = bstack11l11l_opy_ (u"ࠩࠪࢃ")
bstack11l111ll_opy_ = False
bstack1llllll1l_opy_ = True
bstack11l111lll_opy_ = bstack11l11l_opy_ (u"ࠪࠫࢄ")
bstack1ll1111lll_opy_ = []
bstack1l11ll1111_opy_ = bstack11l11l_opy_ (u"ࠫࠬࢅ")
bstack1ll1l111l_opy_ = False
bstack1llll11lll_opy_ = None
bstack1111l1ll1_opy_ = None
bstack11l111111_opy_ = None
bstack1ll1ll111l_opy_ = -1
bstack1llll1ll_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠬࢄࠧࢆ")), bstack11l11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack11l11l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack11l1lll1l_opy_ = 0
bstack1ll1lll11_opy_ = 0
bstack111lll1l1_opy_ = []
bstack11l1ll11l_opy_ = []
bstack1l11ll11l1_opy_ = []
bstack1lll111ll1_opy_ = []
bstack1l1111l11_opy_ = bstack11l11l_opy_ (u"ࠨࠩࢉ")
bstack1l1lll11l1_opy_ = bstack11l11l_opy_ (u"ࠩࠪࢊ")
bstack1111l1lll_opy_ = False
bstack1111l111l_opy_ = False
bstack1lll1l11_opy_ = {}
bstack1l11l1ll1l_opy_ = None
bstack1lll11111l_opy_ = None
bstack11111ll1l_opy_ = None
bstack1lll11ll1_opy_ = None
bstack11lll1l1_opy_ = None
bstack1l1ll11l11_opy_ = None
bstack1l1l1l1l_opy_ = None
bstack1l11lll1ll_opy_ = None
bstack11l11l111_opy_ = None
bstack1l11llllll_opy_ = None
bstack1l1l1111_opy_ = None
bstack1ll1ll11ll_opy_ = None
bstack1lll1l1ll1_opy_ = None
bstack1ll11l1ll_opy_ = None
bstack1lll11l1l1_opy_ = None
bstack11ll1l11l_opy_ = None
bstack1111l11l_opy_ = None
bstack111ll111l_opy_ = None
bstack111llll11_opy_ = None
bstack1l11lll11l_opy_ = None
bstack1ll1l1ll_opy_ = None
bstack1l1ll1l111_opy_ = False
bstack1ll1l11l1l_opy_ = bstack11l11l_opy_ (u"ࠥࠦࢋ")
logger = bstack111ll1l1_opy_.get_logger(__name__, bstack11111l1ll_opy_)
bstack111l11111_opy_ = Config.bstack1l11l1111_opy_()
percy = bstack11l11lll_opy_()
bstack11lll1l1l_opy_ = bstack1l1lll1l1_opy_()
def bstack1ll11ll1l_opy_():
  global CONFIG
  global bstack1111l1lll_opy_
  global bstack111l11111_opy_
  bstack1l1ll1111l_opy_ = bstack1l1l1lll1l_opy_(CONFIG)
  if (bstack11l11l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1l1ll1111l_opy_ and str(bstack1l1ll1111l_opy_[bstack11l11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack11l11l_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
    bstack1111l1lll_opy_ = True
  bstack111l11111_opy_.bstack1l111l11l_opy_(bstack1l1ll1111l_opy_.get(bstack11l11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
def bstack11lll1lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1ll1l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack11l1l11l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11l11l_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack11l11l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack11l111lll_opy_
      bstack11l111lll_opy_ += bstack11l11l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack111l1llll_opy_ = re.compile(bstack11l11l_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1ll1l11ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack111l1llll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11l11l_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack11l11l_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1l1l1l11l1_opy_():
  bstack1l1lll1ll1_opy_ = bstack11l1l11l_opy_()
  if bstack1l1lll1ll1_opy_ and os.path.exists(os.path.abspath(bstack1l1lll1ll1_opy_)):
    fileName = bstack1l1lll1ll1_opy_
  if bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack11l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack11l11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack11l_opy_ = os.path.abspath(fileName)
  else:
    bstack11l_opy_ = bstack11l11l_opy_ (u"࢛ࠬ࠭")
  bstack1l1l11ll11_opy_ = os.getcwd()
  bstack1lll11l111_opy_ = bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l11l1l1l1_opy_ = bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack11l_opy_)) and bstack1l1l11ll11_opy_ != bstack11l11l_opy_ (u"ࠣࠤ࢞"):
    bstack11l_opy_ = os.path.join(bstack1l1l11ll11_opy_, bstack1lll11l111_opy_)
    if not os.path.exists(bstack11l_opy_):
      bstack11l_opy_ = os.path.join(bstack1l1l11ll11_opy_, bstack1l11l1l1l1_opy_)
    if bstack1l1l11ll11_opy_ != os.path.dirname(bstack1l1l11ll11_opy_):
      bstack1l1l11ll11_opy_ = os.path.dirname(bstack1l1l11ll11_opy_)
    else:
      bstack1l1l11ll11_opy_ = bstack11l11l_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack11l_opy_):
    bstack11l1l1lll_opy_(
      bstack1l1lllll_opy_.format(os.getcwd()))
  try:
    with open(bstack11l_opy_, bstack11l11l_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack11l11l_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack111l1llll_opy_)
      yaml.add_constructor(bstack11l11l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1ll1l11ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11l_opy_, bstack11l11l_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l1l1lll_opy_(bstack11l1lll1_opy_.format(str(exc)))
def bstack1l111ll1_opy_(config):
  bstack1l1l1ll11l_opy_ = bstack1lll11lll1_opy_(config)
  for option in list(bstack1l1l1ll11l_opy_):
    if option.lower() in bstack1l11ll1l1l_opy_ and option != bstack1l11ll1l1l_opy_[option.lower()]:
      bstack1l1l1ll11l_opy_[bstack1l11ll1l1l_opy_[option.lower()]] = bstack1l1l1ll11l_opy_[option]
      del bstack1l1l1ll11l_opy_[option]
  return config
def bstack111l111ll_opy_():
  global bstack1l11l1l11_opy_
  for key, bstack1ll1l1ll1_opy_ in bstack1ll11l1l11_opy_.items():
    if isinstance(bstack1ll1l1ll1_opy_, list):
      for var in bstack1ll1l1ll1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l11l1l11_opy_[key] = os.environ[var]
          break
    elif bstack1ll1l1ll1_opy_ in os.environ and os.environ[bstack1ll1l1ll1_opy_] and str(os.environ[bstack1ll1l1ll1_opy_]).strip():
      bstack1l11l1l11_opy_[key] = os.environ[bstack1ll1l1ll1_opy_]
  if bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1l11l1l11_opy_[bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1l11l1l11_opy_[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack11l11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1lll1ll1l1_opy_():
  global bstack11111llll_opy_
  global bstack11l111lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11l11l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack11111llll_opy_[bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack11111llll_opy_[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack11l11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l1l1lll11_opy_ in bstack11l1l11ll_opy_.items():
    if isinstance(bstack1l1l1lll11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l1l1lll11_opy_:
          if idx < len(sys.argv) and bstack11l11l_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack11111llll_opy_:
            bstack11111llll_opy_[key] = sys.argv[idx + 1]
            bstack11l111lll_opy_ += bstack11l11l_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack11l11l_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11l11l_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1l1l1lll11_opy_.lower() == val.lower() and not key in bstack11111llll_opy_:
          bstack11111llll_opy_[key] = sys.argv[idx + 1]
          bstack11l111lll_opy_ += bstack11l11l_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1l1l1lll11_opy_ + bstack11l11l_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1111111l1_opy_(config):
  bstack1ll11l1l_opy_ = config.keys()
  for bstack1l1lll1l_opy_, bstack111lll1ll_opy_ in bstack1l1l1111l1_opy_.items():
    if bstack111lll1ll_opy_ in bstack1ll11l1l_opy_:
      config[bstack1l1lll1l_opy_] = config[bstack111lll1ll_opy_]
      del config[bstack111lll1ll_opy_]
  for bstack1l1lll1l_opy_, bstack111lll1ll_opy_ in bstack1l1ll1ll_opy_.items():
    if isinstance(bstack111lll1ll_opy_, list):
      for bstack11ll1l1l_opy_ in bstack111lll1ll_opy_:
        if bstack11ll1l1l_opy_ in bstack1ll11l1l_opy_:
          config[bstack1l1lll1l_opy_] = config[bstack11ll1l1l_opy_]
          del config[bstack11ll1l1l_opy_]
          break
    elif bstack111lll1ll_opy_ in bstack1ll11l1l_opy_:
      config[bstack1l1lll1l_opy_] = config[bstack111lll1ll_opy_]
      del config[bstack111lll1ll_opy_]
  for bstack11ll1l1l_opy_ in list(config):
    for bstack1lll1l1l_opy_ in bstack1lll1llll1_opy_:
      if bstack11ll1l1l_opy_.lower() == bstack1lll1l1l_opy_.lower() and bstack11ll1l1l_opy_ != bstack1lll1l1l_opy_:
        config[bstack1lll1l1l_opy_] = config[bstack11ll1l1l_opy_]
        del config[bstack11ll1l1l_opy_]
  bstack1l1ll1l1l_opy_ = []
  if bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack1l1ll1l1l_opy_ = config[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack1l1ll1l1l_opy_:
    for bstack11ll1l1l_opy_ in list(platform):
      for bstack1lll1l1l_opy_ in bstack1lll1llll1_opy_:
        if bstack11ll1l1l_opy_.lower() == bstack1lll1l1l_opy_.lower() and bstack11ll1l1l_opy_ != bstack1lll1l1l_opy_:
          platform[bstack1lll1l1l_opy_] = platform[bstack11ll1l1l_opy_]
          del platform[bstack11ll1l1l_opy_]
  for bstack1l1lll1l_opy_, bstack111lll1ll_opy_ in bstack1l1ll1ll_opy_.items():
    for platform in bstack1l1ll1l1l_opy_:
      if isinstance(bstack111lll1ll_opy_, list):
        for bstack11ll1l1l_opy_ in bstack111lll1ll_opy_:
          if bstack11ll1l1l_opy_ in platform:
            platform[bstack1l1lll1l_opy_] = platform[bstack11ll1l1l_opy_]
            del platform[bstack11ll1l1l_opy_]
            break
      elif bstack111lll1ll_opy_ in platform:
        platform[bstack1l1lll1l_opy_] = platform[bstack111lll1ll_opy_]
        del platform[bstack111lll1ll_opy_]
  for bstack1llll1l1l_opy_ in bstack1l1ll1ll11_opy_:
    if bstack1llll1l1l_opy_ in config:
      if not bstack1l1ll1ll11_opy_[bstack1llll1l1l_opy_] in config:
        config[bstack1l1ll1ll11_opy_[bstack1llll1l1l_opy_]] = {}
      config[bstack1l1ll1ll11_opy_[bstack1llll1l1l_opy_]].update(config[bstack1llll1l1l_opy_])
      del config[bstack1llll1l1l_opy_]
  for platform in bstack1l1ll1l1l_opy_:
    for bstack1llll1l1l_opy_ in bstack1l1ll1ll11_opy_:
      if bstack1llll1l1l_opy_ in list(platform):
        if not bstack1l1ll1ll11_opy_[bstack1llll1l1l_opy_] in platform:
          platform[bstack1l1ll1ll11_opy_[bstack1llll1l1l_opy_]] = {}
        platform[bstack1l1ll1ll11_opy_[bstack1llll1l1l_opy_]].update(platform[bstack1llll1l1l_opy_])
        del platform[bstack1llll1l1l_opy_]
  config = bstack1l111ll1_opy_(config)
  return config
def bstack11lll1111_opy_(config):
  global bstack1l11ll1ll1_opy_
  if bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack11l11l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack11l11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack1lllll11_opy_ = datetime.datetime.now()
      bstack1lllll1ll_opy_ = bstack1lllll11_opy_.strftime(bstack11l11l_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1lll111l1l_opy_ = bstack11l11l_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11l11l_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1lllll1ll_opy_, hostname, bstack1lll111l1l_opy_)
      config[bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack11l11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack1l11ll1ll1_opy_ = config[bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack11l11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack1l1ll11ll1_opy_():
  bstack11l1111ll_opy_ =  bstack1llllllll1_opy_()[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack11l1111ll_opy_ if bstack11l1111ll_opy_ else -1
def bstack1l1l11llll_opy_(bstack11l1111ll_opy_):
  global CONFIG
  if not bstack11l11l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack11l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack11l11l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack11l1111ll_opy_)
  )
def bstack1ll1l1lll1_opy_():
  global CONFIG
  if not bstack11l11l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack1lllll11_opy_ = datetime.datetime.now()
  bstack1lllll1ll_opy_ = bstack1lllll11_opy_.strftime(bstack11l11l_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack11l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack11l11l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack1lllll1ll_opy_
  )
def bstack1llllll11_opy_():
  global CONFIG
  if bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack11l11l_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack11l11l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack1ll1l1lll1_opy_()
    os.environ[bstack11l11l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack11l11l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack11l1111ll_opy_ = bstack11l11l_opy_ (u"࠭ࠧࣛ")
  bstack1ll1ll11l_opy_ = bstack1l1ll11ll1_opy_()
  if bstack1ll1ll11l_opy_ != -1:
    bstack11l1111ll_opy_ = bstack11l11l_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack1ll1ll11l_opy_)
  if bstack11l1111ll_opy_ == bstack11l11l_opy_ (u"ࠨࠩࣝ"):
    bstack1l1l111lll_opy_ = bstack1llll1l1l1_opy_(CONFIG[bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack1l1l111lll_opy_ != -1:
      bstack11l1111ll_opy_ = str(bstack1l1l111lll_opy_)
  if bstack11l1111ll_opy_:
    bstack1l1l11llll_opy_(bstack11l1111ll_opy_)
    os.environ[bstack11l11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack1ll1ll1l_opy_(bstack11lll1ll1_opy_, bstack11111ll1_opy_, path):
  bstack1llllll111_opy_ = {
    bstack11l11l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack11111ll1_opy_
  }
  if os.path.exists(path):
    bstack1l11l1l11l_opy_ = json.load(open(path, bstack11l11l_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack1l11l1l11l_opy_ = {}
  bstack1l11l1l11l_opy_[bstack11lll1ll1_opy_] = bstack1llllll111_opy_
  with open(path, bstack11l11l_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack1l11l1l11l_opy_, outfile)
def bstack1llll1l1l1_opy_(bstack11lll1ll1_opy_):
  bstack11lll1ll1_opy_ = str(bstack11lll1ll1_opy_)
  bstack11lllll1_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠨࢀࠪࣤ")), bstack11l11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack11lllll1_opy_):
      os.makedirs(bstack11lllll1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠪࢂࣦࠬ")), bstack11l11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack11l11l_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11l11l_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack11l11l_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11l11l_opy_ (u"ࠨࡴࠪ࣫")) as bstack1l1l111l1_opy_:
      bstack1lll1l1ll_opy_ = json.load(bstack1l1l111l1_opy_)
    if bstack11lll1ll1_opy_ in bstack1lll1l1ll_opy_:
      bstack11l11l1l_opy_ = bstack1lll1l1ll_opy_[bstack11lll1ll1_opy_][bstack11l11l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack1ll1lll1ll_opy_ = int(bstack11l11l1l_opy_) + 1
      bstack1ll1ll1l_opy_(bstack11lll1ll1_opy_, bstack1ll1lll1ll_opy_, file_path)
      return bstack1ll1lll1ll_opy_
    else:
      bstack1ll1ll1l_opy_(bstack11lll1ll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1ll1l11_opy_.format(str(e)))
    return -1
def bstack1l1l1l1111_opy_(config):
  if not config[bstack11l11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack11l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack1l1l11l1ll_opy_(config, index=0):
  global bstack11l111ll_opy_
  bstack1l1l1l11_opy_ = {}
  caps = bstack1111l1l1l_opy_ + bstack1lllll111l_opy_
  if bstack11l111ll_opy_:
    caps += bstack1l1ll1l1l1_opy_
  for key in config:
    if key in caps + [bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack1l1l1l11_opy_[key] = config[key]
  if bstack11l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack1ll1lll11l_opy_ in config[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack1ll1lll11l_opy_ in caps + [bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack1l1l1l11_opy_[bstack1ll1lll11l_opy_] = config[bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack1ll1lll11l_opy_]
  bstack1l1l1l11_opy_[bstack11l11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack11l11l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack1l1l1l11_opy_:
    del (bstack1l1l1l11_opy_[bstack11l11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack1l1l1l11_opy_
def bstack1111lll11_opy_(config):
  global bstack11l111ll_opy_
  bstack1ll1lll111_opy_ = {}
  caps = bstack1lllll111l_opy_
  if bstack11l111ll_opy_:
    caps += bstack1l1ll1l1l1_opy_
  for key in caps:
    if key in config:
      bstack1ll1lll111_opy_[key] = config[key]
  return bstack1ll1lll111_opy_
def bstack1l1111ll1_opy_(bstack1l1l1l11_opy_, bstack1ll1lll111_opy_):
  bstack1l1lllll1_opy_ = {}
  for key in bstack1l1l1l11_opy_.keys():
    if key in bstack1l1l1111l1_opy_:
      bstack1l1lllll1_opy_[bstack1l1l1111l1_opy_[key]] = bstack1l1l1l11_opy_[key]
    else:
      bstack1l1lllll1_opy_[key] = bstack1l1l1l11_opy_[key]
  for key in bstack1ll1lll111_opy_:
    if key in bstack1l1l1111l1_opy_:
      bstack1l1lllll1_opy_[bstack1l1l1111l1_opy_[key]] = bstack1ll1lll111_opy_[key]
    else:
      bstack1l1lllll1_opy_[key] = bstack1ll1lll111_opy_[key]
  return bstack1l1lllll1_opy_
def bstack1ll1l1111_opy_(config, index=0):
  global bstack11l111ll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1l1ll1ll1_opy_ = bstack11l1l11l1_opy_(bstack111l1l1ll_opy_, config, logger)
  bstack1ll1lll111_opy_ = bstack1111lll11_opy_(config)
  bstack1ll111l1l1_opy_ = bstack1lllll111l_opy_
  bstack1ll111l1l1_opy_ += bstack1ll1l1l11_opy_
  bstack1ll1lll111_opy_ = update(bstack1ll1lll111_opy_, bstack1l1ll1ll1_opy_)
  if bstack11l111ll_opy_:
    bstack1ll111l1l1_opy_ += bstack1l1ll1l1l1_opy_
  if bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack111l11l1_opy_ = bstack11l1l11l1_opy_(bstack111l1l1ll_opy_, config[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index], logger)
    bstack1ll111l1l1_opy_ += list(bstack111l11l1_opy_.keys())
    for bstack1l11lll1l_opy_ in bstack1ll111l1l1_opy_:
      if bstack1l11lll1l_opy_ in config[bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index]:
        if bstack1l11lll1l_opy_ == bstack11l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨअ"):
          try:
            bstack111l11l1_opy_[bstack1l11lll1l_opy_] = str(config[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack1l11lll1l_opy_] * 1.0)
          except:
            bstack111l11l1_opy_[bstack1l11lll1l_opy_] = str(config[bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1l11lll1l_opy_])
        else:
          bstack111l11l1_opy_[bstack1l11lll1l_opy_] = config[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1l11lll1l_opy_]
        del (config[bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l11lll1l_opy_])
    bstack1ll1lll111_opy_ = update(bstack1ll1lll111_opy_, bstack111l11l1_opy_)
  bstack1l1l1l11_opy_ = bstack1l1l11l1ll_opy_(config, index)
  for bstack11ll1l1l_opy_ in bstack1lllll111l_opy_ + [bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऊ"), bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऋ")] + list(bstack1l1ll1ll1_opy_.keys()):
    if bstack11ll1l1l_opy_ in bstack1l1l1l11_opy_:
      bstack1ll1lll111_opy_[bstack11ll1l1l_opy_] = bstack1l1l1l11_opy_[bstack11ll1l1l_opy_]
      del (bstack1l1l1l11_opy_[bstack11ll1l1l_opy_])
  if bstack1llll1ll1l_opy_(config):
    bstack1l1l1l11_opy_[bstack11l11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ऌ")] = True
    caps.update(bstack1ll1lll111_opy_)
    caps[bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨऍ")] = bstack1l1l1l11_opy_
  else:
    bstack1l1l1l11_opy_[bstack11l11l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨऎ")] = False
    caps.update(bstack1l1111ll1_opy_(bstack1l1l1l11_opy_, bstack1ll1lll111_opy_))
    if bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧए") in caps:
      caps[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫऐ")] = caps[bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")]
      del (caps[bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ")])
    if bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧओ") in caps:
      caps[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩऔ")] = caps[bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")]
      del (caps[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख")])
  return caps
def bstack11ll1l1l1_opy_():
  global bstack1l11ll1111_opy_
  if bstack1l1ll1l1_opy_() <= version.parse(bstack11l11l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪग")):
    if bstack1l11ll1111_opy_ != bstack11l11l_opy_ (u"ࠫࠬघ"):
      return bstack11l11l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨङ") + bstack1l11ll1111_opy_ + bstack11l11l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥच")
    return bstack1111l11l1_opy_
  if bstack1l11ll1111_opy_ != bstack11l11l_opy_ (u"ࠧࠨछ"):
    return bstack11l11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥज") + bstack1l11ll1111_opy_ + bstack11l11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥझ")
  return bstack1l11l11ll_opy_
def bstack11l1ll1l_opy_(options):
  return hasattr(options, bstack11l11l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫञ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11lll111l_opy_(options, bstack11llll1l1_opy_):
  for bstack11lll11l1_opy_ in bstack11llll1l1_opy_:
    if bstack11lll11l1_opy_ in [bstack11l11l_opy_ (u"ࠫࡦࡸࡧࡴࠩट"), bstack11l11l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩठ")]:
      continue
    if bstack11lll11l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11lll11l1_opy_] = update(options._experimental_options[bstack11lll11l1_opy_],
                                                         bstack11llll1l1_opy_[bstack11lll11l1_opy_])
    else:
      options.add_experimental_option(bstack11lll11l1_opy_, bstack11llll1l1_opy_[bstack11lll11l1_opy_])
  if bstack11l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫड") in bstack11llll1l1_opy_:
    for arg in bstack11llll1l1_opy_[bstack11l11l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")]:
      options.add_argument(arg)
    del (bstack11llll1l1_opy_[bstack11l11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण")])
  if bstack11l11l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त") in bstack11llll1l1_opy_:
    for ext in bstack11llll1l1_opy_[bstack11l11l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")]:
      options.add_extension(ext)
    del (bstack11llll1l1_opy_[bstack11l11l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद")])
def bstack1ll1l1l1_opy_(options, bstack111lll11_opy_):
  if bstack11l11l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध") in bstack111lll11_opy_:
    for bstack11111lll1_opy_ in bstack111lll11_opy_[bstack11l11l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")]:
      if bstack11111lll1_opy_ in options._preferences:
        options._preferences[bstack11111lll1_opy_] = update(options._preferences[bstack11111lll1_opy_], bstack111lll11_opy_[bstack11l11l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack11111lll1_opy_])
      else:
        options.set_preference(bstack11111lll1_opy_, bstack111lll11_opy_[bstack11l11l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")][bstack11111lll1_opy_])
  if bstack11l11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ") in bstack111lll11_opy_:
    for arg in bstack111lll11_opy_[bstack11l11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨब")]:
      options.add_argument(arg)
def bstack1lll11l1_opy_(options, bstack11ll1l111_opy_):
  if bstack11l11l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ") in bstack11ll1l111_opy_:
    options.use_webview(bool(bstack11ll1l111_opy_[bstack11l11l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭म")]))
  bstack11lll111l_opy_(options, bstack11ll1l111_opy_)
def bstack1lll1lll_opy_(options, bstack1llll1lll1_opy_):
  for bstack1ll11l1111_opy_ in bstack1llll1lll1_opy_:
    if bstack1ll11l1111_opy_ in [bstack11l11l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪय"), bstack11l11l_opy_ (u"ࠧࡢࡴࡪࡷࠬर")]:
      continue
    options.set_capability(bstack1ll11l1111_opy_, bstack1llll1lll1_opy_[bstack1ll11l1111_opy_])
  if bstack11l11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ") in bstack1llll1lll1_opy_:
    for arg in bstack1llll1lll1_opy_[bstack11l11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल")]:
      options.add_argument(arg)
  if bstack11l11l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ") in bstack1llll1lll1_opy_:
    options.bstack1l11l111_opy_(bool(bstack1llll1lll1_opy_[bstack11l11l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨऴ")]))
def bstack1l1111l1l_opy_(options, bstack1111llll_opy_):
  for bstack11l1l1ll_opy_ in bstack1111llll_opy_:
    if bstack11l1l1ll_opy_ in [bstack11l11l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩव"), bstack11l11l_opy_ (u"࠭ࡡࡳࡩࡶࠫश")]:
      continue
    options._options[bstack11l1l1ll_opy_] = bstack1111llll_opy_[bstack11l1l1ll_opy_]
  if bstack11l11l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष") in bstack1111llll_opy_:
    for bstack1l1ll11l1l_opy_ in bstack1111llll_opy_[bstack11l11l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")]:
      options.bstack1l11111ll_opy_(
        bstack1l1ll11l1l_opy_, bstack1111llll_opy_[bstack11l11l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह")][bstack1l1ll11l1l_opy_])
  if bstack11l11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ") in bstack1111llll_opy_:
    for arg in bstack1111llll_opy_[bstack11l11l_opy_ (u"ࠫࡦࡸࡧࡴࠩऻ")]:
      options.add_argument(arg)
def bstack1ll111111l_opy_(options, caps):
  if not hasattr(options, bstack11l11l_opy_ (u"ࠬࡑࡅ़࡚ࠩ")):
    return
  if options.KEY == bstack11l11l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ") and options.KEY in caps:
    bstack11lll111l_opy_(options, caps[bstack11l11l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬा")])
  elif options.KEY == bstack11l11l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि") and options.KEY in caps:
    bstack1ll1l1l1_opy_(options, caps[bstack11l11l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧी")])
  elif options.KEY == bstack11l11l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु") and options.KEY in caps:
    bstack1lll1lll_opy_(options, caps[bstack11l11l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬू")])
  elif options.KEY == bstack11l11l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ") and options.KEY in caps:
    bstack1lll11l1_opy_(options, caps[bstack11l11l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॄ")])
  elif options.KEY == bstack11l11l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ") and options.KEY in caps:
    bstack1l1111l1l_opy_(options, caps[bstack11l11l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॆ")])
def bstack1l11111l1_opy_(caps):
  global bstack11l111ll_opy_
  if isinstance(os.environ.get(bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")), str):
    bstack11l111ll_opy_ = eval(os.getenv(bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫै")))
  if bstack11l111ll_opy_:
    if bstack11lll1lll_opy_() < version.parse(bstack11l11l_opy_ (u"ࠫ࠷࠴࠳࠯࠲ࠪॉ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11l11l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬॊ")
    if bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो") in caps:
      browser = caps[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")]
    elif bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ") in caps:
      browser = caps[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॎ")]
    browser = str(browser).lower()
    if browser == bstack11l11l_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧࠪॏ") or browser == bstack11l11l_opy_ (u"ࠫ࡮ࡶࡡࡥࠩॐ"):
      browser = bstack11l11l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ॑")
    if browser == bstack11l11l_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭॒ࠧ"):
      browser = bstack11l11l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓")
    if browser not in [bstack11l11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ॔"), bstack11l11l_opy_ (u"ࠩࡨࡨ࡬࡫ࠧॕ"), bstack11l11l_opy_ (u"ࠪ࡭ࡪ࠭ॖ"), bstack11l11l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॗ"), bstack11l11l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭क़")]:
      return None
    try:
      package = bstack11l11l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨख़").format(browser)
      name = bstack11l11l_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨग़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1ll1l_opy_(options):
        return None
      for bstack11ll1l1l_opy_ in caps.keys():
        options.set_capability(bstack11ll1l1l_opy_, caps[bstack11ll1l1l_opy_])
      bstack1ll111111l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1lll11llll_opy_(options, bstack1ll1111111_opy_):
  if not bstack11l1ll1l_opy_(options):
    return
  for bstack11ll1l1l_opy_ in bstack1ll1111111_opy_.keys():
    if bstack11ll1l1l_opy_ in bstack1ll1l1l11_opy_:
      continue
    if bstack11ll1l1l_opy_ in options._caps and type(options._caps[bstack11ll1l1l_opy_]) in [dict, list]:
      options._caps[bstack11ll1l1l_opy_] = update(options._caps[bstack11ll1l1l_opy_], bstack1ll1111111_opy_[bstack11ll1l1l_opy_])
    else:
      options.set_capability(bstack11ll1l1l_opy_, bstack1ll1111111_opy_[bstack11ll1l1l_opy_])
  bstack1ll111111l_opy_(options, bstack1ll1111111_opy_)
  if bstack11l11l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧज़") in options._caps:
    if options._caps[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")] and options._caps[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")].lower() != bstack11l11l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬफ़"):
      del options._caps[bstack11l11l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫय़")]
def bstack1llll1l11_opy_(proxy_config):
  if bstack11l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॠ") in proxy_config:
    proxy_config[bstack11l11l_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩॡ")] = proxy_config[bstack11l11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")]
    del (proxy_config[bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ")])
  if bstack11l11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।") in proxy_config and proxy_config[bstack11l11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ॥")].lower() != bstack11l11l_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬ०"):
    proxy_config[bstack11l11l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१")] = bstack11l11l_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧ२")
  if bstack11l11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭३") in proxy_config:
    proxy_config[bstack11l11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack11l11l_opy_ (u"ࠪࡴࡦࡩࠧ५")
  return proxy_config
def bstack111llll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11l11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६") in config:
    return proxy
  config[bstack11l11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")] = bstack1llll1l11_opy_(config[bstack11l11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  if proxy == None:
    proxy = Proxy(config[bstack11l11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")])
  return proxy
def bstack11ll1111l_opy_(self):
  global CONFIG
  global bstack1ll1ll11ll_opy_
  try:
    proxy = bstack1l1l11111_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11l11l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭॰")):
        proxies = bstack1l1l1l1l1_opy_(proxy, bstack11ll1l1l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1l1l111_opy_ = proxies.popitem()
          if bstack11l11l_opy_ (u"ࠤ࠽࠳࠴ࠨॱ") in bstack1l1l1l111_opy_:
            return bstack1l1l1l111_opy_
          else:
            return bstack11l11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦॲ") + bstack1l1l1l111_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11l11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣॳ").format(str(e)))
  return bstack1ll1ll11ll_opy_(self)
def bstack11l1l1l1l_opy_():
  global CONFIG
  return bstack111l1111l_opy_(CONFIG) and bstack1llll11l_opy_() and bstack1l1ll1l1_opy_() >= version.parse(bstack1111l11ll_opy_)
def bstack1l1l11l11l_opy_():
  global CONFIG
  return (bstack11l11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨॴ") in CONFIG or bstack11l11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॵ") in CONFIG) and bstack111l1l1l1_opy_()
def bstack1lll11lll1_opy_(config):
  bstack1l1l1ll11l_opy_ = {}
  if bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ") in config:
    bstack1l1l1ll11l_opy_ = config[bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॷ")]
  if bstack11l11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ") in config:
    bstack1l1l1ll11l_opy_ = config[bstack11l11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॹ")]
  proxy = bstack1l1l11111_opy_(config)
  if proxy:
    if proxy.endswith(bstack11l11l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॺ")) and os.path.isfile(proxy):
      bstack1l1l1ll11l_opy_[bstack11l11l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨॻ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11l11l_opy_ (u"࠭࠮ࡱࡣࡦࠫॼ")):
        proxies = bstack1ll111l1l_opy_(config, bstack11ll1l1l1_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1l1l111_opy_ = proxies.popitem()
          if bstack11l11l_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") in bstack1l1l1l111_opy_:
            parsed_url = urlparse(bstack1l1l1l111_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11l11l_opy_ (u"ࠣ࠼࠲࠳ࠧॾ") + bstack1l1l1l111_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1l1l1ll11l_opy_[bstack11l11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬॿ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1l1l1ll11l_opy_[bstack11l11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ঀ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1l1l1ll11l_opy_[bstack11l11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧঁ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1l1l1ll11l_opy_[bstack11l11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨং")] = str(parsed_url.password)
  return bstack1l1l1ll11l_opy_
def bstack1l1l1lll1l_opy_(config):
  if bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ") in config:
    return config[bstack11l11l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ঄")]
  return {}
def bstack1ll1ll11l1_opy_(caps):
  global bstack1l11ll1ll1_opy_
  if bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ") in caps:
    caps[bstack11l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪআ")][bstack11l11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩই")] = True
    if bstack1l11ll1ll1_opy_:
      caps[bstack11l11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ")][bstack11l11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧউ")] = bstack1l11ll1ll1_opy_
  else:
    caps[bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫঊ")] = True
    if bstack1l11ll1ll1_opy_:
      caps[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঋ")] = bstack1l11ll1ll1_opy_
def bstack1l1ll111ll_opy_():
  global CONFIG
  if bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ") in CONFIG and bstack1l1ll111l1_opy_(CONFIG[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭঍")]):
    bstack1l1l1ll11l_opy_ = bstack1lll11lll1_opy_(CONFIG)
    bstack1111l1l11_opy_(CONFIG[bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭঎")], bstack1l1l1ll11l_opy_)
def bstack1111l1l11_opy_(key, bstack1l1l1ll11l_opy_):
  global bstack11l1l1l11_opy_
  logger.info(bstack1l1l111111_opy_)
  try:
    bstack11l1l1l11_opy_ = Local()
    bstack11ll11l1_opy_ = {bstack11l11l_opy_ (u"ࠫࡰ࡫ࡹࠨএ"): key}
    bstack11ll11l1_opy_.update(bstack1l1l1ll11l_opy_)
    logger.debug(bstack1l1lll11ll_opy_.format(str(bstack11ll11l1_opy_)))
    bstack11l1l1l11_opy_.start(**bstack11ll11l1_opy_)
    if bstack11l1l1l11_opy_.isRunning():
      logger.info(bstack11111l11_opy_)
  except Exception as e:
    bstack11l1l1lll_opy_(bstack11l11l11_opy_.format(str(e)))
def bstack11l11l1l1_opy_():
  global bstack11l1l1l11_opy_
  if bstack11l1l1l11_opy_.isRunning():
    logger.info(bstack1lll11l11_opy_)
    bstack11l1l1l11_opy_.stop()
  bstack11l1l1l11_opy_ = None
def bstack11lllll1l_opy_(bstack1lllll1l1l_opy_=[]):
  global CONFIG
  bstack111l1lll1_opy_ = []
  bstack11lll11l_opy_ = [bstack11l11l_opy_ (u"ࠬࡵࡳࠨঐ"), bstack11l11l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ঑"), bstack11l11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ঒"), bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪও"), bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঔ"), bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫক")]
  try:
    for err in bstack1lllll1l1l_opy_:
      bstack111111l1_opy_ = {}
      for k in bstack11lll11l_opy_:
        val = CONFIG[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧখ")][int(err[bstack11l11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫগ")])].get(k)
        if val:
          bstack111111l1_opy_[k] = val
      if(err[bstack11l11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬঘ")] != bstack11l11l_opy_ (u"ࠧࠨঙ")):
        bstack111111l1_opy_[bstack11l11l_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧচ")] = {
          err[bstack11l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧছ")]: err[bstack11l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩজ")]
        }
        bstack111l1lll1_opy_.append(bstack111111l1_opy_)
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ঝ") + str(e))
  finally:
    return bstack111l1lll1_opy_
def bstack1ll1ll1ll_opy_(file_name):
  bstack1lll111l11_opy_ = []
  try:
    bstack1111ll11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1111ll11l_opy_):
      with open(bstack1111ll11l_opy_) as f:
        bstack1lll1ll111_opy_ = json.load(f)
        bstack1lll111l11_opy_ = bstack1lll1ll111_opy_
      os.remove(bstack1111ll11l_opy_)
    return bstack1lll111l11_opy_
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧঞ") + str(e))
def bstack1l11ll1ll_opy_():
  global bstack1ll1l11l1l_opy_
  global bstack1ll1111lll_opy_
  global bstack111lll1l1_opy_
  global bstack11l1ll11l_opy_
  global bstack1l11ll11l1_opy_
  global bstack1l1lll11l1_opy_
  global CONFIG
  percy.shutdown()
  bstack111l1lll_opy_ = os.environ.get(bstack11l11l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧট"))
  if bstack111l1lll_opy_ in [bstack11l11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ঠ"), bstack11l11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧড")]:
    bstack1l11ll111l_opy_()
  if bstack1ll1l11l1l_opy_:
    logger.warning(bstack1l1ll11l1_opy_.format(str(bstack1ll1l11l1l_opy_)))
  else:
    try:
      bstack1l11l1l11l_opy_ = bstack1lllll11ll_opy_(bstack11l11l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨঢ"), logger)
      if bstack1l11l1l11l_opy_.get(bstack11l11l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")) and bstack1l11l1l11l_opy_.get(bstack11l11l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩত")).get(bstack11l11l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧথ")):
        logger.warning(bstack1l1ll11l1_opy_.format(str(bstack1l11l1l11l_opy_[bstack11l11l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")][bstack11l11l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩধ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll1lll1l1_opy_)
  global bstack11l1l1l11_opy_
  if bstack11l1l1l11_opy_:
    bstack11l11l1l1_opy_()
  try:
    for driver in bstack1ll1111lll_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11ll111l1_opy_)
  if bstack1l1lll11l1_opy_ == bstack11l11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧন"):
    bstack1l11ll11l1_opy_ = bstack1ll1ll1ll_opy_(bstack11l11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ঩"))
  if bstack1l1lll11l1_opy_ == bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪপ") and len(bstack11l1ll11l_opy_) == 0:
    bstack11l1ll11l_opy_ = bstack1ll1ll1ll_opy_(bstack11l11l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩফ"))
    if len(bstack11l1ll11l_opy_) == 0:
      bstack11l1ll11l_opy_ = bstack1ll1ll1ll_opy_(bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫব"))
  bstack11ll1lll_opy_ = bstack11l11l_opy_ (u"࠭ࠧভ")
  if len(bstack111lll1l1_opy_) > 0:
    bstack11ll1lll_opy_ = bstack11lllll1l_opy_(bstack111lll1l1_opy_)
  elif len(bstack11l1ll11l_opy_) > 0:
    bstack11ll1lll_opy_ = bstack11lllll1l_opy_(bstack11l1ll11l_opy_)
  elif len(bstack1l11ll11l1_opy_) > 0:
    bstack11ll1lll_opy_ = bstack11lllll1l_opy_(bstack1l11ll11l1_opy_)
  elif len(bstack1lll111ll1_opy_) > 0:
    bstack11ll1lll_opy_ = bstack11lllll1l_opy_(bstack1lll111ll1_opy_)
  if bool(bstack11ll1lll_opy_):
    bstack111l11lll_opy_(bstack11ll1lll_opy_)
  else:
    bstack111l11lll_opy_()
  bstack1l1111111_opy_(bstack1l1ll1lll1_opy_, logger)
  bstack111ll1l1_opy_.bstack111111lll_opy_(CONFIG)
  if len(bstack1l11ll11l1_opy_) > 0:
    sys.exit(len(bstack1l11ll11l1_opy_))
def bstack1lll11ll1l_opy_(self, *args):
  logger.error(bstack1ll11l111_opy_)
  bstack1l11ll1ll_opy_()
  sys.exit(1)
def bstack11l1l1lll_opy_(err):
  logger.critical(bstack1llll111l_opy_.format(str(err)))
  bstack111l11lll_opy_(bstack1llll111l_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11ll1ll_opy_)
  bstack1l11ll111l_opy_()
  sys.exit(1)
def bstack1l1l1lll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111l11lll_opy_(message, True)
  atexit.unregister(bstack1l11ll1ll_opy_)
  bstack1l11ll111l_opy_()
  sys.exit(1)
def bstack1111ll11_opy_():
  global CONFIG
  global bstack11111llll_opy_
  global bstack1l11l1l11_opy_
  global bstack1llllll1l_opy_
  CONFIG = bstack1l1l1l11l1_opy_()
  load_dotenv(CONFIG.get(bstack11l11l_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨম")))
  bstack111l111ll_opy_()
  bstack1lll1ll1l1_opy_()
  CONFIG = bstack1111111l1_opy_(CONFIG)
  update(CONFIG, bstack1l11l1l11_opy_)
  update(CONFIG, bstack11111llll_opy_)
  CONFIG = bstack11lll1111_opy_(CONFIG)
  bstack1llllll1l_opy_ = bstack111ll11l1_opy_(CONFIG)
  bstack111l11111_opy_.bstack1ll1ll1l11_opy_(bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩয"), bstack1llllll1l_opy_)
  if (bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in CONFIG and bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") in bstack11111llll_opy_) or (
          bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") not in bstack1l11l1l11_opy_):
    if os.getenv(bstack11l11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ঴")):
      CONFIG[bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ঵")] = os.getenv(bstack11l11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ"))
    else:
      bstack1llllll11_opy_()
  elif (bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬষ") not in CONFIG and bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬস") in CONFIG) or (
          bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") in bstack1l11l1l11_opy_ and bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঺") not in bstack11111llll_opy_):
    del (CONFIG[bstack11l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঻")])
  if bstack1l1l1l1111_opy_(CONFIG):
    bstack11l1l1lll_opy_(bstack1llll11ll1_opy_)
  bstack1l1l1ll111_opy_()
  bstack1ll11l1l1_opy_()
  if bstack11l111ll_opy_:
    CONFIG[bstack11l11l_opy_ (u"ࠧࡢࡲࡳ়ࠫ")] = bstack1lll1ll11l_opy_(CONFIG)
    logger.info(bstack1ll111l11_opy_.format(CONFIG[bstack11l11l_opy_ (u"ࠨࡣࡳࡴࠬঽ")]))
  if not bstack1llllll1l_opy_:
    CONFIG[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬা")] = [{}]
def bstack1l11l11l_opy_(config, bstack1l1llll1ll_opy_):
  global CONFIG
  global bstack11l111ll_opy_
  CONFIG = config
  bstack11l111ll_opy_ = bstack1l1llll1ll_opy_
def bstack1ll11l1l1_opy_():
  global CONFIG
  global bstack11l111ll_opy_
  if bstack11l11l_opy_ (u"ࠪࡥࡵࡶࠧি") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1ll111lll1_opy_)
    bstack11l111ll_opy_ = True
    bstack111l11111_opy_.bstack1ll1ll1l11_opy_(bstack11l11l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪী"), True)
def bstack1lll1ll11l_opy_(config):
  bstack1l1l1lllll_opy_ = bstack11l11l_opy_ (u"ࠬ࠭ু")
  app = config[bstack11l11l_opy_ (u"࠭ࡡࡱࡲࠪূ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll11l1lll_opy_:
      if os.path.exists(app):
        bstack1l1l1lllll_opy_ = bstack1l11l1ll11_opy_(config, app)
      elif bstack11l11llll_opy_(app):
        bstack1l1l1lllll_opy_ = app
      else:
        bstack11l1l1lll_opy_(bstack11l11l1ll_opy_.format(app))
    else:
      if bstack11l11llll_opy_(app):
        bstack1l1l1lllll_opy_ = app
      elif os.path.exists(app):
        bstack1l1l1lllll_opy_ = bstack1l11l1ll11_opy_(app)
      else:
        bstack11l1l1lll_opy_(bstack1ll1lllll_opy_)
  else:
    if len(app) > 2:
      bstack11l1l1lll_opy_(bstack1l111l1l1_opy_)
    elif len(app) == 2:
      if bstack11l11l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬৃ") in app and bstack11l11l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫৄ") in app:
        if os.path.exists(app[bstack11l11l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅")]):
          bstack1l1l1lllll_opy_ = bstack1l11l1ll11_opy_(config, app[bstack11l11l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")], app[bstack11l11l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧে")])
        else:
          bstack11l1l1lll_opy_(bstack11l11l1ll_opy_.format(app))
      else:
        bstack11l1l1lll_opy_(bstack1l111l1l1_opy_)
    else:
      for key in app:
        if key in bstack1l1l1llll1_opy_:
          if key == bstack11l11l_opy_ (u"ࠬࡶࡡࡵࡪࠪৈ"):
            if os.path.exists(app[key]):
              bstack1l1l1lllll_opy_ = bstack1l11l1ll11_opy_(config, app[key])
            else:
              bstack11l1l1lll_opy_(bstack11l11l1ll_opy_.format(app))
          else:
            bstack1l1l1lllll_opy_ = app[key]
        else:
          bstack11l1l1lll_opy_(bstack111l1l111_opy_)
  return bstack1l1l1lllll_opy_
def bstack11l11llll_opy_(bstack1l1l1lllll_opy_):
  import re
  bstack11111111l_opy_ = re.compile(bstack11l11l_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ৉"))
  bstack1l1l111ll1_opy_ = re.compile(bstack11l11l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৊"))
  if bstack11l11l_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧো") in bstack1l1l1lllll_opy_ or re.fullmatch(bstack11111111l_opy_, bstack1l1l1lllll_opy_) or re.fullmatch(bstack1l1l111ll1_opy_, bstack1l1l1lllll_opy_):
    return True
  else:
    return False
def bstack1l11l1ll11_opy_(config, path, bstack1lll1l11l1_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11l11l_opy_ (u"ࠩࡵࡦࠬৌ")).read()).hexdigest()
  bstack1l1lll111_opy_ = bstack111ll1111_opy_(md5_hash)
  bstack1l1l1lllll_opy_ = None
  if bstack1l1lll111_opy_:
    logger.info(bstack1ll111l11l_opy_.format(bstack1l1lll111_opy_, md5_hash))
    return bstack1l1lll111_opy_
  bstack1ll11111l_opy_ = MultipartEncoder(
    fields={
      bstack11l11l_opy_ (u"ࠪࡪ࡮ࡲࡥࠨ্"): (os.path.basename(path), open(os.path.abspath(path), bstack11l11l_opy_ (u"ࠫࡷࡨࠧৎ")), bstack11l11l_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩ৏")),
      bstack11l11l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐"): bstack1lll1l11l1_opy_
    }
  )
  response = requests.post(bstack1llll1111l_opy_, data=bstack1ll11111l_opy_,
                           headers={bstack11l11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭৑"): bstack1ll11111l_opy_.content_type},
                           auth=(config[bstack11l11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ৒")], config[bstack11l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ৓")]))
  try:
    res = json.loads(response.text)
    bstack1l1l1lllll_opy_ = res[bstack11l11l_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫ৔")]
    logger.info(bstack1ll1111l11_opy_.format(bstack1l1l1lllll_opy_))
    bstack11111111_opy_(md5_hash, bstack1l1l1lllll_opy_)
  except ValueError as err:
    bstack11l1l1lll_opy_(bstack1l111l1l_opy_.format(str(err)))
  return bstack1l1l1lllll_opy_
def bstack1l1l1ll111_opy_():
  global CONFIG
  global bstack11llll1ll_opy_
  bstack1l1l1l11ll_opy_ = 0
  bstack1lllllll11_opy_ = 1
  if bstack11l11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ৕") in CONFIG:
    bstack1lllllll11_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖")]
  if bstack11l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩৗ") in CONFIG:
    bstack1l1l1l11ll_opy_ = len(CONFIG[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘")])
  bstack11llll1ll_opy_ = int(bstack1lllllll11_opy_) * int(bstack1l1l1l11ll_opy_)
def bstack111ll1111_opy_(md5_hash):
  bstack1l11l1lll_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠨࢀࠪ৙")), bstack11l11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৚"), bstack11l11l_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৛"))
  if os.path.exists(bstack1l11l1lll_opy_):
    bstack1lllll11l1_opy_ = json.load(open(bstack1l11l1lll_opy_, bstack11l11l_opy_ (u"ࠫࡷࡨࠧড়")))
    if md5_hash in bstack1lllll11l1_opy_:
      bstack1ll1lll1l_opy_ = bstack1lllll11l1_opy_[md5_hash]
      bstack1l1ll11ll_opy_ = datetime.datetime.now()
      bstack1l11lll11_opy_ = datetime.datetime.strptime(bstack1ll1lll1l_opy_[bstack11l11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨঢ়")], bstack11l11l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৞"))
      if (bstack1l1ll11ll_opy_ - bstack1l11lll11_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll1lll1l_opy_[bstack11l11l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬয়")]):
        return None
      return bstack1ll1lll1l_opy_[bstack11l11l_opy_ (u"ࠨ࡫ࡧࠫৠ")]
  else:
    return None
def bstack11111111_opy_(md5_hash, bstack1l1l1lllll_opy_):
  bstack11lllll1_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠩࢁࠫৡ")), bstack11l11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৢ"))
  if not os.path.exists(bstack11lllll1_opy_):
    os.makedirs(bstack11lllll1_opy_)
  bstack1l11l1lll_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠫࢃ࠭ৣ")), bstack11l11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৤"), bstack11l11l_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৥"))
  bstack11l111ll1_opy_ = {
    bstack11l11l_opy_ (u"ࠧࡪࡦࠪ০"): bstack1l1l1lllll_opy_,
    bstack11l11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ১"): datetime.datetime.strftime(datetime.datetime.now(), bstack11l11l_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭২")),
    bstack11l11l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৩"): str(__version__)
  }
  if os.path.exists(bstack1l11l1lll_opy_):
    bstack1lllll11l1_opy_ = json.load(open(bstack1l11l1lll_opy_, bstack11l11l_opy_ (u"ࠫࡷࡨࠧ৪")))
  else:
    bstack1lllll11l1_opy_ = {}
  bstack1lllll11l1_opy_[md5_hash] = bstack11l111ll1_opy_
  with open(bstack1l11l1lll_opy_, bstack11l11l_opy_ (u"ࠧࡽࠫࠣ৫")) as outfile:
    json.dump(bstack1lllll11l1_opy_, outfile)
def bstack1l11lll1_opy_(self):
  return
def bstack11lll1l11_opy_(self):
  return
def bstack1llll111_opy_(self):
  global bstack1lll1l1ll1_opy_
  bstack1lll1l1ll1_opy_(self)
def bstack1lll11111_opy_():
  global bstack11l111111_opy_
  bstack11l111111_opy_ = True
def bstack1lllll1ll1_opy_(self):
  global bstack1l1l11lll_opy_
  global bstack1ll1111ll1_opy_
  global bstack1lll11111l_opy_
  try:
    if bstack11l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৬") in bstack1l1l11lll_opy_ and self.session_id != None and bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৭"), bstack11l11l_opy_ (u"ࠨࠩ৮")) != bstack11l11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৯"):
      bstack1l11l1llll_opy_ = bstack11l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪৰ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫৱ")
      if bstack1l11l1llll_opy_ == bstack11l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲"):
        bstack1l1ll11111_opy_(logger)
      if self != None:
        bstack1ll1l11l1_opy_(self, bstack1l11l1llll_opy_, bstack11l11l_opy_ (u"࠭ࠬࠡࠩ৳").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11l11l_opy_ (u"ࠧࠨ৴")
    if bstack11l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ৵") in bstack1l1l11lll_opy_ and getattr(threading.current_thread(), bstack11l11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ৶"), None):
      bstack1l1l1ll1ll_opy_.bstack1ll111l111_opy_(self, bstack1lll1l11_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ৷") + str(e))
  bstack1lll11111l_opy_(self)
  self.session_id = None
def bstack1ll11l1ll1_opy_(self, command_executor=bstack11l11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ৸"), *args, **kwargs):
  bstack1l11l1lll1_opy_ = bstack1l11l1ll1l_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack11l11l_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ৹").format(str(command_executor)))
    logger.debug(bstack11l11l_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ৺").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ৻") in command_executor._url:
      bstack111l11111_opy_.bstack1ll1ll1l11_opy_(bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩৼ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ৽") in command_executor):
    bstack111l11111_opy_.bstack1ll1ll1l11_opy_(bstack11l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ৾"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1ll1l1ll1l_opy_.bstack1llllll1l1_opy_(self)
  return bstack1l11l1lll1_opy_
def bstack11lllllll_opy_(args):
  return bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ৿") in str(args)
def bstack111111111_opy_(self, driver_command, *args, **kwargs):
  global bstack1l11lll11l_opy_
  global bstack1l1ll1l111_opy_
  bstack1l1l11l1_opy_ = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ਀"), None) and bstack111111ll_opy_(
          threading.current_thread(), bstack11l11l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬਁ"), None)
  bstack1lll1llll_opy_ = getattr(self, bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧਂ"), None) != None and getattr(self, bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਃ"), None) == True
  if not bstack1l1ll1l111_opy_ and bstack1llllll1l_opy_ and bstack11l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ਄") in CONFIG and CONFIG[bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਅ")] == True and bstack1l1l1ll1_opy_.bstack1111lll1l_opy_(driver_command) and (bstack1lll1llll_opy_ or bstack1l1l11l1_opy_) and not bstack11lllllll_opy_(args):
    try:
      bstack1l1ll1l111_opy_ = True
      logger.debug(bstack11l11l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ਆ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11l11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪਇ").format(str(err)))
    bstack1l1ll1l111_opy_ = False
  response = bstack1l11lll11l_opy_(self, driver_command, *args, **kwargs)
  if bstack11l11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਈ") in str(bstack1l1l11lll_opy_).lower() and bstack1ll1l1ll1l_opy_.on():
    try:
      if driver_command == bstack11l11l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫਉ"):
        bstack1ll1l1ll1l_opy_.bstack1l1lllll11_opy_({
            bstack11l11l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧਊ"): response[bstack11l11l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ਋")],
            bstack11l11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ਌"): bstack1ll1l1ll1l_opy_.current_test_uuid() if bstack1ll1l1ll1l_opy_.current_test_uuid() else bstack1ll1l1ll1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1ll11l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1ll1111ll1_opy_
  global bstack1l11llll1l_opy_
  global bstack1lll111l1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack11111lll_opy_
  global bstack1l1l11lll_opy_
  global bstack1l11l1ll1l_opy_
  global bstack1ll1111lll_opy_
  global bstack1ll1ll111l_opy_
  global bstack1lll1l11_opy_
  CONFIG[bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਍")] = str(bstack1l1l11lll_opy_) + str(__version__)
  command_executor = bstack11ll1l1l1_opy_()
  logger.debug(bstack1lllll1111_opy_.format(command_executor))
  proxy = bstack111llll1_opy_(CONFIG, proxy)
  bstack1ll11lll_opy_ = 0 if bstack1l11llll1l_opy_ < 0 else bstack1l11llll1l_opy_
  try:
    if bstack1lll1l1l1l_opy_ is True:
      bstack1ll11lll_opy_ = int(multiprocessing.current_process().name)
    elif bstack11111lll_opy_ is True:
      bstack1ll11lll_opy_ = int(threading.current_thread().name)
  except:
    bstack1ll11lll_opy_ = 0
  bstack1ll1111111_opy_ = bstack1ll1l1111_opy_(CONFIG, bstack1ll11lll_opy_)
  logger.debug(bstack1lll11l1l_opy_.format(str(bstack1ll1111111_opy_)))
  if bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ਎") in CONFIG and bstack1l1ll111l1_opy_(CONFIG[bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਏ")]):
    bstack1ll1ll11l1_opy_(bstack1ll1111111_opy_)
  if bstack1lll1ll11_opy_.bstack1l1ll1llll_opy_(CONFIG, bstack1ll11lll_opy_) and bstack1lll1ll11_opy_.bstack1l11ll1lll_opy_(bstack1ll1111111_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1lll1ll11_opy_.set_capabilities(bstack1ll1111111_opy_, CONFIG)
  if desired_capabilities:
    bstack1llll11l11_opy_ = bstack1111111l1_opy_(desired_capabilities)
    bstack1llll11l11_opy_[bstack11l11l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧਐ")] = bstack1llll1ll1l_opy_(CONFIG)
    bstack1l11ll1l1_opy_ = bstack1ll1l1111_opy_(bstack1llll11l11_opy_)
    if bstack1l11ll1l1_opy_:
      bstack1ll1111111_opy_ = update(bstack1l11ll1l1_opy_, bstack1ll1111111_opy_)
    desired_capabilities = None
  if options:
    bstack1lll11llll_opy_(options, bstack1ll1111111_opy_)
  if not options:
    options = bstack1l11111l1_opy_(bstack1ll1111111_opy_)
  bstack1lll1l11_opy_ = CONFIG.get(bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਑"))[bstack1ll11lll_opy_]
  if proxy and bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ਒")):
    options.proxy(proxy)
  if options and bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩਓ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1ll1l1_opy_() < version.parse(bstack11l11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪਔ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll1111111_opy_)
  logger.info(bstack1llll1ll1_opy_)
  if bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਕ")):
    bstack1l11l1ll1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਖ")):
    bstack1l11l1ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧਗ")):
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
    bstack1l1l11l1l_opy_ = bstack11l11l_opy_ (u"ࠨࠩਘ")
    if bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪਙ")):
      bstack1l1l11l1l_opy_ = self.caps.get(bstack11l11l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥਚ"))
    else:
      bstack1l1l11l1l_opy_ = self.capabilities.get(bstack11l11l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦਛ"))
    if bstack1l1l11l1l_opy_:
      bstack1l1lll11l_opy_(bstack1l1l11l1l_opy_)
      if bstack1l1ll1l1_opy_() <= version.parse(bstack11l11l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬਜ")):
        self.command_executor._url = bstack11l11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢਝ") + bstack1l11ll1111_opy_ + bstack11l11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦਞ")
      else:
        self.command_executor._url = bstack11l11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥਟ") + bstack1l1l11l1l_opy_ + bstack11l11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥਠ")
      logger.debug(bstack111l11ll1_opy_.format(bstack1l1l11l1l_opy_))
    else:
      logger.debug(bstack1llll1l111_opy_.format(bstack11l11l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦਡ")))
  except Exception as e:
    logger.debug(bstack1llll1l111_opy_.format(e))
  if bstack11l11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਢ") in bstack1l1l11lll_opy_:
    bstack1llll1l1_opy_(bstack1l11llll1l_opy_, bstack1ll1ll111l_opy_)
  bstack1ll1111ll1_opy_ = self.session_id
  if bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਣ") in bstack1l1l11lll_opy_ or bstack11l11l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ਤ") in bstack1l1l11lll_opy_ or bstack11l11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in bstack1l1l11lll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1ll1l1ll1l_opy_.bstack1llllll1l1_opy_(self)
  bstack1ll1111lll_opy_.append(self)
  if bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਦ") in CONFIG and bstack11l11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਧ") in CONFIG[bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਨ")][bstack1ll11lll_opy_]:
    bstack1lll111l1_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਩")][bstack1ll11lll_opy_][bstack11l11l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਪ")]
  logger.debug(bstack1l1l11l1l1_opy_.format(bstack1ll1111ll1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l111l1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1ll1l111l_opy_
      if(bstack11l11l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣਫ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠧࡿࠩਬ")), bstack11l11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਭ"), bstack11l11l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫਮ")), bstack11l11l_opy_ (u"ࠪࡻࠬਯ")) as fp:
          fp.write(bstack11l11l_opy_ (u"ࠦࠧਰ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11l11l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ਱")))):
          with open(args[1], bstack11l11l_opy_ (u"࠭ࡲࠨਲ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11l11l_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭ਲ਼") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11ll111ll_opy_)
            lines.insert(1, bstack11111l1l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11l11l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ਴")), bstack11l11l_opy_ (u"ࠩࡺࠫਵ")) as bstack1l1l1l1ll_opy_:
              bstack1l1l1l1ll_opy_.writelines(lines)
        CONFIG[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬਸ਼")] = str(bstack1l1l11lll_opy_) + str(__version__)
        bstack1ll11lll_opy_ = 0 if bstack1l11llll1l_opy_ < 0 else bstack1l11llll1l_opy_
        try:
          if bstack1lll1l1l1l_opy_ is True:
            bstack1ll11lll_opy_ = int(multiprocessing.current_process().name)
          elif bstack11111lll_opy_ is True:
            bstack1ll11lll_opy_ = int(threading.current_thread().name)
        except:
          bstack1ll11lll_opy_ = 0
        CONFIG[bstack11l11l_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ਷")] = False
        CONFIG[bstack11l11l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦਸ")] = True
        bstack1ll1111111_opy_ = bstack1ll1l1111_opy_(CONFIG, bstack1ll11lll_opy_)
        logger.debug(bstack1lll11l1l_opy_.format(str(bstack1ll1111111_opy_)))
        if CONFIG.get(bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਹ")):
          bstack1ll1ll11l1_opy_(bstack1ll1111111_opy_)
        if bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ਺") in CONFIG and bstack11l11l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਻") in CONFIG[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ਼ࠬ")][bstack1ll11lll_opy_]:
          bstack1lll111l1_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack1ll11lll_opy_][bstack11l11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਾ")]
        args.append(os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠬࢄࠧਿ")), bstack11l11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ੀ"), bstack11l11l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩੁ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll1111111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11l11l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥੂ"))
      bstack1ll1l111l_opy_ = True
      return bstack1lll11l1l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1l1llll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l11llll1l_opy_
    global bstack1lll111l1_opy_
    global bstack1lll1l1l1l_opy_
    global bstack11111lll_opy_
    global bstack1l1l11lll_opy_
    CONFIG[bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ੃")] = str(bstack1l1l11lll_opy_) + str(__version__)
    bstack1ll11lll_opy_ = 0 if bstack1l11llll1l_opy_ < 0 else bstack1l11llll1l_opy_
    try:
      if bstack1lll1l1l1l_opy_ is True:
        bstack1ll11lll_opy_ = int(multiprocessing.current_process().name)
      elif bstack11111lll_opy_ is True:
        bstack1ll11lll_opy_ = int(threading.current_thread().name)
    except:
      bstack1ll11lll_opy_ = 0
    CONFIG[bstack11l11l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ੄")] = True
    bstack1ll1111111_opy_ = bstack1ll1l1111_opy_(CONFIG, bstack1ll11lll_opy_)
    logger.debug(bstack1lll11l1l_opy_.format(str(bstack1ll1111111_opy_)))
    if CONFIG.get(bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ੅")):
      bstack1ll1ll11l1_opy_(bstack1ll1111111_opy_)
    if bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆") in CONFIG and bstack11l11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੇ") in CONFIG[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪੈ")][bstack1ll11lll_opy_]:
      bstack1lll111l1_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")][bstack1ll11lll_opy_][bstack11l11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ੊")]
    import urllib
    import json
    bstack11l1l1l1_opy_ = bstack11l11l_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬੋ") + urllib.parse.quote(json.dumps(bstack1ll1111111_opy_))
    browser = self.connect(bstack11l1l1l1_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1l11111l_opy_():
    global bstack1ll1l111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1l1llll_opy_
        bstack1ll1l111l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l111l1ll_opy_
      bstack1ll1l111l_opy_ = True
    except Exception as e:
      pass
def bstack1lll11l11l_opy_(context, bstack1lll1l1l11_opy_):
  try:
    context.page.evaluate(bstack11l11l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧੌ"), bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻੍ࠩ")+ json.dumps(bstack1lll1l1l11_opy_) + bstack11l11l_opy_ (u"ࠨࡽࡾࠤ੎"))
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ੏"), e)
def bstack1llllll1ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11l11l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ੐"), bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧੑ") + json.dumps(message) + bstack11l11l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭੒") + json.dumps(level) + bstack11l11l_opy_ (u"ࠫࢂࢃࠧ੓"))
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ੔"), e)
def bstack1111lll1_opy_(self, url):
  global bstack1ll11l1ll_opy_
  try:
    bstack1ll11lll11_opy_(url)
  except Exception as err:
    logger.debug(bstack11ll11l1l_opy_.format(str(err)))
  try:
    bstack1ll11l1ll_opy_(self, url)
  except Exception as e:
    try:
      bstack11l11ll1_opy_ = str(e)
      if any(err_msg in bstack11l11ll1_opy_ for err_msg in bstack1111l1111_opy_):
        bstack1ll11lll11_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11ll11l1l_opy_.format(str(err)))
    raise e
def bstack1ll1ll11_opy_(self):
  global bstack1111l1ll1_opy_
  bstack1111l1ll1_opy_ = self
  return
def bstack11111l1l1_opy_(self):
  global bstack1llll11lll_opy_
  bstack1llll11lll_opy_ = self
  return
def bstack11111l111_opy_(test_name, bstack11ll11ll_opy_):
  global CONFIG
  if CONFIG.get(bstack11l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ੕"), False):
    bstack1lllll111_opy_ = os.path.relpath(bstack11ll11ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1lllll111_opy_)
    bstack1ll1l111_opy_ = suite_name + bstack11l11l_opy_ (u"ࠢ࠮ࠤ੖") + test_name
    threading.current_thread().percySessionName = bstack1ll1l111_opy_
def bstack11ll11ll1_opy_(self, test, *args, **kwargs):
  global bstack11111ll1l_opy_
  test_name = None
  bstack11ll11ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack11ll11ll_opy_ = str(test.source)
  bstack11111l111_opy_(test_name, bstack11ll11ll_opy_)
  bstack11111ll1l_opy_(self, test, *args, **kwargs)
def bstack1l111ll1l_opy_(driver, bstack1ll1l111_opy_):
  if not bstack1111l1lll_opy_ and bstack1ll1l111_opy_:
      bstack1l1l1ll1l_opy_ = {
          bstack11l11l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੗"): bstack11l11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੘"),
          bstack11l11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ਖ਼"): {
              bstack11l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩਗ਼"): bstack1ll1l111_opy_
          }
      }
      bstack1lll11ll_opy_ = bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪਜ਼").format(json.dumps(bstack1l1l1ll1l_opy_))
      driver.execute_script(bstack1lll11ll_opy_)
  if bstack1lll1lll1_opy_:
      bstack1ll11lll1_opy_ = {
          bstack11l11l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੜ"): bstack11l11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ੝"),
          bstack11l11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫਫ਼"): {
              bstack11l11l_opy_ (u"ࠩࡧࡥࡹࡧࠧ੟"): bstack1ll1l111_opy_ + bstack11l11l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ੠"),
              bstack11l11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ੡"): bstack11l11l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ੢")
          }
      }
      if bstack1lll1lll1_opy_.status == bstack11l11l_opy_ (u"࠭ࡐࡂࡕࡖࠫ੣"):
          bstack1ll11ll111_opy_ = bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੤").format(json.dumps(bstack1ll11lll1_opy_))
          driver.execute_script(bstack1ll11ll111_opy_)
          bstack1ll1l11l1_opy_(driver, bstack11l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ੥"))
      elif bstack1lll1lll1_opy_.status == bstack11l11l_opy_ (u"ࠩࡉࡅࡎࡒࠧ੦"):
          reason = bstack11l11l_opy_ (u"ࠥࠦ੧")
          bstack1l11lll1l1_opy_ = bstack1ll1l111_opy_ + bstack11l11l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬ੨")
          if bstack1lll1lll1_opy_.message:
              reason = str(bstack1lll1lll1_opy_.message)
              bstack1l11lll1l1_opy_ = bstack1l11lll1l1_opy_ + bstack11l11l_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬ੩") + reason
          bstack1ll11lll1_opy_[bstack11l11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੪")] = {
              bstack11l11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੫"): bstack11l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ੬"),
              bstack11l11l_opy_ (u"ࠩࡧࡥࡹࡧࠧ੭"): bstack1l11lll1l1_opy_
          }
          bstack1ll11ll111_opy_ = bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੮").format(json.dumps(bstack1ll11lll1_opy_))
          driver.execute_script(bstack1ll11ll111_opy_)
          bstack1ll1l11l1_opy_(driver, bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੯"), reason)
          bstack1l11l1l1_opy_(reason, str(bstack1lll1lll1_opy_), str(bstack1l11llll1l_opy_), logger)
def bstack1ll111ll_opy_(driver, test):
  if CONFIG.get(bstack11l11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫੰ"), False) and CONFIG.get(bstack11l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩੱ"), bstack11l11l_opy_ (u"ࠢࡢࡷࡷࡳࠧੲ")) == bstack11l11l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥੳ"):
      bstack1ll1l11111_opy_ = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੴ"), None)
      bstack1ll1111l1_opy_(driver, bstack1ll1l11111_opy_)
  if bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧੵ"), None) and bstack111111ll_opy_(
          threading.current_thread(), bstack11l11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੶"), None):
      logger.info(bstack11l11l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧ੷"))
      bstack1lll1ll11_opy_.bstack1l1lll1l11_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None,
                              path=test.source, bstack1ll11l11ll_opy_=bstack1lll1l11_opy_)
def bstack1ll1l1ll11_opy_(test, bstack1ll1l111_opy_):
    try:
      data = {}
      if test:
        data[bstack11l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸")] = bstack1ll1l111_opy_
      if bstack1lll1lll1_opy_:
        if bstack1lll1lll1_opy_.status == bstack11l11l_opy_ (u"ࠧࡑࡃࡖࡗࠬ੹"):
          data[bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੺")] = bstack11l11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੻")
        elif bstack1lll1lll1_opy_.status == bstack11l11l_opy_ (u"ࠪࡊࡆࡏࡌࠨ੼"):
          data[bstack11l11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੽")] = bstack11l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੾")
          if bstack1lll1lll1_opy_.message:
            data[bstack11l11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭੿")] = str(bstack1lll1lll1_opy_.message)
      user = CONFIG[bstack11l11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ઀")]
      key = CONFIG[bstack11l11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઁ")]
      url = bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧં").format(user, key, bstack1ll1111ll1_opy_)
      headers = {
        bstack11l11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩઃ"): bstack11l11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ઄"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1ll11l_opy_.format(str(e)))
def bstack1ll1llllll_opy_(test, bstack1ll1l111_opy_):
  global CONFIG
  global bstack1llll11lll_opy_
  global bstack1111l1ll1_opy_
  global bstack1ll1111ll1_opy_
  global bstack1lll1lll1_opy_
  global bstack1lll111l1_opy_
  global bstack1lll11ll1_opy_
  global bstack11lll1l1_opy_
  global bstack1l1ll11l11_opy_
  global bstack1ll1l1ll_opy_
  global bstack1ll1111lll_opy_
  global bstack1lll1l11_opy_
  try:
    if not bstack1ll1111ll1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠬࢄࠧઅ")), bstack11l11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭આ"), bstack11l11l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩઇ"))) as f:
        bstack1ll11l111l_opy_ = json.loads(bstack11l11l_opy_ (u"ࠣࡽࠥઈ") + f.read().strip() + bstack11l11l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫઉ") + bstack11l11l_opy_ (u"ࠥࢁࠧઊ"))
        bstack1ll1111ll1_opy_ = bstack1ll11l111l_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1ll1111lll_opy_:
    for driver in bstack1ll1111lll_opy_:
      if bstack1ll1111ll1_opy_ == driver.session_id:
        if test:
          bstack1ll111ll_opy_(driver, test)
        bstack1l111ll1l_opy_(driver, bstack1ll1l111_opy_)
  elif bstack1ll1111ll1_opy_:
    bstack1ll1l1ll11_opy_(test, bstack1ll1l111_opy_)
  if bstack1llll11lll_opy_:
    bstack11lll1l1_opy_(bstack1llll11lll_opy_)
  if bstack1111l1ll1_opy_:
    bstack1l1ll11l11_opy_(bstack1111l1ll1_opy_)
  if bstack11l111111_opy_:
    bstack1ll1l1ll_opy_()
def bstack1lll111l_opy_(self, test, *args, **kwargs):
  bstack1ll1l111_opy_ = None
  if test:
    bstack1ll1l111_opy_ = str(test.name)
  bstack1ll1llllll_opy_(test, bstack1ll1l111_opy_)
  bstack1lll11ll1_opy_(self, test, *args, **kwargs)
def bstack1ll1ll1ll1_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1l1l_opy_
  global CONFIG
  global bstack1ll1111lll_opy_
  global bstack1ll1111ll1_opy_
  bstack1ll1ll111_opy_ = None
  try:
    if bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઋ"), None):
      try:
        if not bstack1ll1111ll1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠬࢄࠧઌ")), bstack11l11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack11l11l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ઎"))) as f:
            bstack1ll11l111l_opy_ = json.loads(bstack11l11l_opy_ (u"ࠣࡽࠥએ") + f.read().strip() + bstack11l11l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫઐ") + bstack11l11l_opy_ (u"ࠥࢁࠧઑ"))
            bstack1ll1111ll1_opy_ = bstack1ll11l111l_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1ll1111lll_opy_:
        for driver in bstack1ll1111lll_opy_:
          if bstack1ll1111ll1_opy_ == driver.session_id:
            bstack1ll1ll111_opy_ = driver
    bstack11l1ll111_opy_ = bstack1lll1ll11_opy_.bstack11l1ll11_opy_(CONFIG, test.tags)
    if bstack1ll1ll111_opy_:
      threading.current_thread().isA11yTest = bstack1lll1ll11_opy_.bstack1l1l1111ll_opy_(bstack1ll1ll111_opy_, bstack11l1ll111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11l1ll111_opy_
  except:
    pass
  bstack1l1l1l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll1lll1_opy_
  bstack1lll1lll1_opy_ = self._test
def bstack1llll1lll_opy_():
  global bstack1llll1ll_opy_
  try:
    if os.path.exists(bstack1llll1ll_opy_):
      os.remove(bstack1llll1ll_opy_)
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ઒") + str(e))
def bstack11ll1llll_opy_():
  global bstack1llll1ll_opy_
  bstack1l11l1l11l_opy_ = {}
  try:
    if not os.path.isfile(bstack1llll1ll_opy_):
      with open(bstack1llll1ll_opy_, bstack11l11l_opy_ (u"ࠬࡽࠧઓ")):
        pass
      with open(bstack1llll1ll_opy_, bstack11l11l_opy_ (u"ࠨࡷࠬࠤઔ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1llll1ll_opy_):
      bstack1l11l1l11l_opy_ = json.load(open(bstack1llll1ll_opy_, bstack11l11l_opy_ (u"ࠧࡳࡤࠪક")))
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪખ") + str(e))
  finally:
    return bstack1l11l1l11l_opy_
def bstack1llll1l1_opy_(platform_index, item_index):
  global bstack1llll1ll_opy_
  try:
    bstack1l11l1l11l_opy_ = bstack11ll1llll_opy_()
    bstack1l11l1l11l_opy_[item_index] = platform_index
    with open(bstack1llll1ll_opy_, bstack11l11l_opy_ (u"ࠤࡺ࠯ࠧગ")) as outfile:
      json.dump(bstack1l11l1l11l_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઘ") + str(e))
def bstack1l1ll1ll1l_opy_(bstack1l11ll111_opy_):
  global CONFIG
  bstack1l11ll11ll_opy_ = bstack11l11l_opy_ (u"ࠫࠬઙ")
  if not bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨચ") in CONFIG:
    logger.info(bstack11l11l_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪછ"))
  try:
    platform = CONFIG[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪજ")][bstack1l11ll111_opy_]
    if bstack11l11l_opy_ (u"ࠨࡱࡶࠫઝ") in platform:
      bstack1l11ll11ll_opy_ += str(platform[bstack11l11l_opy_ (u"ࠩࡲࡷࠬઞ")]) + bstack11l11l_opy_ (u"ࠪ࠰ࠥ࠭ટ")
    if bstack11l11l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧઠ") in platform:
      bstack1l11ll11ll_opy_ += str(platform[bstack11l11l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨડ")]) + bstack11l11l_opy_ (u"࠭ࠬࠡࠩઢ")
    if bstack11l11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫણ") in platform:
      bstack1l11ll11ll_opy_ += str(platform[bstack11l11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬત")]) + bstack11l11l_opy_ (u"ࠩ࠯ࠤࠬથ")
    if bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬદ") in platform:
      bstack1l11ll11ll_opy_ += str(platform[bstack11l11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ધ")]) + bstack11l11l_opy_ (u"ࠬ࠲ࠠࠨન")
    if bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ઩") in platform:
      bstack1l11ll11ll_opy_ += str(platform[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬપ")]) + bstack11l11l_opy_ (u"ࠨ࠮ࠣࠫફ")
    if bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪબ") in platform:
      bstack1l11ll11ll_opy_ += str(platform[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫભ")]) + bstack11l11l_opy_ (u"ࠫ࠱ࠦࠧમ")
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬય") + str(e))
  finally:
    if bstack1l11ll11ll_opy_[len(bstack1l11ll11ll_opy_) - 2:] == bstack11l11l_opy_ (u"࠭ࠬࠡࠩર"):
      bstack1l11ll11ll_opy_ = bstack1l11ll11ll_opy_[:-2]
    return bstack1l11ll11ll_opy_
def bstack1l1l11ll_opy_(path, bstack1l11ll11ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll1111ll_opy_ = ET.parse(path)
    bstack1ll1lllll1_opy_ = bstack1lll1111ll_opy_.getroot()
    bstack1l11lllll1_opy_ = None
    for suite in bstack1ll1lllll1_opy_.iter(bstack11l11l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭઱")):
      if bstack11l11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨલ") in suite.attrib:
        suite.attrib[bstack11l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧળ")] += bstack11l11l_opy_ (u"ࠪࠤࠬ઴") + bstack1l11ll11ll_opy_
        bstack1l11lllll1_opy_ = suite
    bstack1ll11lll1l_opy_ = None
    for robot in bstack1ll1lllll1_opy_.iter(bstack11l11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪવ")):
      bstack1ll11lll1l_opy_ = robot
    bstack1l11ll1l_opy_ = len(bstack1ll11lll1l_opy_.findall(bstack11l11l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫશ")))
    if bstack1l11ll1l_opy_ == 1:
      bstack1ll11lll1l_opy_.remove(bstack1ll11lll1l_opy_.findall(bstack11l11l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬષ"))[0])
      bstack1lll1111l1_opy_ = ET.Element(bstack11l11l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭સ"), attrib={bstack11l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭હ"): bstack11l11l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ઺"), bstack11l11l_opy_ (u"ࠪ࡭ࡩ࠭઻"): bstack11l11l_opy_ (u"ࠫࡸ࠶઼ࠧ")})
      bstack1ll11lll1l_opy_.insert(1, bstack1lll1111l1_opy_)
      bstack111l11ll_opy_ = None
      for suite in bstack1ll11lll1l_opy_.iter(bstack11l11l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઽ")):
        bstack111l11ll_opy_ = suite
      bstack111l11ll_opy_.append(bstack1l11lllll1_opy_)
      bstack1111ll1ll_opy_ = None
      for status in bstack1l11lllll1_opy_.iter(bstack11l11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ા")):
        bstack1111ll1ll_opy_ = status
      bstack111l11ll_opy_.append(bstack1111ll1ll_opy_)
    bstack1lll1111ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬિ") + str(e))
def bstack1ll1llll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack111ll111l_opy_
  global CONFIG
  if bstack11l11l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧી") in options:
    del options[bstack11l11l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨુ")]
  bstack1llllll111_opy_ = bstack11ll1llll_opy_()
  for bstack1ll1l1llll_opy_ in bstack1llllll111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11l11l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪૂ"), str(bstack1ll1l1llll_opy_), bstack11l11l_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨૃ"))
    bstack1l1l11ll_opy_(path, bstack1l1ll1ll1l_opy_(bstack1llllll111_opy_[bstack1ll1l1llll_opy_]))
  bstack1llll1lll_opy_()
  return bstack111ll111l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1l1llll1_opy_(self, ff_profile_dir):
  global bstack1l11lll1ll_opy_
  if not ff_profile_dir:
    return None
  return bstack1l11lll1ll_opy_(self, ff_profile_dir)
def bstack1l1lll1ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1l11ll1ll1_opy_
  bstack1l1ll11lll_opy_ = []
  if bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ") in CONFIG:
    bstack1l1ll11lll_opy_ = CONFIG[bstack11l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11l11l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ૆")],
      pabot_args[bstack11l11l_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤે")],
      argfile,
      pabot_args.get(bstack11l11l_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢૈ")),
      pabot_args[bstack11l11l_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨૉ")],
      platform[0],
      bstack1l11ll1ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11l11l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૊")] or [(bstack11l11l_opy_ (u"ࠧࠨો"), None)]
    for platform in enumerate(bstack1l1ll11lll_opy_)
  ]
def bstack1lllll11l_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll1llll11_opy_=bstack11l11l_opy_ (u"࠭ࠧૌ")):
  global bstack1l11llllll_opy_
  self.platform_index = platform_index
  self.bstack1lll1ll1_opy_ = bstack1ll1llll11_opy_
  bstack1l11llllll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1ll1111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1111_opy_
  global bstack11l111lll_opy_
  if not bstack11l11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ") in item.options:
    item.options[bstack11l11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૎")] = []
  for v in item.options[bstack11l11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૏")]:
    if bstack11l11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩૐ") in v:
      item.options[bstack11l11l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૑")].remove(v)
    if bstack11l11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૒") in v:
      item.options[bstack11l11l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૓")].remove(v)
    if bstack11l11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ૔") in v:
      item.options[bstack11l11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૕")].remove(v)
  item.options[bstack11l11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૖")].insert(0, bstack11l11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬ૗").format(item.platform_index))
  item.options[bstack11l11l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૘")].insert(0, bstack11l11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬ૙").format(item.bstack1lll1ll1_opy_))
  if bstack11l111lll_opy_:
    item.options[bstack11l11l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૚")].insert(0, bstack11l11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ૛").format(bstack11l111lll_opy_))
  return bstack1l1l1111_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack11ll1l1ll_opy_(command, item_index):
  if bstack111l11111_opy_.get_property(bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ૜")):
    os.environ[bstack11l11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૝")] = json.dumps(CONFIG[bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૞")][item_index % bstack1ll11llll1_opy_])
  global bstack11l111lll_opy_
  if bstack11l111lll_opy_:
    command[0] = command[0].replace(bstack11l11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૟"), bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩૠ") + str(
      item_index) + bstack11l11l_opy_ (u"࠭ࠠࠨૡ") + bstack11l111lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11l11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ૢ"),
                                    bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬૣ") + str(item_index), 1)
def bstack1ll1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l11l111_opy_
  bstack11ll1l1ll_opy_(command, item_index)
  return bstack11l11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack111ll1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l11l111_opy_
  bstack11ll1l1ll_opy_(command, item_index)
  return bstack11l11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l11l111_opy_
  bstack11ll1l1ll_opy_(command, item_index)
  return bstack11l11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11l11111l_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1l111l_opy_
  bstack1lll1lll1l_opy_ = bstack11l1l111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack11l11l_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ૤")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11l11l_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ૥")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1lll1lll1l_opy_
def bstack1l1l11ll1_opy_(self, name, context, *args):
  os.environ[bstack11l11l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ૦")] = json.dumps(CONFIG[bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૧")][int(threading.current_thread()._name) % bstack1ll11llll1_opy_])
  global bstack1ll11ll11_opy_
  if name == bstack11l11l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ૨"):
    bstack1ll11ll11_opy_(self, name, context, *args)
    try:
      if not bstack1111l1lll_opy_:
        bstack1ll1ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lll1_opy_(bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૩")) else context.browser
        bstack1lll1l1l11_opy_ = str(self.feature.name)
        bstack1lll11l11l_opy_(context, bstack1lll1l1l11_opy_)
        bstack1ll1ll111_opy_.execute_script(bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭૪") + json.dumps(bstack1lll1l1l11_opy_) + bstack11l11l_opy_ (u"ࠩࢀࢁࠬ૫"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack11l11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ૬").format(str(e)))
  elif name == bstack11l11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭૭"):
    bstack1ll11ll11_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack11l11l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ૮")):
        self.driver_before_scenario = True
      if (not bstack1111l1lll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1lll1l1l11_opy_ = str(self.feature.name)
        bstack1lll1l1l11_opy_ = feature_name + bstack11l11l_opy_ (u"࠭ࠠ࠮ࠢࠪ૯") + scenario_name
        bstack1ll1ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lll1_opy_(bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭૰")) else context.browser
        if self.driver_before_scenario:
          bstack1lll11l11l_opy_(context, bstack1lll1l1l11_opy_)
          bstack1ll1ll111_opy_.execute_script(bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭૱") + json.dumps(bstack1lll1l1l11_opy_) + bstack11l11l_opy_ (u"ࠩࢀࢁࠬ૲"))
    except Exception as e:
      logger.debug(bstack11l11l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫ૳").format(str(e)))
  elif name == bstack11l11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૴"):
    try:
      bstack1l1111ll_opy_ = args[0].status.name
      bstack1ll1ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૵") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l1111ll_opy_).lower() == bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭૶"):
        bstack1l11ll11l_opy_ = bstack11l11l_opy_ (u"ࠧࠨ૷")
        bstack1ll1l1l1l_opy_ = bstack11l11l_opy_ (u"ࠨࠩ૸")
        bstack111111ll1_opy_ = bstack11l11l_opy_ (u"ࠩࠪૹ")
        try:
          import traceback
          bstack1l11ll11l_opy_ = self.exception.__class__.__name__
          bstack111l1l1l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1ll1l1l1l_opy_ = bstack11l11l_opy_ (u"ࠪࠤࠬૺ").join(bstack111l1l1l_opy_)
          bstack111111ll1_opy_ = bstack111l1l1l_opy_[-1]
        except Exception as e:
          logger.debug(bstack11l1lll11_opy_.format(str(e)))
        bstack1l11ll11l_opy_ += bstack111111ll1_opy_
        bstack1llllll1ll_opy_(context, json.dumps(str(args[0].name) + bstack11l11l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥૻ") + str(bstack1ll1l1l1l_opy_)),
                            bstack11l11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦૼ"))
        if self.driver_before_scenario:
          bstack1l11ll1l11_opy_(getattr(context, bstack11l11l_opy_ (u"࠭ࡰࡢࡩࡨࠫ૽"), None), bstack11l11l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ૾"), bstack1l11ll11l_opy_)
          bstack1ll1ll111_opy_.execute_script(bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭૿") + json.dumps(str(args[0].name) + bstack11l11l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ଀") + str(bstack1ll1l1l1l_opy_)) + bstack11l11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪଁ"))
        if self.driver_before_scenario:
          bstack1ll1l11l1_opy_(bstack1ll1ll111_opy_, bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫଂ"), bstack11l11l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤଃ") + str(bstack1l11ll11l_opy_))
      else:
        bstack1llllll1ll_opy_(context, bstack11l11l_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ଄"), bstack11l11l_opy_ (u"ࠢࡪࡰࡩࡳࠧଅ"))
        if self.driver_before_scenario:
          bstack1l11ll1l11_opy_(getattr(context, bstack11l11l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭ଆ"), None), bstack11l11l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤଇ"))
        bstack1ll1ll111_opy_.execute_script(bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨଈ") + json.dumps(str(args[0].name) + bstack11l11l_opy_ (u"ࠦࠥ࠳ࠠࡑࡣࡶࡷࡪࡪࠡࠣଉ")) + bstack11l11l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫଊ"))
        if self.driver_before_scenario:
          bstack1ll1l11l1_opy_(bstack1ll1ll111_opy_, bstack11l11l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨଋ"))
    except Exception as e:
      logger.debug(bstack11l11l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩଌ").format(str(e)))
  elif name == bstack11l11l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ଍"):
    try:
      bstack1ll1ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lll1_opy_(bstack11l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ଎")) else context.browser
      if context.failed is True:
        bstack11llllll_opy_ = []
        bstack1ll11llll_opy_ = []
        bstack1l1ll111_opy_ = []
        bstack111ll11ll_opy_ = bstack11l11l_opy_ (u"ࠪࠫଏ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack11llllll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack111l1l1l_opy_ = traceback.format_tb(exc_tb)
            bstack111lllll1_opy_ = bstack11l11l_opy_ (u"ࠫࠥ࠭ଐ").join(bstack111l1l1l_opy_)
            bstack1ll11llll_opy_.append(bstack111lllll1_opy_)
            bstack1l1ll111_opy_.append(bstack111l1l1l_opy_[-1])
        except Exception as e:
          logger.debug(bstack11l1lll11_opy_.format(str(e)))
        bstack1l11ll11l_opy_ = bstack11l11l_opy_ (u"ࠬ࠭଑")
        for i in range(len(bstack11llllll_opy_)):
          bstack1l11ll11l_opy_ += bstack11llllll_opy_[i] + bstack1l1ll111_opy_[i] + bstack11l11l_opy_ (u"࠭࡜࡯ࠩ଒")
        bstack111ll11ll_opy_ = bstack11l11l_opy_ (u"ࠧࠡࠩଓ").join(bstack1ll11llll_opy_)
        if not self.driver_before_scenario:
          bstack1llllll1ll_opy_(context, bstack111ll11ll_opy_, bstack11l11l_opy_ (u"ࠣࡧࡵࡶࡴࡸࠢଔ"))
          bstack1l11ll1l11_opy_(getattr(context, bstack11l11l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧକ"), None), bstack11l11l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଖ"), bstack1l11ll11l_opy_)
          bstack1ll1ll111_opy_.execute_script(bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଗ") + json.dumps(bstack111ll11ll_opy_) + bstack11l11l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬଘ"))
          bstack1ll1l11l1_opy_(bstack1ll1ll111_opy_, bstack11l11l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨଙ"), bstack11l11l_opy_ (u"ࠢࡔࡱࡰࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵࡳࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡟ࡲࠧଚ") + str(bstack1l11ll11l_opy_))
          bstack1llll1l1ll_opy_ = bstack1l11l11l1_opy_(bstack111ll11ll_opy_, self.feature.name, logger)
          if (bstack1llll1l1ll_opy_ != None):
            bstack1lll111ll1_opy_.append(bstack1llll1l1ll_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1llllll1ll_opy_(context, bstack11l11l_opy_ (u"ࠣࡈࡨࡥࡹࡻࡲࡦ࠼ࠣࠦଛ") + str(self.feature.name) + bstack11l11l_opy_ (u"ࠤࠣࡴࡦࡹࡳࡦࡦࠤࠦଜ"), bstack11l11l_opy_ (u"ࠥ࡭ࡳ࡬࡯ࠣଝ"))
          bstack1l11ll1l11_opy_(getattr(context, bstack11l11l_opy_ (u"ࠫࡵࡧࡧࡦࠩଞ"), None), bstack11l11l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧଟ"))
          bstack1ll1ll111_opy_.execute_script(bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫଠ") + json.dumps(bstack11l11l_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥଡ") + str(self.feature.name) + bstack11l11l_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥଢ")) + bstack11l11l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨଣ"))
          bstack1ll1l11l1_opy_(bstack1ll1ll111_opy_, bstack11l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪତ"))
          bstack1llll1l1ll_opy_ = bstack1l11l11l1_opy_(bstack111ll11ll_opy_, self.feature.name, logger)
          if (bstack1llll1l1ll_opy_ != None):
            bstack1lll111ll1_opy_.append(bstack1llll1l1ll_opy_)
    except Exception as e:
      logger.debug(bstack11l11l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡨࡨࡥࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭ଥ").format(str(e)))
  else:
    bstack1ll11ll11_opy_(self, name, context, *args)
  if name in [bstack11l11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣ࡫࡫ࡡࡵࡷࡵࡩࠬଦ"), bstack11l11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧଧ")]:
    bstack1ll11ll11_opy_(self, name, context, *args)
    if (name == bstack11l11l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠨନ") and self.driver_before_scenario) or (
            name == bstack11l11l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ଩") and not self.driver_before_scenario):
      try:
        bstack1ll1ll111_opy_ = threading.current_thread().bstackSessionDriver if bstack11l11lll1_opy_(bstack11l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨପ")) else context.browser
        bstack1ll1ll111_opy_.quit()
      except Exception:
        pass
def bstack111111l11_opy_(config, startdir):
  return bstack11l11l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠤࢀ࠶ࡽࠣଫ").format(bstack11l11l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥବ"))
notset = Notset()
def bstack1lll11lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack11ll1l11l_opy_
  if str(name).lower() == bstack11l11l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬଭ"):
    return bstack11l11l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧମ")
  else:
    return bstack11ll1l11l_opy_(self, name, default, skip)
def bstack1l1l1l1ll1_opy_(item, when):
  global bstack1111l11l_opy_
  try:
    bstack1111l11l_opy_(item, when)
  except Exception as e:
    pass
def bstack1l1l1ll1l1_opy_():
  return
def bstack11ll1lll1_opy_(type, name, status, reason, bstack111ll1lll_opy_, bstack1l1l111l11_opy_):
  bstack1l1l1ll1l_opy_ = {
    bstack11l11l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧଯ"): type,
    bstack11l11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫର"): {}
  }
  if type == bstack11l11l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ଱"):
    bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଲ")][bstack11l11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪଳ")] = bstack111ll1lll_opy_
    bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ଴")][bstack11l11l_opy_ (u"࠭ࡤࡢࡶࡤࠫଵ")] = json.dumps(str(bstack1l1l111l11_opy_))
  if type == bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଶ"):
    bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫଷ")][bstack11l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧସ")] = name
  if type == bstack11l11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ହ"):
    bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ଺")][bstack11l11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ଻")] = status
    if status == bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ଼࠭"):
      bstack1l1l1ll1l_opy_[bstack11l11l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଽ")][bstack11l11l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨା")] = json.dumps(str(reason))
  bstack1lll11ll_opy_ = bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧି").format(json.dumps(bstack1l1l1ll1l_opy_))
  return bstack1lll11ll_opy_
def bstack1ll1l1l1l1_opy_(driver_command, response):
    if driver_command == bstack11l11l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧୀ"):
        bstack1ll1l1ll1l_opy_.bstack1l1lllll11_opy_({
            bstack11l11l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪୁ"): response[bstack11l11l_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫୂ")],
            bstack11l11l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ୃ"): bstack1ll1l1ll1l_opy_.current_test_uuid()
        })
def bstack11l11ll11_opy_(item, call, rep):
  global bstack111llll11_opy_
  global bstack1ll1111lll_opy_
  global bstack1111l1lll_opy_
  name = bstack11l11l_opy_ (u"ࠧࠨୄ")
  try:
    if rep.when == bstack11l11l_opy_ (u"ࠨࡥࡤࡰࡱ࠭୅"):
      bstack1ll1111ll1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1111l1lll_opy_:
          name = str(rep.nodeid)
          bstack1l111lll1_opy_ = bstack11ll1lll1_opy_(bstack11l11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ୆"), name, bstack11l11l_opy_ (u"ࠪࠫେ"), bstack11l11l_opy_ (u"ࠫࠬୈ"), bstack11l11l_opy_ (u"ࠬ࠭୉"), bstack11l11l_opy_ (u"࠭ࠧ୊"))
          threading.current_thread().bstack1llll111l1_opy_ = name
          for driver in bstack1ll1111lll_opy_:
            if bstack1ll1111ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1l111lll1_opy_)
      except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧୋ").format(str(e)))
      try:
        bstack11ll1111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11l11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩୌ"):
          status = bstack11l11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥ୍ࠩ") if rep.outcome.lower() == bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ୎") else bstack11l11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ୏")
          reason = bstack11l11l_opy_ (u"ࠬ࠭୐")
          if status == bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭୑"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11l11l_opy_ (u"ࠧࡪࡰࡩࡳࠬ୒") if status == bstack11l11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ୓") else bstack11l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ୔")
          data = name + bstack11l11l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ୕") if status == bstack11l11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫୖ") else name + bstack11l11l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨୗ") + reason
          bstack1lll1l1111_opy_ = bstack11ll1lll1_opy_(bstack11l11l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ୘"), bstack11l11l_opy_ (u"ࠧࠨ୙"), bstack11l11l_opy_ (u"ࠨࠩ୚"), bstack11l11l_opy_ (u"ࠩࠪ୛"), level, data)
          for driver in bstack1ll1111lll_opy_:
            if bstack1ll1111ll1_opy_ == driver.session_id:
              driver.execute_script(bstack1lll1l1111_opy_)
      except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧଡ଼").format(str(e)))
  except Exception as e:
    logger.debug(bstack11l11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨଢ଼").format(str(e)))
  bstack111llll11_opy_(item, call, rep)
def bstack1ll1111l1_opy_(driver, bstack1ll11l11l_opy_):
  PercySDK.screenshot(driver, bstack1ll11l11l_opy_)
def bstack1ll1llll_opy_(driver):
  if bstack11lll1l1l_opy_.bstack11ll11111_opy_() is True or bstack11lll1l1l_opy_.capturing() is True:
    return
  bstack11lll1l1l_opy_.bstack1l1llll1l1_opy_()
  while not bstack11lll1l1l_opy_.bstack11ll11111_opy_():
    bstack1lllll1l11_opy_ = bstack11lll1l1l_opy_.bstack1llllll11l_opy_()
    bstack1ll1111l1_opy_(driver, bstack1lllll1l11_opy_)
  bstack11lll1l1l_opy_.bstack1lll1l11ll_opy_()
def bstack1ll11ll1ll_opy_(sequence, driver_command, response = None, bstack1111ll111_opy_ = None, args = None):
    try:
      if sequence != bstack11l11l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ୞"):
        return
      if not CONFIG.get(bstack11l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬୟ"), False):
        return
      bstack1lllll1l11_opy_ = bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪୠ"), None)
      for command in bstack111l1ll11_opy_:
        if command == driver_command:
          for driver in bstack1ll1111lll_opy_:
            bstack1ll1llll_opy_(driver)
      bstack1l111ll11_opy_ = CONFIG.get(bstack11l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫୡ"), bstack11l11l_opy_ (u"ࠤࡤࡹࡹࡵࠢୢ"))
      if driver_command in bstack11l1ll1ll_opy_[bstack1l111ll11_opy_]:
        bstack11lll1l1l_opy_.bstack1111lllll_opy_(bstack1lllll1l11_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1l1111l_opy_(framework_name):
  global bstack1l1l11lll_opy_
  global bstack1ll1l111l_opy_
  global bstack1111l111l_opy_
  bstack1l1l11lll_opy_ = framework_name
  logger.info(bstack11l1l111_opy_.format(bstack1l1l11lll_opy_.split(bstack11l11l_opy_ (u"ࠪ࠱ࠬୣ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1llllll1l_opy_:
      Service.start = bstack1l11lll1_opy_
      Service.stop = bstack11lll1l11_opy_
      webdriver.Remote.get = bstack1111lll1_opy_
      WebDriver.close = bstack1llll111_opy_
      WebDriver.quit = bstack1lllll1ll1_opy_
      webdriver.Remote.__init__ = bstack1ll11l11_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1llllll1l_opy_ and bstack1ll1l1ll1l_opy_.on():
      webdriver.Remote.__init__ = bstack1ll11l1ll1_opy_
    WebDriver.execute = bstack111111111_opy_
    bstack1ll1l111l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1llllll1l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll11111_opy_
  except Exception as e:
    pass
  bstack1l1l11111l_opy_()
  if not bstack1ll1l111l_opy_:
    bstack1l1l1lll1_opy_(bstack11l11l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨ୤"), bstack1l1111l1_opy_)
  if bstack11l1l1l1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11ll1111l_opy_
    except Exception as e:
      logger.error(bstack1l1l11ll1l_opy_.format(str(e)))
  if bstack1l1l11l11l_opy_():
    bstack1l11lll111_opy_(CONFIG, logger)
  if (bstack11l11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ୥") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack11l11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ୦"), False):
          bstack1llllllll_opy_(bstack1ll11ll1ll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1l1llll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack11111l1l1_opy_
      except Exception as e:
        logger.warn(bstack1llll111ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1l1ll1111_opy_
        bstack1l1ll1111_opy_.close = bstack1ll1ll11_opy_
      except Exception as e:
        logger.debug(bstack1ll1ll1l1_opy_ + str(e))
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1llll111ll_opy_)
    Output.start_test = bstack11ll11ll1_opy_
    Output.end_test = bstack1lll111l_opy_
    TestStatus.__init__ = bstack1ll1ll1ll1_opy_
    QueueItem.__init__ = bstack1lllll11l_opy_
    pabot._create_items = bstack1l1lll1ll_opy_
    try:
      from pabot import __version__ as bstack1111l111_opy_
      if version.parse(bstack1111l111_opy_) >= version.parse(bstack11l11l_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧ୧")):
        pabot._run = bstack11l11l11l_opy_
      elif version.parse(bstack1111l111_opy_) >= version.parse(bstack11l11l_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨ୨")):
        pabot._run = bstack111ll1ll_opy_
      else:
        pabot._run = bstack1ll1l11l11_opy_
    except Exception as e:
      pabot._run = bstack1ll1l11l11_opy_
    pabot._create_command_for_execution = bstack1ll1111l_opy_
    pabot._report_results = bstack1ll1llll1l_opy_
  if bstack11l11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ୩") in str(framework_name).lower():
    if not bstack1llllll1l_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1ll1ll1111_opy_)
    Runner.run_hook = bstack1l1l11ll1_opy_
    Step.run = bstack11l11111l_opy_
  if bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ୪") in str(framework_name).lower():
    if not bstack1llllll1l_opy_:
      return
    try:
      if CONFIG.get(bstack11l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ୫"), False):
          bstack1llllllll_opy_(bstack1ll11ll1ll_opy_)
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
def bstack11ll1l11_opy_():
  global CONFIG
  if bstack11l11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ୬") in CONFIG and int(CONFIG[bstack11l11l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭୭")]) > 1:
    logger.warn(bstack11ll1ll11_opy_)
def bstack1l1ll1lll_opy_(arg, bstack11111l11l_opy_, bstack1lll111l11_opy_=None):
  global CONFIG
  global bstack1l11ll1111_opy_
  global bstack11l111ll_opy_
  global bstack1llllll1l_opy_
  global bstack111l11111_opy_
  bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ୮")
  if bstack11111l11l_opy_ and isinstance(bstack11111l11l_opy_, str):
    bstack11111l11l_opy_ = eval(bstack11111l11l_opy_)
  CONFIG = bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ୯")]
  bstack1l11ll1111_opy_ = bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ୰")]
  bstack11l111ll_opy_ = bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬୱ")]
  bstack1llllll1l_opy_ = bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ୲")]
  bstack111l11111_opy_.bstack1ll1ll1l11_opy_(bstack11l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭୳"), bstack1llllll1l_opy_)
  os.environ[bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ୴")] = bstack111l1lll_opy_
  os.environ[bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭୵")] = json.dumps(CONFIG)
  os.environ[bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ୶")] = bstack1l11ll1111_opy_
  os.environ[bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୷")] = str(bstack11l111ll_opy_)
  os.environ[bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩ୸")] = str(True)
  if bstack1ll111lll_opy_(arg, [bstack11l11l_opy_ (u"ࠫ࠲ࡴࠧ୹"), bstack11l11l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭୺")]) != -1:
    os.environ[bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ୻")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack111lll11l_opy_)
    return
  bstack1lll11l1ll_opy_()
  global bstack11llll1ll_opy_
  global bstack1l11llll1l_opy_
  global bstack1l11ll1ll1_opy_
  global bstack11l111lll_opy_
  global bstack11l1ll11l_opy_
  global bstack1111l111l_opy_
  global bstack1lll1l1l1l_opy_
  arg.append(bstack11l11l_opy_ (u"ࠢ࠮࡙ࠥ୼"))
  arg.append(bstack11l11l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦ୽"))
  arg.append(bstack11l11l_opy_ (u"ࠤ࠰࡛ࠧ୾"))
  arg.append(bstack11l11l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤ୿"))
  global bstack1l11l1ll1l_opy_
  global bstack1lll11111l_opy_
  global bstack1l11lll11l_opy_
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
    bstack1l11lll11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111l1111l_opy_(CONFIG) and bstack1llll11l_opy_():
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
    logger.debug(bstack11l11l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ஀"))
  bstack1l11ll1ll1_opy_ = CONFIG.get(bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஁"), {}).get(bstack11l11l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨஂ"))
  bstack1lll1l1l1l_opy_ = True
  bstack1l1l1111l_opy_(bstack1l1llll11l_opy_)
  os.environ[bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨஃ")] = CONFIG[bstack11l11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ஄")]
  os.environ[bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬஅ")] = CONFIG[bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ஆ")]
  os.environ[bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧஇ")] = bstack1llllll1l_opy_.__str__()
  from _pytest.config import main as bstack1ll11ll11l_opy_
  bstack1l11lllll_opy_ = []
  try:
    bstack11ll111l_opy_ = bstack1ll11ll11l_opy_(arg)
    if bstack11l11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩஈ") in multiprocessing.current_process().__dict__.keys():
      for bstack111111l1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11lllll_opy_.append(bstack111111l1l_opy_)
    try:
      bstack111l111l_opy_ = (bstack1l11lllll_opy_, int(bstack11ll111l_opy_))
      bstack1lll111l11_opy_.append(bstack111l111l_opy_)
    except:
      bstack1lll111l11_opy_.append((bstack1l11lllll_opy_, bstack11ll111l_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11lllll_opy_.append({bstack11l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫஉ"): bstack11l11l_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩஊ") + os.environ.get(bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ஋")), bstack11l11l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ஌"): traceback.format_exc(), bstack11l11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ஍"): int(os.environ.get(bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫஎ")))})
    bstack1lll111l11_opy_.append((bstack1l11lllll_opy_, 1))
def bstack1l111111l_opy_(arg):
  global bstack1ll1lll11_opy_
  bstack1l1l1111l_opy_(bstack1llll1llll_opy_)
  os.environ[bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ஏ")] = str(bstack11l111ll_opy_)
  from behave.__main__ import main as bstack1ll1l111l1_opy_
  status_code = bstack1ll1l111l1_opy_(arg)
  if status_code != 0:
    bstack1ll1lll11_opy_ = status_code
def bstack1ll11l1l1l_opy_():
  logger.info(bstack1lll1l1l1_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11l11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬஐ"), help=bstack11l11l_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨ஑"))
  parser.add_argument(bstack11l11l_opy_ (u"ࠨ࠯ࡸࠫஒ"), bstack11l11l_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭ஓ"), help=bstack11l11l_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩஔ"))
  parser.add_argument(bstack11l11l_opy_ (u"ࠫ࠲ࡱࠧக"), bstack11l11l_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫ஖"), help=bstack11l11l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧ஗"))
  parser.add_argument(bstack11l11l_opy_ (u"ࠧ࠮ࡨࠪ஘"), bstack11l11l_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ங"), help=bstack11l11l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨச"))
  bstack11ll1ll1_opy_ = parser.parse_args()
  try:
    bstack1lll11ll11_opy_ = bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ஛")
    if bstack11ll1ll1_opy_.framework and bstack11ll1ll1_opy_.framework not in (bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫஜ"), bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭஝")):
      bstack1lll11ll11_opy_ = bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬஞ")
    bstack1l111llll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll11ll11_opy_)
    bstack1l111l111_opy_ = open(bstack1l111llll_opy_, bstack11l11l_opy_ (u"ࠧࡳࠩட"))
    bstack1l11ll11_opy_ = bstack1l111l111_opy_.read()
    bstack1l111l111_opy_.close()
    if bstack11ll1ll1_opy_.username:
      bstack1l11ll11_opy_ = bstack1l11ll11_opy_.replace(bstack11l11l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ஠"), bstack11ll1ll1_opy_.username)
    if bstack11ll1ll1_opy_.key:
      bstack1l11ll11_opy_ = bstack1l11ll11_opy_.replace(bstack11l11l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ஡"), bstack11ll1ll1_opy_.key)
    if bstack11ll1ll1_opy_.framework:
      bstack1l11ll11_opy_ = bstack1l11ll11_opy_.replace(bstack11l11l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ஢"), bstack11ll1ll1_opy_.framework)
    file_name = bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧண")
    file_path = os.path.abspath(file_name)
    bstack1l111111_opy_ = open(file_path, bstack11l11l_opy_ (u"ࠬࡽࠧத"))
    bstack1l111111_opy_.write(bstack1l11ll11_opy_)
    bstack1l111111_opy_.close()
    logger.info(bstack1l11l1l1ll_opy_)
    try:
      os.environ[bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ஥")] = bstack11ll1ll1_opy_.framework if bstack11ll1ll1_opy_.framework != None else bstack11l11l_opy_ (u"ࠢࠣ஦")
      config = yaml.safe_load(bstack1l11ll11_opy_)
      config[bstack11l11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ஧")] = bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨந")
      bstack1l1l1l1lll_opy_(bstack111l1ll1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1lll1l111_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1111l1l1_opy_.format(str(e)))
def bstack1l1l1l1lll_opy_(bstack11l1lllll_opy_, config, bstack1l11llll11_opy_={}):
  global bstack1llllll1l_opy_
  global bstack1l1lll11l1_opy_
  if not config:
    return
  bstack1l1lll111l_opy_ = bstack1lllllll1_opy_ if not bstack1llllll1l_opy_ else (
    bstack1ll1l111ll_opy_ if bstack11l11l_opy_ (u"ࠪࡥࡵࡶࠧன") in config else bstack1111l1ll_opy_)
  bstack1l1l111l_opy_ = False
  bstack1ll111ll1_opy_ = False
  if bstack1llllll1l_opy_ is True:
      if bstack11l11l_opy_ (u"ࠫࡦࡶࡰࠨப") in config:
          bstack1l1l111l_opy_ = True
      else:
          bstack1ll111ll1_opy_ = True
  bstack1l1l1l1l11_opy_ = {
      bstack11l11l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ஫"): bstack1ll1l1ll1l_opy_.bstack111llllll_opy_(bstack1l1lll11l1_opy_),
      bstack11l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭஬"): bstack1lll1ll11_opy_.bstack1llll1111_opy_(config),
      bstack11l11l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭஭"): config.get(bstack11l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧம"), False),
      bstack11l11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫய"): bstack1ll111ll1_opy_,
      bstack11l11l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩர"): bstack1l1l111l_opy_
  }
  data = {
    bstack11l11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ற"): config[bstack11l11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧல")],
    bstack11l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩள"): config[bstack11l11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪழ")],
    bstack11l11l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬவ"): bstack11l1lllll_opy_,
    bstack11l11l_opy_ (u"ࠩࡧࡩࡹ࡫ࡣࡵࡧࡧࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ஶ"): os.environ.get(bstack11l11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬஷ"), bstack1l1lll11l1_opy_),
    bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ஸ"): bstack1l1111l11_opy_,
    bstack11l11l_opy_ (u"ࠬࡵࡰࡵ࡫ࡰࡥࡱࡥࡨࡶࡤࡢࡹࡷࡲࠧஹ"): bstack11l1llll1_opy_(),
    bstack11l11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩ஺"): {
      bstack11l11l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ஻"): str(config[bstack11l11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ஼")]) if bstack11l11l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ஽") in config else bstack11l11l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦா"),
      bstack11l11l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ி"): sys.version,
      bstack11l11l_opy_ (u"ࠬࡸࡥࡧࡧࡵࡶࡪࡸࠧீ"): bstack1lll1l11l_opy_(os.getenv(bstack11l11l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠣு"), bstack11l11l_opy_ (u"ࠢࠣூ"))),
      bstack11l11l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ௃"): bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௄"),
      bstack11l11l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ௅"): bstack1l1lll111l_opy_,
      bstack11l11l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩெ"): bstack1l1l1l1l11_opy_,
      bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡥࡵࡶ࡫ࡧࠫே"): os.environ[bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫை")],
      bstack11l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ௉"): bstack1ll1l1111l_opy_(os.environ.get(bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪொ"), bstack1l1lll11l1_opy_)),
      bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬோ"): config[bstack11l11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ௌ")] if config[bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫்ࠧ")] else bstack11l11l_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨ௎"),
      bstack11l11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௏"): str(config[bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩௐ")]) if bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௑") in config else bstack11l11l_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥ௒"),
      bstack11l11l_opy_ (u"ࠪࡳࡸ࠭௓"): sys.platform,
      bstack11l11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭௔"): socket.gethostname()
    }
  }
  update(data[bstack11l11l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ௕")], bstack1l11llll11_opy_)
  try:
    response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"࠭ࡐࡐࡕࡗࠫ௖"), bstack1ll1llll1_opy_(bstack1lllllll1l_opy_), data, {
      bstack11l11l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬௗ"): (config[bstack11l11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ௘")], config[bstack11l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ௙")])
    })
    if response:
      logger.debug(bstack1ll1l11l_opy_.format(bstack11l1lllll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1lll1l1lll_opy_.format(str(e)))
def bstack1lll1l11l_opy_(framework):
  return bstack11l11l_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢ௚").format(str(framework), __version__) if framework else bstack11l11l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ௛").format(
    __version__)
def bstack1lll11l1ll_opy_():
  global CONFIG
  global bstack11111l1ll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1111ll11_opy_()
    logger.debug(bstack1llll11ll_opy_.format(str(CONFIG)))
    bstack11111l1ll_opy_ = bstack111ll1l1_opy_.bstack1111111l_opy_(CONFIG, bstack11111l1ll_opy_)
    bstack1ll11ll1l_opy_()
  except Exception as e:
    logger.error(bstack11l11l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤ௜") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll11l11l1_opy_
  atexit.register(bstack1l11ll1ll_opy_)
  signal.signal(signal.SIGINT, bstack1lll11ll1l_opy_)
  signal.signal(signal.SIGTERM, bstack1lll11ll1l_opy_)
def bstack1ll11l11l1_opy_(exctype, value, traceback):
  global bstack1ll1111lll_opy_
  try:
    for driver in bstack1ll1111lll_opy_:
      bstack1ll1l11l1_opy_(driver, bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௝"), bstack11l11l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ௞") + str(value))
  except Exception:
    pass
  bstack111l11lll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111l11lll_opy_(message=bstack11l11l_opy_ (u"ࠨࠩ௟"), bstack11l1llll_opy_ = False):
  global CONFIG
  bstack1l1l1ll11_opy_ = bstack11l11l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡇࡻࡧࡪࡶࡴࡪࡱࡱࠫ௠") if bstack11l1llll_opy_ else bstack11l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ௡")
  try:
    if message:
      bstack1l11llll11_opy_ = {
        bstack1l1l1ll11_opy_ : str(message)
      }
      bstack1l1l1l1lll_opy_(bstack11lll11ll_opy_, CONFIG, bstack1l11llll11_opy_)
    else:
      bstack1l1l1l1lll_opy_(bstack11lll11ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll111111_opy_.format(str(e)))
def bstack1ll111l1ll_opy_(bstack1lll1lll11_opy_, size):
  bstack1l1lll1111_opy_ = []
  while len(bstack1lll1lll11_opy_) > size:
    bstack1ll1l1lll_opy_ = bstack1lll1lll11_opy_[:size]
    bstack1l1lll1111_opy_.append(bstack1ll1l1lll_opy_)
    bstack1lll1lll11_opy_ = bstack1lll1lll11_opy_[size:]
  bstack1l1lll1111_opy_.append(bstack1lll1lll11_opy_)
  return bstack1l1lll1111_opy_
def bstack1ll1111l1l_opy_(args):
  if bstack11l11l_opy_ (u"ࠫ࠲ࡳࠧ௢") in args and bstack11l11l_opy_ (u"ࠬࡶࡤࡣࠩ௣") in args:
    return True
  return False
def run_on_browserstack(bstack11l111l1_opy_=None, bstack1lll111l11_opy_=None, bstack1l1l1l111l_opy_=False):
  global CONFIG
  global bstack1l11ll1111_opy_
  global bstack11l111ll_opy_
  global bstack1l1lll11l1_opy_
  bstack111l1lll_opy_ = bstack11l11l_opy_ (u"࠭ࠧ௤")
  bstack1l1111111_opy_(bstack1l1ll1lll1_opy_, logger)
  if bstack11l111l1_opy_ and isinstance(bstack11l111l1_opy_, str):
    bstack11l111l1_opy_ = eval(bstack11l111l1_opy_)
  if bstack11l111l1_opy_:
    CONFIG = bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ௥")]
    bstack1l11ll1111_opy_ = bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ௦")]
    bstack11l111ll_opy_ = bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ௧")]
    bstack111l11111_opy_.bstack1ll1ll1l11_opy_(bstack11l11l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ௨"), bstack11l111ll_opy_)
    bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௩")
  if not bstack1l1l1l111l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack111lll11l_opy_)
      return
    if sys.argv[1] == bstack11l11l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௪") or sys.argv[1] == bstack11l11l_opy_ (u"࠭࠭ࡷࠩ௫"):
      logger.info(bstack11l11l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧ௬").format(__version__))
      return
    if sys.argv[1] == bstack11l11l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ௭"):
      bstack1ll11l1l1l_opy_()
      return
  args = sys.argv
  bstack1lll11l1ll_opy_()
  global bstack11llll1ll_opy_
  global bstack1ll11llll1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack11111lll_opy_
  global bstack1l11llll1l_opy_
  global bstack1l11ll1ll1_opy_
  global bstack11l111lll_opy_
  global bstack111lll1l1_opy_
  global bstack11l1ll11l_opy_
  global bstack1111l111l_opy_
  global bstack11l1lll1l_opy_
  bstack1ll11llll1_opy_ = len(CONFIG.get(bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௮"), []))
  if not bstack111l1lll_opy_:
    if args[1] == bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௯") or args[1] == bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ௰"):
      bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௱")
      args = args[2:]
    elif args[1] == bstack11l11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௲"):
      bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௳")
      args = args[2:]
    elif args[1] == bstack11l11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௴"):
      bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ௵")
      args = args[2:]
    elif args[1] == bstack11l11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௶"):
      bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௷")
      args = args[2:]
    elif args[1] == bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௸"):
      bstack111l1lll_opy_ = bstack11l11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௹")
      args = args[2:]
    elif args[1] == bstack11l11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ௺"):
      bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ௻")
      args = args[2:]
    else:
      if not bstack11l11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௼") in CONFIG or str(CONFIG[bstack11l11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭௽")]).lower() in [bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௾"), bstack11l11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭௿")]:
        bstack111l1lll_opy_ = bstack11l11l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ఀ")
        args = args[1:]
      elif str(CONFIG[bstack11l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఁ")]).lower() == bstack11l11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧం"):
        bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨః")
        args = args[1:]
      elif str(CONFIG[bstack11l11l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ఄ")]).lower() == bstack11l11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪఅ"):
        bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫఆ")
        args = args[1:]
      elif str(CONFIG[bstack11l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩఇ")]).lower() == bstack11l11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧఈ"):
        bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨఉ")
        args = args[1:]
      elif str(CONFIG[bstack11l11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬఊ")]).lower() == bstack11l11l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪఋ"):
        bstack111l1lll_opy_ = bstack11l11l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫఌ")
        args = args[1:]
      else:
        os.environ[bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ఍")] = bstack111l1lll_opy_
        bstack11l1l1lll_opy_(bstack1lllll1lll_opy_)
  os.environ[bstack11l11l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧఎ")] = bstack111l1lll_opy_
  bstack1l1lll11l1_opy_ = bstack111l1lll_opy_
  global bstack1lll11l1l1_opy_
  if bstack11l111l1_opy_:
    try:
      os.environ[bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩఏ")] = bstack111l1lll_opy_
      bstack1l1l1l1lll_opy_(bstack11l111l11_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll111111_opy_.format(str(e)))
  global bstack1l11l1ll1l_opy_
  global bstack1lll11111l_opy_
  global bstack11111ll1l_opy_
  global bstack1lll11ll1_opy_
  global bstack1l1ll11l11_opy_
  global bstack11lll1l1_opy_
  global bstack1l1l1l1l_opy_
  global bstack1l11lll1ll_opy_
  global bstack11l11l111_opy_
  global bstack1l11llllll_opy_
  global bstack1l1l1111_opy_
  global bstack1lll1l1ll1_opy_
  global bstack1ll11ll11_opy_
  global bstack11l1l111l_opy_
  global bstack1ll11l1ll_opy_
  global bstack1ll1ll11ll_opy_
  global bstack11ll1l11l_opy_
  global bstack1111l11l_opy_
  global bstack111ll111l_opy_
  global bstack111llll11_opy_
  global bstack1l11lll11l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l1ll1l_opy_ = webdriver.Remote.__init__
    bstack1lll11111l_opy_ = WebDriver.quit
    bstack1lll1l1ll1_opy_ = WebDriver.close
    bstack1ll11l1ll_opy_ = WebDriver.get
    bstack1l11lll11l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll11l1l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack1ll1l1ll_opy_
    from QWeb.keywords import browser
    bstack1ll1l1ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111l1111l_opy_(CONFIG) and bstack1llll11l_opy_():
    if bstack1l1ll1l1_opy_() < version.parse(bstack1111l11ll_opy_):
      logger.error(bstack1ll111l1_opy_.format(bstack1l1ll1l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1ll1ll11ll_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l1l11ll1l_opy_.format(str(e)))
  if not CONFIG.get(bstack11l11l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪఐ"), False) and not bstack11l111l1_opy_:
    logger.info(bstack111ll111_opy_)
  if bstack111l1lll_opy_ != bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ఑") or (bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪఒ") and not bstack11l111l1_opy_):
    bstack1ll1ll1lll_opy_()
  if (bstack111l1lll_opy_ in [bstack11l11l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪఓ"), bstack11l11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫఔ"), bstack11l11l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧక")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1l1llll1_opy_
        bstack11lll1l1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1llll111ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1l1ll1111_opy_
        bstack1l1ll11l11_opy_ = bstack1l1ll1111_opy_.close
      except Exception as e:
        logger.debug(bstack1ll1ll1l1_opy_ + str(e))
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1llll111ll_opy_)
    if bstack111l1lll_opy_ != bstack11l11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨఖ"):
      bstack1llll1lll_opy_()
    bstack11111ll1l_opy_ = Output.start_test
    bstack1lll11ll1_opy_ = Output.end_test
    bstack1l1l1l1l_opy_ = TestStatus.__init__
    bstack11l11l111_opy_ = pabot._run
    bstack1l11llllll_opy_ = QueueItem.__init__
    bstack1l1l1111_opy_ = pabot._create_command_for_execution
    bstack111ll111l_opy_ = pabot._report_results
  if bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨగ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1ll1ll1111_opy_)
    bstack1ll11ll11_opy_ = Runner.run_hook
    bstack11l1l111l_opy_ = Step.run
  if bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩఘ"):
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
      logger.debug(bstack11l11l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫఙ"))
  try:
    framework_name = bstack11l11l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪచ") if bstack111l1lll_opy_ in [bstack11l11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫఛ"), bstack11l11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬజ"), bstack11l11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨఝ")] else bstack1ll11111ll_opy_(bstack111l1lll_opy_)
    bstack1ll1l1ll1l_opy_.launch(CONFIG, {
      bstack11l11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩఞ"): bstack11l11l_opy_ (u"ࠩࡾ࠴ࢂ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨట").format(framework_name) if bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪఠ") and bstack1111ll1l_opy_() else framework_name,
      bstack11l11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨడ"): bstack1ll1l1111l_opy_(framework_name),
      bstack11l11l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪఢ"): __version__,
      bstack11l11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧణ"): bstack111l1lll_opy_
    })
  except Exception as e:
    logger.debug(bstack11llll11l_opy_.format(bstack11l11l_opy_ (u"ࠧࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧత"), str(e)))
  if bstack111l1lll_opy_ in bstack1l1111lll_opy_:
    try:
      framework_name = bstack11l11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧథ") if bstack111l1lll_opy_ in [bstack11l11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨద"), bstack11l11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩధ")] else bstack111l1lll_opy_
      if bstack1llllll1l_opy_ and bstack11l11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫన") in CONFIG and CONFIG[bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ఩")] == True:
        if bstack11l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ప") in CONFIG:
          os.environ[bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨఫ")] = os.getenv(bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩబ"), json.dumps(CONFIG[bstack11l11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩభ")]))
          CONFIG[bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪమ")].pop(bstack11l11l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩయ"), None)
          CONFIG[bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬర")].pop(bstack11l11l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫఱ"), None)
        bstack11llll111_opy_, bstack1lll1ll1l_opy_ = bstack1lll1ll11_opy_.bstack1ll111ll11_opy_(CONFIG, bstack111l1lll_opy_, bstack1ll1l1111l_opy_(framework_name), str(bstack1l1ll1l1_opy_()))
        if not bstack11llll111_opy_ is None:
          os.environ[bstack11l11l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬల")] = bstack11llll111_opy_
          os.environ[bstack11l11l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡗࡉࡘ࡚࡟ࡓࡗࡑࡣࡎࡊࠧళ")] = str(bstack1lll1ll1l_opy_)
    except Exception as e:
      logger.debug(bstack11llll11l_opy_.format(bstack11l11l_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩఴ"), str(e)))
  if bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪవ"):
    bstack1lll1l1l1l_opy_ = True
    if bstack11l111l1_opy_ and bstack1l1l1l111l_opy_:
      bstack1l11ll1ll1_opy_ = CONFIG.get(bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨశ"), {}).get(bstack11l11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧష"))
      bstack1l1l1111l_opy_(bstack1lllll1l1_opy_)
    elif bstack11l111l1_opy_:
      bstack1l11ll1ll1_opy_ = CONFIG.get(bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪస"), {}).get(bstack11l11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩహ"))
      global bstack1ll1111lll_opy_
      try:
        if bstack1ll1111l1l_opy_(bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ఺")]) and multiprocessing.current_process().name == bstack11l11l_opy_ (u"ࠩ࠳ࠫ఻"):
          bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ఼࠭")].remove(bstack11l11l_opy_ (u"ࠫ࠲ࡳࠧఽ"))
          bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨా")].remove(bstack11l11l_opy_ (u"࠭ࡰࡥࡤࠪి"))
          bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪీ")] = bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫు")][0]
          with open(bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬూ")], bstack11l11l_opy_ (u"ࠪࡶࠬృ")) as f:
            bstack11111ll11_opy_ = f.read()
          bstack1l1l111l1l_opy_ = bstack11l11l_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࡤࡦࡨࠣࡱࡴࡪ࡟ࡣࡴࡨࡥࡰ࠮ࡳࡦ࡮ࡩ࠰ࠥࡧࡲࡨ࠮ࠣࡸࡪࡳࡰࡰࡴࡤࡶࡾࠦ࠽ࠡ࠲ࠬ࠾ࠏࠦࠠࡵࡴࡼ࠾ࠏࠦࠠࠡࠢࡤࡶ࡬ࠦ࠽ࠡࡵࡷࡶ࠭࡯࡮ࡵࠪࡤࡶ࡬࠯ࠫ࠲࠲ࠬࠎࠥࠦࡥࡹࡥࡨࡴࡹࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡤࡷࠥ࡫࠺ࠋࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࡵࡧࡠࡦࡥࠬࡸ࡫࡬ࡧ࠮ࡤࡶ࡬࠲ࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠫࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࡔࡩࡨ࠮ࡥࡱࡢࡦࡷ࡫ࡡ࡬ࠢࡀࠤࡲࡵࡤࡠࡤࡵࡩࡦࡱࠊࡑࡦࡥࠬ࠮࠴ࡳࡦࡶࡢࡸࡷࡧࡣࡦࠪࠬࡠࡳࠨࠢࠣౄ").format(str(bstack11l111l1_opy_))
          bstack1ll1l11lll_opy_ = bstack1l1l111l1l_opy_ + bstack11111ll11_opy_
          bstack1llll11111_opy_ = bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౅")] + bstack11l11l_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨె")
          with open(bstack1llll11111_opy_, bstack11l11l_opy_ (u"ࠧࡸࠩే")):
            pass
          with open(bstack1llll11111_opy_, bstack11l11l_opy_ (u"ࠣࡹ࠮ࠦై")) as f:
            f.write(bstack1ll1l11lll_opy_)
          import subprocess
          bstack11ll1ll1l_opy_ = subprocess.run([bstack11l11l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤ౉"), bstack1llll11111_opy_])
          if os.path.exists(bstack1llll11111_opy_):
            os.unlink(bstack1llll11111_opy_)
          os._exit(bstack11ll1ll1l_opy_.returncode)
        else:
          if bstack1ll1111l1l_opy_(bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ొ")]):
            bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧో")].remove(bstack11l11l_opy_ (u"ࠬ࠳࡭ࠨౌ"))
            bstack11l111l1_opy_[bstack11l11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦ్ࠩ")].remove(bstack11l11l_opy_ (u"ࠧࡱࡦࡥࠫ౎"))
            bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౏")] = bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౐")][0]
          bstack1l1l1111l_opy_(bstack1lllll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭౑")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11l11l_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭౒")] = bstack11l11l_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ౓")
          mod_globals[bstack11l11l_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ౔")] = os.path.abspath(bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧౕࠪ")])
          exec(open(bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨౖࠫ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11l11l_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩ౗").format(str(e)))
          for driver in bstack1ll1111lll_opy_:
            bstack1lll111l11_opy_.append({
              bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨౘ"): bstack11l111l1_opy_[bstack11l11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧౙ")],
              bstack11l11l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫౚ"): str(e),
              bstack11l11l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ౛"): multiprocessing.current_process().name
            })
            bstack1ll1l11l1_opy_(driver, bstack11l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ౜"), bstack11l11l_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦౝ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1ll1111lll_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11l111ll_opy_, CONFIG, logger)
      bstack1l1ll111ll_opy_()
      bstack11ll1l11_opy_()
      bstack11111l11l_opy_ = {
        bstack11l11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౞"): args[0],
        bstack11l11l_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪ౟"): CONFIG,
        bstack11l11l_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬౠ"): bstack1l11ll1111_opy_,
        bstack11l11l_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧౡ"): bstack11l111ll_opy_
      }
      percy.bstack1l11l1ll1_opy_()
      if bstack11l11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ") in CONFIG:
        bstack1l1lll11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1l1lllllll_opy_ = manager.list()
        if bstack1ll1111l1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11l11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪౣ")]):
            if index == 0:
              bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౤")] = args
            bstack1l1lll11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11111l11l_opy_, bstack1l1lllllll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ౥")]):
            bstack1l1lll11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11111l11l_opy_, bstack1l1lllllll_opy_)))
        for t in bstack1l1lll11_opy_:
          t.start()
        for t in bstack1l1lll11_opy_:
          t.join()
        bstack111lll1l1_opy_ = list(bstack1l1lllllll_opy_)
      else:
        if bstack1ll1111l1l_opy_(args):
          bstack11111l11l_opy_[bstack11l11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭౦")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11111l11l_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1l1111l_opy_(bstack1lllll1l1_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11l11l_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭౧")] = bstack11l11l_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ౨")
          mod_globals[bstack11l11l_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨ౩")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭౪") or bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ౫"):
    percy.init(bstack11l111ll_opy_, CONFIG, logger)
    percy.bstack1l11l1ll1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1llll111ll_opy_)
    bstack1l1ll111ll_opy_()
    bstack1l1l1111l_opy_(bstack1l1l1l1l1l_opy_)
    if bstack1llllll1l_opy_ and bstack11l11l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ౬") in args:
      i = args.index(bstack11l11l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ౭"))
      args.pop(i)
      args.pop(i)
    if bstack1llllll1l_opy_:
      args.insert(0, str(bstack11llll1ll_opy_))
      args.insert(0, str(bstack11l11l_opy_ (u"ࠫ࠲࠳ࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ౮")))
    if bstack1ll1l1ll1l_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1ll1ll1l1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1l1l11lll1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11l11l_opy_ (u"ࠧࡘࡏࡃࡑࡗࡣࡔࡖࡔࡊࡑࡑࡗࠧ౯"),
        ).parse_args(bstack1ll1ll1l1l_opy_)
        bstack1l1lll1lll_opy_ = args.index(bstack1ll1ll1l1l_opy_[0]) if len(bstack1ll1ll1l1l_opy_) > 0 else len(args)
        args.insert(bstack1l1lll1lll_opy_, str(bstack11l11l_opy_ (u"࠭࠭࠮࡮࡬ࡷࡹ࡫࡮ࡦࡴࠪ౰")))
        args.insert(bstack1l1lll1lll_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲ࠯ࡲࡼࠫ౱"))))
        if bstack1l1ll111l1_opy_(os.environ.get(bstack11l11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭౲"))) and str(os.environ.get(bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘ࠭౳"), bstack11l11l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ౴"))) != bstack11l11l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ౵"):
          for bstack111llll1l_opy_ in bstack1l1l11lll1_opy_:
            args.remove(bstack111llll1l_opy_)
          bstack1l1llll1l_opy_ = os.environ.get(bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩ౶")).split(bstack11l11l_opy_ (u"࠭ࠬࠨ౷"))
          for bstack11llll1l_opy_ in bstack1l1llll1l_opy_:
            args.append(bstack11llll1l_opy_)
      except Exception as e:
        logger.error(bstack11l11l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡴࡵࡣࡦ࡬࡮ࡴࡧࠡ࡮࡬ࡷࡹ࡫࡮ࡦࡴࠣࡪࡴࡸࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࠡࡇࡵࡶࡴࡸࠠ࠮ࠢࠥ౸").format(e))
    pabot.main(args)
  elif bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ౹"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1llll111ll_opy_)
    for a in args:
      if bstack11l11l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨ౺") in a:
        bstack1l11llll1l_opy_ = int(a.split(bstack11l11l_opy_ (u"ࠪ࠾ࠬ౻"))[1])
      if bstack11l11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ౼") in a:
        bstack1l11ll1ll1_opy_ = str(a.split(bstack11l11l_opy_ (u"ࠬࡀࠧ౽"))[1])
      if bstack11l11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭౾") in a:
        bstack11l111lll_opy_ = str(a.split(bstack11l11l_opy_ (u"ࠧ࠻ࠩ౿"))[1])
    bstack1l1llllll_opy_ = None
    if bstack11l11l_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧಀ") in args:
      i = args.index(bstack11l11l_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨಁ"))
      args.pop(i)
      bstack1l1llllll_opy_ = args.pop(i)
    if bstack1l1llllll_opy_ is not None:
      global bstack1ll1ll111l_opy_
      bstack1ll1ll111l_opy_ = bstack1l1llllll_opy_
    bstack1l1l1111l_opy_(bstack1l1l1l1l1l_opy_)
    run_cli(args)
    if bstack11l11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧಂ") in multiprocessing.current_process().__dict__.keys():
      for bstack111111l1l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll111l11_opy_.append(bstack111111l1l_opy_)
  elif bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಃ"):
    percy.init(bstack11l111ll_opy_, CONFIG, logger)
    percy.bstack1l11l1ll1_opy_()
    bstack1ll11lllll_opy_ = bstack1l1l1ll1ll_opy_(args, logger, CONFIG, bstack1llllll1l_opy_)
    bstack1ll11lllll_opy_.bstack11ll11l11_opy_()
    bstack1l1ll111ll_opy_()
    bstack11111lll_opy_ = True
    bstack1111l111l_opy_ = bstack1ll11lllll_opy_.bstack111ll1l1l_opy_()
    bstack1ll11lllll_opy_.bstack11111l11l_opy_(bstack1111l1lll_opy_)
    bstack11l1111l1_opy_ = bstack1ll11lllll_opy_.bstack1ll1l1l11l_opy_(bstack1l1ll1lll_opy_, {
      bstack11l11l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭಄"): bstack1l11ll1111_opy_,
      bstack11l11l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨಅ"): bstack11l111ll_opy_,
      bstack11l11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪಆ"): bstack1llllll1l_opy_
    })
    try:
      bstack1l11lllll_opy_, bstack1l1llll111_opy_ = map(list, zip(*bstack11l1111l1_opy_))
      bstack11l1ll11l_opy_ = bstack1l11lllll_opy_[0]
      for status_code in bstack1l1llll111_opy_:
        if status_code != 0:
          bstack11l1lll1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡧࡶࡦࠢࡨࡶࡷࡵࡲࡴࠢࡤࡲࡩࠦࡳࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠲ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࠼ࠣࡿࢂࠨಇ").format(str(e)))
  elif bstack111l1lll_opy_ == bstack11l11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩಈ"):
    try:
      from behave.__main__ import main as bstack1ll1l111l1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1l1l1lll1_opy_(e, bstack1ll1ll1111_opy_)
    bstack1l1ll111ll_opy_()
    bstack11111lll_opy_ = True
    bstack11l1l1111_opy_ = 1
    if bstack11l11l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪಉ") in CONFIG:
      bstack11l1l1111_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫಊ")]
    bstack1lll1l111l_opy_ = int(bstack11l1l1111_opy_) * int(len(CONFIG[bstack11l11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨಋ")]))
    config = Configuration(args)
    bstack1ll1l1l111_opy_ = config.paths
    if len(bstack1ll1l1l111_opy_) == 0:
      import glob
      pattern = bstack11l11l_opy_ (u"࠭ࠪࠫ࠱࠭࠲࡫࡫ࡡࡵࡷࡵࡩࠬಌ")
      bstack111lll1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack111lll1l_opy_)
      config = Configuration(args)
      bstack1ll1l1l111_opy_ = config.paths
    bstack1l1l111ll_opy_ = [os.path.normpath(item) for item in bstack1ll1l1l111_opy_]
    bstack11l1111l_opy_ = [os.path.normpath(item) for item in args]
    bstack111lll111_opy_ = [item for item in bstack11l1111l_opy_ if item not in bstack1l1l111ll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11l11l_opy_ (u"ࠧࡸ࡫ࡱࡨࡴࡽࡳࠨ಍"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1l111ll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111111ll_opy_)))
                    for bstack1111111ll_opy_ in bstack1l1l111ll_opy_]
    bstack11l11ll1l_opy_ = []
    for spec in bstack1l1l111ll_opy_:
      bstack1l1llllll1_opy_ = []
      bstack1l1llllll1_opy_ += bstack111lll111_opy_
      bstack1l1llllll1_opy_.append(spec)
      bstack11l11ll1l_opy_.append(bstack1l1llllll1_opy_)
    execution_items = []
    for bstack1l1llllll1_opy_ in bstack11l11ll1l_opy_:
      for index, _ in enumerate(CONFIG[bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫಎ")]):
        item = {}
        item[bstack11l11l_opy_ (u"ࠩࡤࡶ࡬࠭ಏ")] = bstack11l11l_opy_ (u"ࠪࠤࠬಐ").join(bstack1l1llllll1_opy_)
        item[bstack11l11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ಑")] = index
        execution_items.append(item)
    bstack111ll1ll1_opy_ = bstack1ll111l1ll_opy_(execution_items, bstack1lll1l111l_opy_)
    for execution_item in bstack111ll1ll1_opy_:
      bstack1l1lll11_opy_ = []
      for item in execution_item:
        bstack1l1lll11_opy_.append(bstack111l11l11_opy_(name=str(item[bstack11l11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫಒ")]),
                                             target=bstack1l111111l_opy_,
                                             args=(item[bstack11l11l_opy_ (u"࠭ࡡࡳࡩࠪಓ")],)))
      for t in bstack1l1lll11_opy_:
        t.start()
      for t in bstack1l1lll11_opy_:
        t.join()
  else:
    bstack11l1l1lll_opy_(bstack1lllll1lll_opy_)
  if not bstack11l111l1_opy_:
    bstack1l11ll111l_opy_()
  bstack111ll1l1_opy_.bstack1l1ll1l1ll_opy_()
def browserstack_initialize(bstack1ll11111_opy_=None):
  run_on_browserstack(bstack1ll11111_opy_, None, True)
def bstack1l11ll111l_opy_():
  global CONFIG
  global bstack1l1lll11l1_opy_
  global bstack11l1lll1l_opy_
  global bstack1ll1lll11_opy_
  bstack1ll1l1ll1l_opy_.stop()
  bstack1ll1l1ll1l_opy_.bstack1ll11ll1l1_opy_()
  if bstack1lll1ll11_opy_.bstack1llll1111_opy_(CONFIG):
    bstack1lll1ll11_opy_.bstack111l11l1l_opy_()
  [bstack11lllll11_opy_, bstack11l1l1ll1_opy_] = get_build_link()
  if bstack11lllll11_opy_ is not None and bstack1l1ll11ll1_opy_() != -1:
    sessions = bstack1lll111111_opy_(bstack11lllll11_opy_)
    bstack1l111l11_opy_(sessions, bstack11l1l1ll1_opy_)
  if bstack1l1lll11l1_opy_ == bstack11l11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧಔ") and bstack11l1lll1l_opy_ != 0:
    sys.exit(bstack11l1lll1l_opy_)
  if bstack1l1lll11l1_opy_ == bstack11l11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨಕ") and bstack1ll1lll11_opy_ != 0:
    sys.exit(bstack1ll1lll11_opy_)
def bstack1ll11111ll_opy_(bstack111l1l11_opy_):
  if bstack111l1l11_opy_:
    return bstack111l1l11_opy_.capitalize()
  else:
    return bstack11l11l_opy_ (u"ࠩࠪಖ")
def bstack1ll1lll1_opy_(bstack1l1l11l11_opy_):
  if bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨಗ") in bstack1l1l11l11_opy_ and bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩಘ")] != bstack11l11l_opy_ (u"ࠬ࠭ಙ"):
    return bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫಚ")]
  else:
    bstack1ll1l111_opy_ = bstack11l11l_opy_ (u"ࠢࠣಛ")
    if bstack11l11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨಜ") in bstack1l1l11l11_opy_ and bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩಝ")] != None:
      bstack1ll1l111_opy_ += bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪಞ")] + bstack11l11l_opy_ (u"ࠦ࠱ࠦࠢಟ")
      if bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠬࡵࡳࠨಠ")] == bstack11l11l_opy_ (u"ࠨࡩࡰࡵࠥಡ"):
        bstack1ll1l111_opy_ += bstack11l11l_opy_ (u"ࠢࡪࡑࡖࠤࠧಢ")
      bstack1ll1l111_opy_ += (bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಣ")] or bstack11l11l_opy_ (u"ࠩࠪತ"))
      return bstack1ll1l111_opy_
    else:
      bstack1ll1l111_opy_ += bstack1ll11111ll_opy_(bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫಥ")]) + bstack11l11l_opy_ (u"ࠦࠥࠨದ") + (
              bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧಧ")] or bstack11l11l_opy_ (u"࠭ࠧನ")) + bstack11l11l_opy_ (u"ࠢ࠭ࠢࠥ಩")
      if bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠨࡱࡶࠫಪ")] == bstack11l11l_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥಫ"):
        bstack1ll1l111_opy_ += bstack11l11l_opy_ (u"࡛ࠥ࡮ࡴࠠࠣಬ")
      bstack1ll1l111_opy_ += bstack1l1l11l11_opy_[bstack11l11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨಭ")] or bstack11l11l_opy_ (u"ࠬ࠭ಮ")
      return bstack1ll1l111_opy_
def bstack1l1lll1l1l_opy_(bstack11l11111_opy_):
  if bstack11l11111_opy_ == bstack11l11l_opy_ (u"ࠨࡤࡰࡰࡨࠦಯ"):
    return bstack11l11l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪರ")
  elif bstack11l11111_opy_ == bstack11l11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣಱ"):
    return bstack11l11l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಲ")
  elif bstack11l11111_opy_ == bstack11l11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥಳ"):
    return bstack11l11l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ಴")
  elif bstack11l11111_opy_ == bstack11l11l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦವ"):
    return bstack11l11l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಶ")
  elif bstack11l11111_opy_ == bstack11l11l_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣಷ"):
    return bstack11l11l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ಸ")
  elif bstack11l11111_opy_ == bstack11l11l_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥಹ"):
    return bstack11l11l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫ಺")
  else:
    return bstack11l11l_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨ಻") + bstack1ll11111ll_opy_(
      bstack11l11111_opy_) + bstack11l11l_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁ಼ࠫ")
def bstack1l1l1lll_opy_(session):
  return bstack11l11l_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ࠭ಽ").format(
    session[bstack11l11l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯ࠫಾ")], bstack1ll1lll1_opy_(session), bstack1l1lll1l1l_opy_(session[bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧಿ")]),
    bstack1l1lll1l1l_opy_(session[bstack11l11l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩೀ")]),
    bstack1ll11111ll_opy_(session[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫು")] or session[bstack11l11l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫೂ")] or bstack11l11l_opy_ (u"ࠬ࠭ೃ")) + bstack11l11l_opy_ (u"ࠨࠠࠣೄ") + (session[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ೅")] or bstack11l11l_opy_ (u"ࠨࠩೆ")),
    session[bstack11l11l_opy_ (u"ࠩࡲࡷࠬೇ")] + bstack11l11l_opy_ (u"ࠥࠤࠧೈ") + session[bstack11l11l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ೉")], session[bstack11l11l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧೊ")] or bstack11l11l_opy_ (u"࠭ࠧೋ"),
    session[bstack11l11l_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫೌ")] if session[bstack11l11l_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸ್ࠬ")] else bstack11l11l_opy_ (u"ࠩࠪ೎"))
def bstack1l111l11_opy_(sessions, bstack11l1l1ll1_opy_):
  try:
    bstack111lllll_opy_ = bstack11l11l_opy_ (u"ࠥࠦ೏")
    if not os.path.exists(bstack1l11llll_opy_):
      os.mkdir(bstack1l11llll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l11l_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩ೐")), bstack11l11l_opy_ (u"ࠬࡸࠧ೑")) as f:
      bstack111lllll_opy_ = f.read()
    bstack111lllll_opy_ = bstack111lllll_opy_.replace(bstack11l11l_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪ೒"), str(len(sessions)))
    bstack111lllll_opy_ = bstack111lllll_opy_.replace(bstack11l11l_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧ೓"), bstack11l1l1ll1_opy_)
    bstack111lllll_opy_ = bstack111lllll_opy_.replace(bstack11l11l_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩ೔"),
                                              sessions[0].get(bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭ೕ")) if sessions[0] else bstack11l11l_opy_ (u"ࠪࠫೖ"))
    with open(os.path.join(bstack1l11llll_opy_, bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨ೗")), bstack11l11l_opy_ (u"ࠬࡽࠧ೘")) as stream:
      stream.write(bstack111lllll_opy_.split(bstack11l11l_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ೙"))[0])
      for session in sessions:
        stream.write(bstack1l1l1lll_opy_(session))
      stream.write(bstack111lllll_opy_.split(bstack11l11l_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ೚"))[1])
    logger.info(bstack11l11l_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫ೛").format(bstack1l11llll_opy_));
  except Exception as e:
    logger.debug(bstack11lll1ll_opy_.format(str(e)))
def bstack1lll111111_opy_(bstack11lllll11_opy_):
  global CONFIG
  try:
    host = bstack11l11l_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬ೜") if bstack11l11l_opy_ (u"ࠪࡥࡵࡶࠧೝ") in CONFIG else bstack11l11l_opy_ (u"ࠫࡦࡶࡩࠨೞ")
    user = CONFIG[bstack11l11l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ೟")]
    key = CONFIG[bstack11l11l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩೠ")]
    bstack1l11llll1_opy_ = bstack11l11l_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ೡ") if bstack11l11l_opy_ (u"ࠨࡣࡳࡴࠬೢ") in CONFIG else bstack11l11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫೣ")
    url = bstack11l11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨ೤").format(user, key, host, bstack1l11llll1_opy_,
                                                                                bstack11lllll11_opy_)
    headers = {
      bstack11l11l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪ೥"): bstack11l11l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ೦"),
    }
    proxies = bstack1ll111l1l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11l11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ೧")], response.json()))
  except Exception as e:
    logger.debug(bstack1ll11ll1_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1l1111l11_opy_
  try:
    if bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೨") in CONFIG:
      host = bstack11l11l_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ೩") if bstack11l11l_opy_ (u"ࠩࡤࡴࡵ࠭೪") in CONFIG else bstack11l11l_opy_ (u"ࠪࡥࡵ࡯ࠧ೫")
      user = CONFIG[bstack11l11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭೬")]
      key = CONFIG[bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ೭")]
      bstack1l11llll1_opy_ = bstack11l11l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ೮") if bstack11l11l_opy_ (u"ࠧࡢࡲࡳࠫ೯") in CONFIG else bstack11l11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ೰")
      url = bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩೱ").format(user, key, host, bstack1l11llll1_opy_)
      headers = {
        bstack11l11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩೲ"): bstack11l11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧೳ"),
      }
      if bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ೴") in CONFIG:
        params = {bstack11l11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೵"): CONFIG[bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ೶")], bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೷"): CONFIG[bstack11l11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೸")]}
      else:
        params = {bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ೹"): CONFIG[bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೺")]}
      proxies = bstack1ll111l1l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1ll11111l1_opy_ = response.json()[0][bstack11l11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ೻")]
        if bstack1ll11111l1_opy_:
          bstack11l1l1ll1_opy_ = bstack1ll11111l1_opy_[bstack11l11l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪ೼")].split(bstack11l11l_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭೽"))[0] + bstack11l11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩ೾") + bstack1ll11111l1_opy_[
            bstack11l11l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ೿")]
          logger.info(bstack1l1l11l111_opy_.format(bstack11l1l1ll1_opy_))
          bstack1l1111l11_opy_ = bstack1ll11111l1_opy_[bstack11l11l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ഀ")]
          bstack1l1ll111l_opy_ = CONFIG[bstack11l11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧഁ")]
          if bstack11l11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧം") in CONFIG:
            bstack1l1ll111l_opy_ += bstack11l11l_opy_ (u"࠭ࠠࠨഃ") + CONFIG[bstack11l11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩഄ")]
          if bstack1l1ll111l_opy_ != bstack1ll11111l1_opy_[bstack11l11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭അ")]:
            logger.debug(bstack11ll11lll_opy_.format(bstack1ll11111l1_opy_[bstack11l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧആ")], bstack1l1ll111l_opy_))
          return [bstack1ll11111l1_opy_[bstack11l11l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ഇ")], bstack11l1l1ll1_opy_]
    else:
      logger.warn(bstack1l11111l_opy_)
  except Exception as e:
    logger.debug(bstack11llll11_opy_.format(str(e)))
  return [None, None]
def bstack1ll11lll11_opy_(url, bstack1ll111ll1l_opy_=False):
  global CONFIG
  global bstack1ll1l11l1l_opy_
  if not bstack1ll1l11l1l_opy_:
    hostname = bstack111l1111_opy_(url)
    is_private = bstack1111ll1l1_opy_(hostname)
    if (bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨഈ") in CONFIG and not bstack1l1ll111l1_opy_(CONFIG[bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩഉ")])) and (is_private or bstack1ll111ll1l_opy_):
      bstack1ll1l11l1l_opy_ = hostname
def bstack111l1111_opy_(url):
  return urlparse(url).hostname
def bstack1111ll1l1_opy_(hostname):
  for bstack111ll11l_opy_ in bstack1lll1ll1ll_opy_:
    regex = re.compile(bstack111ll11l_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack11l11lll1_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11llll1l_opy_
  bstack111l111l1_opy_ = not (bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪഊ"), None) and bstack111111ll_opy_(
          threading.current_thread(), bstack11l11l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ഋ"), None))
  bstack111ll1l11_opy_ = getattr(driver, bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨഌ"), None) != True
  if not bstack1lll1ll11_opy_.bstack1l1ll1llll_opy_(CONFIG, bstack1l11llll1l_opy_) or (bstack111ll1l11_opy_ and bstack111l111l1_opy_):
    logger.warning(bstack11l11l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧ഍"))
    return {}
  try:
    logger.debug(bstack11l11l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧഎ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1l1ll1_opy_.bstack1l1l1l11l_opy_)
    return results
  except Exception:
    logger.error(bstack11l11l_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨഏ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11llll1l_opy_
  bstack111l111l1_opy_ = not (bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩഐ"), None) and bstack111111ll_opy_(
          threading.current_thread(), bstack11l11l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ഑"), None))
  bstack111ll1l11_opy_ = getattr(driver, bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧഒ"), None) != True
  if not bstack1lll1ll11_opy_.bstack1l1ll1llll_opy_(CONFIG, bstack1l11llll1l_opy_) or (bstack111ll1l11_opy_ and bstack111l111l1_opy_):
    logger.warning(bstack11l11l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧഓ"))
    return {}
  try:
    logger.debug(bstack11l11l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧഔ"))
    logger.debug(perform_scan(driver))
    bstack1ll1111ll_opy_ = driver.execute_async_script(bstack1l1l1ll1_opy_.bstack1llll1l11l_opy_)
    return bstack1ll1111ll_opy_
  except Exception:
    logger.error(bstack11l11l_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦക"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l11llll1l_opy_
  bstack111l111l1_opy_ = not (bstack111111ll_opy_(threading.current_thread(), bstack11l11l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨഖ"), None) and bstack111111ll_opy_(
          threading.current_thread(), bstack11l11l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫഗ"), None))
  bstack111ll1l11_opy_ = getattr(driver, bstack11l11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ഘ"), None) != True
  if not bstack1lll1ll11_opy_.bstack1l1ll1llll_opy_(CONFIG, bstack1l11llll1l_opy_) or (bstack111ll1l11_opy_ and bstack111l111l1_opy_):
    logger.warning(bstack11l11l_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤങ"))
    return {}
  try:
    bstack1l11l1l111_opy_ = driver.execute_async_script(bstack1l1l1ll1_opy_.perform_scan, {bstack11l11l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨച"): kwargs.get(bstack11l11l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪഛ"), None) or bstack11l11l_opy_ (u"ࠪࠫജ")})
    return bstack1l11l1l111_opy_
  except Exception:
    logger.error(bstack11l11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥഝ"))
    return {}