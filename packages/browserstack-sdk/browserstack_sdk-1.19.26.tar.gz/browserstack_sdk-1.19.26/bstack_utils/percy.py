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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1ll1llll1_opy_, bstack1llll11l1_opy_
class bstack11l11lll_opy_:
  working_dir = os.getcwd()
  bstack1l1llll1ll_opy_ = False
  config = {}
  binary_path = bstack11l11l_opy_ (u"ࠩࠪᐛ")
  bstack111111111l_opy_ = bstack11l11l_opy_ (u"ࠪࠫᐜ")
  bstack11lll1l1l_opy_ = False
  bstack1111l1l111_opy_ = None
  bstack11111l11ll_opy_ = {}
  bstack11111ll111_opy_ = 300
  bstack11111llll1_opy_ = False
  logger = None
  bstack1111l1l1ll_opy_ = False
  bstack11111l1111_opy_ = bstack11l11l_opy_ (u"ࠫࠬᐝ")
  bstack111111llll_opy_ = {
    bstack11l11l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᐞ") : 1,
    bstack11l11l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧᐟ") : 2,
    bstack11l11l_opy_ (u"ࠧࡦࡦࡪࡩࠬᐠ") : 3,
    bstack11l11l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨᐡ") : 4
  }
  def __init__(self) -> None: pass
  def bstack11111l1l11_opy_(self):
    bstack11111lll1l_opy_ = bstack11l11l_opy_ (u"ࠩࠪᐢ")
    bstack1llllllll1l_opy_ = sys.platform
    bstack1lllllllll1_opy_ = bstack11l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᐣ")
    if re.match(bstack11l11l_opy_ (u"ࠦࡩࡧࡲࡸ࡫ࡱࢀࡲࡧࡣࠡࡱࡶࠦᐤ"), bstack1llllllll1l_opy_) != None:
      bstack11111lll1l_opy_ = bstack11l111lll1_opy_ + bstack11l11l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡵࡳࡹ࠰ࡽ࡭ࡵࠨᐥ")
      self.bstack11111l1111_opy_ = bstack11l11l_opy_ (u"࠭࡭ࡢࡥࠪᐦ")
    elif re.match(bstack11l11l_opy_ (u"ࠢ࡮ࡵࡺ࡭ࡳࢂ࡭ࡴࡻࡶࢀࡲ࡯࡮ࡨࡹࡿࡧࡾ࡭ࡷࡪࡰࡿࡦࡨࡩࡷࡪࡰࡿࡻ࡮ࡴࡣࡦࡾࡨࡱࡨࢂࡷࡪࡰ࠶࠶ࠧᐧ"), bstack1llllllll1l_opy_) != None:
      bstack11111lll1l_opy_ = bstack11l111lll1_opy_ + bstack11l11l_opy_ (u"ࠣ࠱ࡳࡩࡷࡩࡹ࠮ࡹ࡬ࡲ࠳ࢀࡩࡱࠤᐨ")
      bstack1lllllllll1_opy_ = bstack11l11l_opy_ (u"ࠤࡳࡩࡷࡩࡹ࠯ࡧࡻࡩࠧᐩ")
      self.bstack11111l1111_opy_ = bstack11l11l_opy_ (u"ࠪࡻ࡮ࡴࠧᐪ")
    else:
      bstack11111lll1l_opy_ = bstack11l111lll1_opy_ + bstack11l11l_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡱ࡯࡮ࡶࡺ࠱ࡾ࡮ࡶࠢᐫ")
      self.bstack11111l1111_opy_ = bstack11l11l_opy_ (u"ࠬࡲࡩ࡯ࡷࡻࠫᐬ")
    return bstack11111lll1l_opy_, bstack1lllllllll1_opy_
  def bstack1lllllll1ll_opy_(self):
    try:
      bstack1111111ll1_opy_ = [os.path.join(expanduser(bstack11l11l_opy_ (u"ࠨࡾࠣᐭ")), bstack11l11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᐮ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1111111ll1_opy_:
        if(self.bstack11111lll11_opy_(path)):
          return path
      raise bstack11l11l_opy_ (u"ࠣࡗࡱࡥࡱࡨࡥࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠧᐯ")
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠦࡰࡢࡶ࡫ࠤ࡫ࡵࡲࠡࡲࡨࡶࡨࡿࠠࡥࡱࡺࡲࡱࡵࡡࡥ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠭ࠡࡽࢀࠦᐰ").format(e))
  def bstack11111lll11_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack11111l111l_opy_(self, bstack11111lll1l_opy_, bstack1lllllllll1_opy_):
    try:
      bstack111111l111_opy_ = self.bstack1lllllll1ll_opy_()
      bstack1111l11lll_opy_ = os.path.join(bstack111111l111_opy_, bstack11l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭ᐱ"))
      bstack1111111111_opy_ = os.path.join(bstack111111l111_opy_, bstack1lllllllll1_opy_)
      if os.path.exists(bstack1111111111_opy_):
        self.logger.info(bstack11l11l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᐲ").format(bstack1111111111_opy_))
        return bstack1111111111_opy_
      if os.path.exists(bstack1111l11lll_opy_):
        self.logger.info(bstack11l11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᐳ").format(bstack1111l11lll_opy_))
        return self.bstack1111l11l11_opy_(bstack1111l11lll_opy_, bstack1lllllllll1_opy_)
      self.logger.info(bstack11l11l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᐴ").format(bstack11111lll1l_opy_))
      response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠧࡈࡇࡗࠫᐵ"), bstack11111lll1l_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1111l11lll_opy_, bstack11l11l_opy_ (u"ࠨࡹࡥࠫᐶ")) as file:
          file.write(response.content)
        self.logger.info(bstack11l11l_opy_ (u"ࠤࡇࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࠦࡰࡦࡴࡦࡽࠥࡨࡩ࡯ࡣࡵࡽࠥࡧ࡮ࡥࠢࡶࡥࡻ࡫ࡤࠡࡣࡷࠤࢀࢃࠢᐷ").format(bstack1111l11lll_opy_))
        return self.bstack1111l11l11_opy_(bstack1111l11lll_opy_, bstack1lllllllll1_opy_)
      else:
        raise(bstack11l11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡶ࡫ࡩࠥ࡬ࡩ࡭ࡧ࠱ࠤࡘࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠼ࠣࡿࢂࠨᐸ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹ࠻ࠢࡾࢁࠧᐹ").format(e))
  def bstack111111ll1l_opy_(self, bstack11111lll1l_opy_, bstack1lllllllll1_opy_):
    try:
      retry = 2
      bstack1111111111_opy_ = None
      bstack111111lll1_opy_ = False
      while retry > 0:
        bstack1111111111_opy_ = self.bstack11111l111l_opy_(bstack11111lll1l_opy_, bstack1lllllllll1_opy_)
        bstack111111lll1_opy_ = self.bstack1111111l11_opy_(bstack11111lll1l_opy_, bstack1lllllllll1_opy_, bstack1111111111_opy_)
        if bstack111111lll1_opy_:
          break
        retry -= 1
      return bstack1111111111_opy_, bstack111111lll1_opy_
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡸࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡵࡧࡴࡩࠤᐺ").format(e))
    return bstack1111111111_opy_, False
  def bstack1111111l11_opy_(self, bstack11111lll1l_opy_, bstack1lllllllll1_opy_, bstack1111111111_opy_, bstack1111111l1l_opy_ = 0):
    if bstack1111111l1l_opy_ > 1:
      return False
    if bstack1111111111_opy_ == None or os.path.exists(bstack1111111111_opy_) == False:
      self.logger.warn(bstack11l11l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩ࠲ࠠࡳࡧࡷࡶࡾ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᐻ"))
      return False
    bstack1lllllll11l_opy_ = bstack11l11l_opy_ (u"ࠢ࡟࠰࠭ࡄࡵ࡫ࡲࡤࡻ࡟࠳ࡨࡲࡩࠡ࡞ࡧ࠲ࡡࡪࠫ࠯࡞ࡧ࠯ࠧᐼ")
    command = bstack11l11l_opy_ (u"ࠨࡽࢀࠤ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧᐽ").format(bstack1111111111_opy_)
    bstack11111111ll_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1lllllll11l_opy_, bstack11111111ll_opy_) != None:
      return True
    else:
      self.logger.error(bstack11l11l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡦ࡬ࡪࡩ࡫ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᐾ"))
      return False
  def bstack1111l11l11_opy_(self, bstack1111l11lll_opy_, bstack1lllllllll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1111l11lll_opy_)
      shutil.unpack_archive(bstack1111l11lll_opy_, working_dir)
      bstack1111111111_opy_ = os.path.join(working_dir, bstack1lllllllll1_opy_)
      os.chmod(bstack1111111111_opy_, 0o755)
      return bstack1111111111_opy_
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡵ࡯ࡼ࡬ࡴࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᐿ"))
  def bstack1111l111l1_opy_(self):
    try:
      percy = str(self.config.get(bstack11l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᑀ"), bstack11l11l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᑁ"))).lower()
      if percy != bstack11l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦᑂ"):
        return False
      self.bstack11lll1l1l_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡤࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᑃ").format(e))
  def bstack11111l1ll1_opy_(self):
    try:
      bstack11111l1ll1_opy_ = str(self.config.get(bstack11l11l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᑄ"), bstack11l11l_opy_ (u"ࠤࡤࡹࡹࡵࠢᑅ"))).lower()
      return bstack11111l1ll1_opy_
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡧࡹࠦࡰࡦࡴࡦࡽࠥࡩࡡࡱࡶࡸࡶࡪࠦ࡭ࡰࡦࡨ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᑆ").format(e))
  def init(self, bstack1l1llll1ll_opy_, config, logger):
    self.bstack1l1llll1ll_opy_ = bstack1l1llll1ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1111l111l1_opy_():
      return
    self.bstack11111l11ll_opy_ = config.get(bstack11l11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᑇ"), {})
    self.bstack1111l11l1l_opy_ = config.get(bstack11l11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡇࡦࡶࡴࡶࡴࡨࡑࡴࡪࡥࠨᑈ"), bstack11l11l_opy_ (u"ࠨࡡࡶࡶࡲࠦᑉ"))
    try:
      bstack11111lll1l_opy_, bstack1lllllllll1_opy_ = self.bstack11111l1l11_opy_()
      bstack1111111111_opy_, bstack111111lll1_opy_ = self.bstack111111ll1l_opy_(bstack11111lll1l_opy_, bstack1lllllllll1_opy_)
      if bstack111111lll1_opy_:
        self.binary_path = bstack1111111111_opy_
        thread = Thread(target=self.bstack111111l11l_opy_)
        thread.start()
      else:
        self.bstack1111l1l1ll_opy_ = True
        self.logger.error(bstack11l11l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡲࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾ࠮࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡖࡥࡳࡥࡼࠦᑊ").format(bstack1111111111_opy_))
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᑋ").format(e))
  def bstack1llllllllll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11l11l_opy_ (u"ࠩ࡯ࡳ࡬࠭ᑌ"), bstack11l11l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰࡯ࡳ࡬࠭ᑍ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11l11l_opy_ (u"ࠦࡕࡻࡳࡩ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࡴࠢࡤࡸࠥࢁࡽࠣᑎ").format(logfile))
      self.bstack111111111l_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࠥࡶࡥࡳࡥࡼࠤࡱࡵࡧࠡࡲࡤࡸ࡭࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᑏ").format(e))
  def bstack111111l11l_opy_(self):
    bstack1111l1l1l1_opy_ = self.bstack1111l11ll1_opy_()
    if bstack1111l1l1l1_opy_ == None:
      self.bstack1111l1l1ll_opy_ = True
      self.logger.error(bstack11l11l_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡺ࡯࡬ࡧࡱࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠬࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺࠤᑐ"))
      return False
    command_args = [bstack11l11l_opy_ (u"ࠢࡢࡲࡳ࠾ࡪࡾࡥࡤ࠼ࡶࡸࡦࡸࡴࠣᑑ") if self.bstack1l1llll1ll_opy_ else bstack11l11l_opy_ (u"ࠨࡧࡻࡩࡨࡀࡳࡵࡣࡵࡸࠬᑒ")]
    bstack11111ll1ll_opy_ = self.bstack111111l1ll_opy_()
    if bstack11111ll1ll_opy_ != None:
      command_args.append(bstack11l11l_opy_ (u"ࠤ࠰ࡧࠥࢁࡽࠣᑓ").format(bstack11111ll1ll_opy_))
    env = os.environ.copy()
    env[bstack11l11l_opy_ (u"ࠥࡔࡊࡘࡃ࡚ࡡࡗࡓࡐࡋࡎࠣᑔ")] = bstack1111l1l1l1_opy_
    bstack1111l11111_opy_ = [self.binary_path]
    self.bstack1llllllllll_opy_()
    self.bstack1111l1l111_opy_ = self.bstack1111111lll_opy_(bstack1111l11111_opy_ + command_args, env)
    self.logger.debug(bstack11l11l_opy_ (u"ࠦࡘࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠧᑕ"))
    bstack1111111l1l_opy_ = 0
    while self.bstack1111l1l111_opy_.poll() == None:
      bstack1lllllll1l1_opy_ = self.bstack11111111l1_opy_()
      if bstack1lllllll1l1_opy_:
        self.logger.debug(bstack11l11l_opy_ (u"ࠧࡎࡥࡢ࡮ࡷ࡬ࠥࡉࡨࡦࡥ࡮ࠤࡸࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠣᑖ"))
        self.bstack11111llll1_opy_ = True
        return True
      bstack1111111l1l_opy_ += 1
      self.logger.debug(bstack11l11l_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡘࡥࡵࡴࡼࠤ࠲ࠦࡻࡾࠤᑗ").format(bstack1111111l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack11l11l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡧࡲࡵࠢࡳࡩࡷࡩࡹ࠭ࠢࡋࡩࡦࡲࡴࡩࠢࡆ࡬ࡪࡩ࡫ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡣࡩࡸࡪࡸࠠࡼࡿࠣࡥࡹࡺࡥ࡮ࡲࡷࡷࠧᑘ").format(bstack1111111l1l_opy_))
    self.bstack1111l1l1ll_opy_ = True
    return False
  def bstack11111111l1_opy_(self, bstack1111111l1l_opy_ = 0):
    try:
      if bstack1111111l1l_opy_ > 10:
        return False
      bstack1111l111ll_opy_ = os.environ.get(bstack11l11l_opy_ (u"ࠨࡒࡈࡖࡈ࡟࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡂࡆࡇࡖࡊ࡙ࡓࠨᑙ"), bstack11l11l_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸ࠿࠻࠳࠴࠺ࠪᑚ"))
      bstack11111l1l1l_opy_ = bstack1111l111ll_opy_ + bstack11l111ll1l_opy_
      response = requests.get(bstack11111l1l1l_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack1111l11ll1_opy_(self):
    bstack1111l1111l_opy_ = bstack11l11l_opy_ (u"ࠪࡥࡵࡶࠧᑛ") if self.bstack1l1llll1ll_opy_ else bstack11l11l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᑜ")
    bstack111l1l1l1l_opy_ = bstack11l11l_opy_ (u"ࠧࡧࡰࡪ࠱ࡤࡴࡵࡥࡰࡦࡴࡦࡽ࠴࡭ࡥࡵࡡࡳࡶࡴࡰࡥࡤࡶࡢࡸࡴࡱࡥ࡯ࡁࡱࡥࡲ࡫࠽ࡼࡿࠩࡸࡾࡶࡥ࠾ࡽࢀࠦᑝ").format(self.config[bstack11l11l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᑞ")], bstack1111l1111l_opy_)
    uri = bstack1ll1llll1_opy_(bstack111l1l1l1l_opy_)
    try:
      response = bstack1llll11l1_opy_(bstack11l11l_opy_ (u"ࠧࡈࡇࡗࠫᑟ"), uri, {}, {bstack11l11l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᑠ"): (self.config[bstack11l11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᑡ")], self.config[bstack11l11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᑢ")])})
      if response.status_code == 200:
        bstack11111ll11l_opy_ = response.json()
        if bstack11l11l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᑣ") in bstack11111ll11l_opy_:
          return bstack11111ll11l_opy_[bstack11l11l_opy_ (u"ࠧࡺ࡯࡬ࡧࡱࠦᑤ")]
        else:
          raise bstack11l11l_opy_ (u"࠭ࡔࡰ࡭ࡨࡲࠥࡔ࡯ࡵࠢࡉࡳࡺࡴࡤࠡ࠯ࠣࡿࢂ࠭ᑥ").format(bstack11111ll11l_opy_)
      else:
        raise bstack11l11l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡳࡩࡷࡩࡹࠡࡶࡲ࡯ࡪࡴࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡷࡹࡧࡴࡶࡵࠣ࠱ࠥࢁࡽ࠭ࠢࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡇࡵࡤࡺࠢ࠰ࠤࢀࢃࠢᑦ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡲࡵࡳ࡯࡫ࡣࡵࠤᑧ").format(e))
  def bstack111111l1ll_opy_(self):
    bstack111111ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠤࡳࡩࡷࡩࡹࡄࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠧᑨ"))
    try:
      if bstack11l11l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᑩ") not in self.bstack11111l11ll_opy_:
        self.bstack11111l11ll_opy_[bstack11l11l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࠬᑪ")] = 2
      with open(bstack111111ll11_opy_, bstack11l11l_opy_ (u"ࠬࡽࠧᑫ")) as fp:
        json.dump(self.bstack11111l11ll_opy_, fp)
      return bstack111111ll11_opy_
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡦࡶࡪࡧࡴࡦࠢࡳࡩࡷࡩࡹࠡࡥࡲࡲ࡫࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᑬ").format(e))
  def bstack1111111lll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack11111l1111_opy_ == bstack11l11l_opy_ (u"ࠧࡸ࡫ࡱࠫᑭ"):
        bstack11111lllll_opy_ = [bstack11l11l_opy_ (u"ࠨࡥࡰࡨ࠳࡫ࡸࡦࠩᑮ"), bstack11l11l_opy_ (u"ࠩ࠲ࡧࠬᑯ")]
        cmd = bstack11111lllll_opy_ + cmd
      cmd = bstack11l11l_opy_ (u"ࠪࠤࠬᑰ").join(cmd)
      self.logger.debug(bstack11l11l_opy_ (u"ࠦࡗࡻ࡮࡯࡫ࡱ࡫ࠥࢁࡽࠣᑱ").format(cmd))
      with open(self.bstack111111111l_opy_, bstack11l11l_opy_ (u"ࠧࡧࠢᑲ")) as bstack11111l11l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack11111l11l1_opy_, text=True, stderr=bstack11111l11l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111l1l1ll_opy_ = True
      self.logger.error(bstack11l11l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠠࡸ࡫ࡷ࡬ࠥࡩ࡭ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᑳ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111llll1_opy_:
        self.logger.info(bstack11l11l_opy_ (u"ࠢࡔࡶࡲࡴࡵ࡯࡮ࡨࠢࡓࡩࡷࡩࡹࠣᑴ"))
        cmd = [self.binary_path, bstack11l11l_opy_ (u"ࠣࡧࡻࡩࡨࡀࡳࡵࡱࡳࠦᑵ")]
        self.bstack1111111lll_opy_(cmd)
        self.bstack11111llll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡰࡲࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡦࡳࡲࡳࡡ࡯ࡦࠣ࠱ࠥࢁࡽ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠤᑶ").format(cmd, e))
  def bstack1l11l1ll1_opy_(self):
    if not self.bstack11lll1l1l_opy_:
      return
    try:
      bstack1111l1l11l_opy_ = 0
      while not self.bstack11111llll1_opy_ and bstack1111l1l11l_opy_ < self.bstack11111ll111_opy_:
        if self.bstack1111l1l1ll_opy_:
          self.logger.info(bstack11l11l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡨࡤ࡭ࡱ࡫ࡤࠣᑷ"))
          return
        time.sleep(1)
        bstack1111l1l11l_opy_ += 1
      os.environ[bstack11l11l_opy_ (u"ࠫࡕࡋࡒࡄ࡛ࡢࡆࡊ࡙ࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࠪᑸ")] = str(self.bstack11111ll1l1_opy_())
      self.logger.info(bstack11l11l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡸ࡫ࡴࡶࡲࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠨᑹ"))
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡩࡹࡻࡰࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᑺ").format(e))
  def bstack11111ll1l1_opy_(self):
    if self.bstack1l1llll1ll_opy_:
      return
    try:
      bstack111111l1l1_opy_ = [platform[bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᑻ")].lower() for platform in self.config.get(bstack11l11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᑼ"), [])]
      bstack1lllllll111_opy_ = sys.maxsize
      bstack1llllllll11_opy_ = bstack11l11l_opy_ (u"ࠩࠪᑽ")
      for browser in bstack111111l1l1_opy_:
        if browser in self.bstack111111llll_opy_:
          bstack11111l1lll_opy_ = self.bstack111111llll_opy_[browser]
        if bstack11111l1lll_opy_ < bstack1lllllll111_opy_:
          bstack1lllllll111_opy_ = bstack11111l1lll_opy_
          bstack1llllllll11_opy_ = browser
      return bstack1llllllll11_opy_
    except Exception as e:
      self.logger.error(bstack11l11l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪࡰࡧࠤࡧ࡫ࡳࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᑾ").format(e))