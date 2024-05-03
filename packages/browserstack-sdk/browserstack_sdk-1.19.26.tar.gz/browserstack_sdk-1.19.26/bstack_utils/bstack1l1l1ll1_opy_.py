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
class bstack11l11llll1_opy_(object):
  bstack11lllll1_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"࠭ࡾࠨ༬")), bstack11l11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ༭"))
  bstack11l11lll1l_opy_ = os.path.join(bstack11lllll1_opy_, bstack11l11l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ༮"))
  bstack11l11ll1l1_opy_ = None
  perform_scan = None
  bstack1l1l1l11l_opy_ = None
  bstack1llll1l11l_opy_ = None
  bstack11l1ll1111_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11l11l_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫ༯")):
      cls.instance = super(bstack11l11llll1_opy_, cls).__new__(cls)
      cls.instance.bstack11l11ll11l_opy_()
    return cls.instance
  def bstack11l11ll11l_opy_(self):
    try:
      with open(self.bstack11l11lll1l_opy_, bstack11l11l_opy_ (u"ࠪࡶࠬ༰")) as bstack1l1l111l1_opy_:
        bstack11l11lll11_opy_ = bstack1l1l111l1_opy_.read()
        data = json.loads(bstack11l11lll11_opy_)
        if bstack11l11l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭༱") in data:
          self.bstack11l1l111l1_opy_(data[bstack11l11l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ༲")])
        if bstack11l11l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ༳") in data:
          self.bstack11l1ll111l_opy_(data[bstack11l11l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ༴")])
    except:
      pass
  def bstack11l1ll111l_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11l11l_opy_ (u"ࠨࡵࡦࡥࡳ༵࠭")]
      self.bstack1l1l1l11l_opy_ = scripts[bstack11l11l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭༶")]
      self.bstack1llll1l11l_opy_ = scripts[bstack11l11l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿ༷ࠧ")]
      self.bstack11l1ll1111_opy_ = scripts[bstack11l11l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩ༸")]
  def bstack11l1l111l1_opy_(self, bstack11l11ll1l1_opy_):
    if bstack11l11ll1l1_opy_ != None and len(bstack11l11ll1l1_opy_) != 0:
      self.bstack11l11ll1l1_opy_ = bstack11l11ll1l1_opy_
  def store(self):
    try:
      with open(self.bstack11l11lll1l_opy_, bstack11l11l_opy_ (u"ࠬࡽ༹ࠧ")) as file:
        json.dump({
          bstack11l11l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣ༺"): self.bstack11l11ll1l1_opy_,
          bstack11l11l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ༻"): {
            bstack11l11l_opy_ (u"ࠣࡵࡦࡥࡳࠨ༼"): self.perform_scan,
            bstack11l11l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ༽"): self.bstack1l1l1l11l_opy_,
            bstack11l11l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ༾"): self.bstack1llll1l11l_opy_,
            bstack11l11l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤ༿"): self.bstack11l1ll1111_opy_
          }
        }, file)
    except:
      pass
  def bstack1111lll1l_opy_(self, bstack11l11ll1ll_opy_):
    try:
      return any(command.get(bstack11l11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪཀ")) == bstack11l11ll1ll_opy_ for command in self.bstack11l11ll1l1_opy_)
    except:
      return False
bstack1l1l1ll1_opy_ = bstack11l11llll1_opy_()