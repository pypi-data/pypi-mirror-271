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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l1ll11l_opy_
from browserstack_sdk.bstack11l111l1l_opy_ import bstack1l1l1ll1ll_opy_
def _111l1111ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l111l11_opy_:
    def __init__(self, handler):
        self._111l11ll11_opy_ = {}
        self._111l11l11l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l1ll1ll_opy_.version()
        if bstack111l1ll11l_opy_(pytest_version, bstack11l11l_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢ፹")) >= 0:
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ፺")] = Module._register_setup_function_fixture
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ፻")] = Module._register_setup_module_fixture
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ፼")] = Class._register_setup_class_fixture
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭፽")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ፾"))
            Module._register_setup_module_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ፿"))
            Class._register_setup_class_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᎀ"))
            Class._register_setup_method_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᎁ"))
        else:
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᎂ")] = Module._inject_setup_function_fixture
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎃ")] = Module._inject_setup_module_fixture
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᎄ")] = Class._inject_setup_class_fixture
            self._111l11ll11_opy_[bstack11l11l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᎅ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᎆ"))
            Module._inject_setup_module_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᎇ"))
            Class._inject_setup_class_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᎈ"))
            Class._inject_setup_method_fixture = self.bstack111l11ll1l_opy_(bstack11l11l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᎉ"))
    def bstack111l111111_opy_(self, bstack111l11111l_opy_, hook_type):
        meth = getattr(bstack111l11111l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111l11l11l_opy_[hook_type] = meth
            setattr(bstack111l11111l_opy_, hook_type, self.bstack111l11l1ll_opy_(hook_type))
    def bstack111l11l1l1_opy_(self, instance, bstack111l111lll_opy_):
        if bstack111l111lll_opy_ == bstack11l11l_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᎊ"):
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᎋ"))
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᎌ"))
        if bstack111l111lll_opy_ == bstack11l11l_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᎍ"):
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᎎ"))
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᎏ"))
        if bstack111l111lll_opy_ == bstack11l11l_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥ᎐"):
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤ᎑"))
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨ᎒"))
        if bstack111l111lll_opy_ == bstack11l11l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢ᎓"):
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨ᎔"))
            self.bstack111l111111_opy_(instance.obj, bstack11l11l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥ᎕"))
    @staticmethod
    def bstack111l1111l1_opy_(hook_type, func, args):
        if hook_type in [bstack11l11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨ᎖"), bstack11l11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬ᎗")]:
            _111l1111ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111l11l1ll_opy_(self, hook_type):
        def bstack1111llllll_opy_(arg=None):
            self.handler(hook_type, bstack11l11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ᎘"))
            result = None
            exception = None
            try:
                self.bstack111l1111l1_opy_(hook_type, self._111l11l11l_opy_[hook_type], (arg,))
                result = Result(result=bstack11l11l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᎙"))
            except Exception as e:
                result = Result(result=bstack11l11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᎚"), exception=e)
                self.handler(hook_type, bstack11l11l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭᎛"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l11l_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧ᎜"), result)
        def bstack111l111l1l_opy_(this, arg=None):
            self.handler(hook_type, bstack11l11l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ᎝"))
            result = None
            exception = None
            try:
                self.bstack111l1111l1_opy_(hook_type, self._111l11l11l_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ᎞"))
            except Exception as e:
                result = Result(result=bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᎟"), exception=e)
                self.handler(hook_type, bstack11l11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᎠ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᎡ"), result)
        if hook_type in [bstack11l11l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭Ꭲ"), bstack11l11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᎣ")]:
            return bstack111l111l1l_opy_
        return bstack1111llllll_opy_
    def bstack111l11ll1l_opy_(self, bstack111l111lll_opy_):
        def bstack111l111ll1_opy_(this, *args, **kwargs):
            self.bstack111l11l1l1_opy_(this, bstack111l111lll_opy_)
            self._111l11ll11_opy_[bstack111l111lll_opy_](this, *args, **kwargs)
        return bstack111l111ll1_opy_