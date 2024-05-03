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
from uuid import uuid4
from bstack_utils.helper import bstack1lllll11_opy_, bstack111ll1ll1l_opy_
from bstack_utils.bstack1lll1111l_opy_ import bstack11ll111111_opy_
class bstack1l111lll1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11lllllll1_opy_=None, framework=None, tags=[], scope=[], bstack1llll111lll_opy_=None, bstack1llll11llll_opy_=True, bstack1llll11ll1l_opy_=None, bstack11l1lllll_opy_=None, result=None, duration=None, bstack11llll11l1_opy_=None, meta={}):
        self.bstack11llll11l1_opy_ = bstack11llll11l1_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll11llll_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11lllllll1_opy_ = bstack11lllllll1_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll111lll_opy_ = bstack1llll111lll_opy_
        self.bstack1llll11ll1l_opy_ = bstack1llll11ll1l_opy_
        self.bstack11l1lllll_opy_ = bstack11l1lllll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11llllll11_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1111ll_opy_(self):
        bstack1llll11ll11_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11l11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᒶ"): bstack1llll11ll11_opy_,
            bstack11l11l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᒷ"): bstack1llll11ll11_opy_,
            bstack11l11l_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᒸ"): bstack1llll11ll11_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11l11l_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᒹ") + key)
            setattr(self, key, val)
    def bstack1llll11l11l_opy_(self):
        return {
            bstack11l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒺ"): self.name,
            bstack11l11l_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᒻ"): {
                bstack11l11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᒼ"): bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᒽ"),
                bstack11l11l_opy_ (u"ࠫࡨࡵࡤࡦࠩᒾ"): self.code
            },
            bstack11l11l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᒿ"): self.scope,
            bstack11l11l_opy_ (u"࠭ࡴࡢࡩࡶࠫᓀ"): self.tags,
            bstack11l11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᓁ"): self.framework,
            bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᓂ"): self.bstack11lllllll1_opy_
        }
    def bstack1llll11l1l1_opy_(self):
        return {
         bstack11l11l_opy_ (u"ࠩࡰࡩࡹࡧࠧᓃ"): self.meta
        }
    def bstack1llll111ll1_opy_(self):
        return {
            bstack11l11l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᓄ"): {
                bstack11l11l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᓅ"): self.bstack1llll111lll_opy_
            }
        }
    def bstack1llll11l111_opy_(self, bstack1llll11lll1_opy_, details):
        step = next(filter(lambda st: st[bstack11l11l_opy_ (u"ࠬ࡯ࡤࠨᓆ")] == bstack1llll11lll1_opy_, self.meta[bstack11l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓇ")]), None)
        step.update(details)
    def bstack1llll1l11ll_opy_(self, bstack1llll11lll1_opy_):
        step = next(filter(lambda st: st[bstack11l11l_opy_ (u"ࠧࡪࡦࠪᓈ")] == bstack1llll11lll1_opy_, self.meta[bstack11l11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓉ")]), None)
        step.update({
            bstack11l11l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᓊ"): bstack1lllll11_opy_()
        })
    def bstack11lll1ll1l_opy_(self, bstack1llll11lll1_opy_, result, duration=None):
        bstack1llll11ll1l_opy_ = bstack1lllll11_opy_()
        if bstack1llll11lll1_opy_ is not None and self.meta.get(bstack11l11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓋ")):
            step = next(filter(lambda st: st[bstack11l11l_opy_ (u"ࠫ࡮ࡪࠧᓌ")] == bstack1llll11lll1_opy_, self.meta[bstack11l11l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓍ")]), None)
            step.update({
                bstack11l11l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᓎ"): bstack1llll11ll1l_opy_,
                bstack11l11l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᓏ"): duration if duration else bstack111ll1ll1l_opy_(step[bstack11l11l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᓐ")], bstack1llll11ll1l_opy_),
                bstack11l11l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᓑ"): result.result,
                bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᓒ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll1l1111_opy_):
        if self.meta.get(bstack11l11l_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᓓ")):
            self.meta[bstack11l11l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᓔ")].append(bstack1llll1l1111_opy_)
        else:
            self.meta[bstack11l11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓕ")] = [ bstack1llll1l1111_opy_ ]
    def bstack1llll1l1l11_opy_(self):
        return {
            bstack11l11l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᓖ"): self.bstack11llllll11_opy_(),
            **self.bstack1llll11l11l_opy_(),
            **self.bstack1llll1111ll_opy_(),
            **self.bstack1llll11l1l1_opy_()
        }
    def bstack1llll1l111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11l11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓗ"): self.bstack1llll11ll1l_opy_,
            bstack11l11l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᓘ"): self.duration,
            bstack11l11l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᓙ"): self.result.result
        }
        if data[bstack11l11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓚ")] == bstack11l11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᓛ"):
            data[bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᓜ")] = self.result.bstack11ll1l111l_opy_()
            data[bstack11l11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᓝ")] = [{bstack11l11l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᓞ"): self.result.bstack11l1111ll1_opy_()}]
        return data
    def bstack1llll111l11_opy_(self):
        return {
            bstack11l11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓟ"): self.bstack11llllll11_opy_(),
            **self.bstack1llll11l11l_opy_(),
            **self.bstack1llll1111ll_opy_(),
            **self.bstack1llll1l111l_opy_(),
            **self.bstack1llll11l1l1_opy_()
        }
    def bstack11lllll11l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11l11l_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫᓠ") in event:
            return self.bstack1llll1l1l11_opy_()
        elif bstack11l11l_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓡ") in event:
            return self.bstack1llll111l11_opy_()
    def bstack1l111111l1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll11ll1l_opy_ = time if time else bstack1lllll11_opy_()
        self.duration = duration if duration else bstack111ll1ll1l_opy_(self.bstack11lllllll1_opy_, self.bstack1llll11ll1l_opy_)
        if result:
            self.result = result
class bstack1l111l1lll_opy_(bstack1l111lll1l_opy_):
    def __init__(self, hooks=[], bstack1l11l111l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l111l1_opy_ = bstack1l11l111l1_opy_
        super().__init__(*args, **kwargs, bstack11l1lllll_opy_=bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࠪᓢ"))
    @classmethod
    def bstack1llll1111l1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11l11l_opy_ (u"࠭ࡩࡥࠩᓣ"): id(step),
                bstack11l11l_opy_ (u"ࠧࡵࡧࡻࡸࠬᓤ"): step.name,
                bstack11l11l_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᓥ"): step.keyword,
            })
        return bstack1l111l1lll_opy_(
            **kwargs,
            meta={
                bstack11l11l_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᓦ"): {
                    bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨᓧ"): feature.name,
                    bstack11l11l_opy_ (u"ࠫࡵࡧࡴࡩࠩᓨ"): feature.filename,
                    bstack11l11l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᓩ"): feature.description
                },
                bstack11l11l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᓪ"): {
                    bstack11l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᓫ"): scenario.name
                },
                bstack11l11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓬ"): steps,
                bstack11l11l_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᓭ"): bstack11ll111111_opy_(test)
            }
        )
    def bstack1llll111l1l_opy_(self):
        return {
            bstack11l11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᓮ"): self.hooks
        }
    def bstack1llll11l1ll_opy_(self):
        if self.bstack1l11l111l1_opy_:
            return {
                bstack11l11l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᓯ"): self.bstack1l11l111l1_opy_
            }
        return {}
    def bstack1llll111l11_opy_(self):
        return {
            **super().bstack1llll111l11_opy_(),
            **self.bstack1llll111l1l_opy_()
        }
    def bstack1llll1l1l11_opy_(self):
        return {
            **super().bstack1llll1l1l11_opy_(),
            **self.bstack1llll11l1ll_opy_()
        }
    def bstack1l111111l1_opy_(self):
        return bstack11l11l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᓰ")
class bstack1l111l11l1_opy_(bstack1l111lll1l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack11l1lllll_opy_=bstack11l11l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᓱ"))
    def bstack11lll1l1l1_opy_(self):
        return self.hook_type
    def bstack1llll1l11l1_opy_(self):
        return {
            bstack11l11l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᓲ"): self.hook_type
        }
    def bstack1llll111l11_opy_(self):
        return {
            **super().bstack1llll111l11_opy_(),
            **self.bstack1llll1l11l1_opy_()
        }
    def bstack1llll1l1l11_opy_(self):
        return {
            **super().bstack1llll1l1l11_opy_(),
            **self.bstack1llll1l11l1_opy_()
        }
    def bstack1l111111l1_opy_(self):
        return bstack11l11l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᓳ")