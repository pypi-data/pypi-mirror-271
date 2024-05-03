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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l11l111l_opy_
import tempfile
import json
bstack1111lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᎤ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11l11l_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᎥ"),
      datefmt=bstack11l11l_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭Ꭶ"),
      stream=sys.stdout
    )
  return logger
def bstack1111lll111_opy_():
  global bstack1111lll1ll_opy_
  if os.path.exists(bstack1111lll1ll_opy_):
    os.remove(bstack1111lll1ll_opy_)
def bstack1l1ll1l1ll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1111111l_opy_(config, log_level):
  bstack1111lllll1_opy_ = log_level
  if bstack11l11l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᎧ") in config:
    bstack1111lllll1_opy_ = bstack11l11l111l_opy_[config[bstack11l11l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᎨ")]]
  if config.get(bstack11l11l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᎩ"), False):
    logging.getLogger().setLevel(bstack1111lllll1_opy_)
    return bstack1111lllll1_opy_
  global bstack1111lll1ll_opy_
  bstack1l1ll1l1ll_opy_()
  bstack1111ll1ll1_opy_ = logging.Formatter(
    fmt=bstack11l11l_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭Ꭺ"),
    datefmt=bstack11l11l_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᎫ")
  )
  bstack1111ll1l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1111lll1ll_opy_)
  file_handler.setFormatter(bstack1111ll1ll1_opy_)
  bstack1111ll1l11_opy_.setFormatter(bstack1111ll1ll1_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1111ll1l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11l11l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᎬ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1111ll1l11_opy_.setLevel(bstack1111lllll1_opy_)
  logging.getLogger().addHandler(bstack1111ll1l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1111lllll1_opy_
def bstack1111lll11l_opy_(config):
  try:
    bstack1111llll1l_opy_ = set([
      bstack11l11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ꭽ"), bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᎮ"), bstack11l11l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᎯ"), bstack11l11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᎰ"), bstack11l11l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪᎱ"),
      bstack11l11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᎲ"), bstack11l11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭Ꮃ"), bstack11l11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬᎴ"), bstack11l11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭Ꮅ")
    ])
    bstack1111ll11ll_opy_ = bstack11l11l_opy_ (u"࠭ࠧᎶ")
    with open(bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᎷ")) as bstack1111ll1lll_opy_:
      bstack1111ll111l_opy_ = bstack1111ll1lll_opy_.read()
      bstack1111ll11ll_opy_ = re.sub(bstack11l11l_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠦ࠲࠯ࠪ࡜࡯ࠩᎸ"), bstack11l11l_opy_ (u"ࠩࠪᎹ"), bstack1111ll111l_opy_, flags=re.M)
      bstack1111ll11ll_opy_ = re.sub(
        bstack11l11l_opy_ (u"ࡵࠫࡣ࠮࡜ࡴ࠭ࠬࡃ࠭࠭Ꮊ") + bstack11l11l_opy_ (u"ࠫࢁ࠭Ꮋ").join(bstack1111llll1l_opy_) + bstack11l11l_opy_ (u"ࠬ࠯࠮ࠫࠦࠪᎼ"),
        bstack11l11l_opy_ (u"ࡸࠧ࡝࠴࠽ࠤࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᎽ"),
        bstack1111ll11ll_opy_, flags=re.M | re.I
      )
    def bstack1111ll11l1_opy_(dic):
      bstack1111llll11_opy_ = {}
      for key, value in dic.items():
        if key in bstack1111llll1l_opy_:
          bstack1111llll11_opy_[key] = bstack11l11l_opy_ (u"ࠧ࡜ࡔࡈࡈࡆࡉࡔࡆࡆࡠࠫᎾ")
        else:
          if isinstance(value, dict):
            bstack1111llll11_opy_[key] = bstack1111ll11l1_opy_(value)
          else:
            bstack1111llll11_opy_[key] = value
      return bstack1111llll11_opy_
    bstack1111llll11_opy_ = bstack1111ll11l1_opy_(config)
    return {
      bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡺ࡯࡯ࠫᎿ"): bstack1111ll11ll_opy_,
      bstack11l11l_opy_ (u"ࠩࡩ࡭ࡳࡧ࡬ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᏀ"): json.dumps(bstack1111llll11_opy_)
    }
  except Exception as e:
    return {}
def bstack111111lll_opy_(config):
  global bstack1111lll1ll_opy_
  try:
    if config.get(bstack11l11l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬᏁ"), False):
      return
    uuid = os.getenv(bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᏂ"))
    if not uuid or uuid == bstack11l11l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᏃ"):
      return
    bstack1111lll1l1_opy_ = [bstack11l11l_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩᏄ"), bstack11l11l_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨᏅ"), bstack11l11l_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩᏆ"), bstack1111lll1ll_opy_]
    bstack1l1ll1l1ll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯࡯ࡳ࡬ࡹ࠭ࠨᏇ") + uuid + bstack11l11l_opy_ (u"ࠪ࠲ࡹࡧࡲ࠯ࡩࡽࠫᏈ"))
    with tarfile.open(output_file, bstack11l11l_opy_ (u"ࠦࡼࡀࡧࡻࠤᏉ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1111lll1l1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1111lll11l_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1111ll1l1l_opy_ = data.encode()
        tarinfo.size = len(bstack1111ll1l1l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1111ll1l1l_opy_))
    bstack1ll11111l_opy_ = MultipartEncoder(
      fields= {
        bstack11l11l_opy_ (u"ࠬࡪࡡࡵࡣࠪᏊ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11l11l_opy_ (u"࠭ࡲࡣࠩᏋ")), bstack11l11l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾ࠭ࡨࡼ࡬ࡴࠬᏌ")),
        bstack11l11l_opy_ (u"ࠨࡥ࡯࡭ࡪࡴࡴࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᏍ"): uuid
      }
    )
    response = requests.post(
      bstack11l11l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡹࡵࡲ࡯ࡢࡦ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡣ࡭࡫ࡨࡲࡹ࠳࡬ࡰࡩࡶ࠳ࡺࡶ࡬ࡰࡣࡧࠦᏎ"),
      data=bstack1ll11111l_opy_,
      headers={bstack11l11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᏏ"): bstack1ll11111l_opy_.content_type},
      auth=(config[bstack11l11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭Ꮠ")], config[bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᏑ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11l11l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥࡻࡰ࡭ࡱࡤࡨࠥࡲ࡯ࡨࡵ࠽ࠤࠬᏒ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11l11l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡰࡧ࡭ࡳ࡭ࠠ࡭ࡱࡪࡷ࠿࠭Ꮣ") + str(e))
  finally:
    try:
      bstack1111lll111_opy_()
    except:
      pass