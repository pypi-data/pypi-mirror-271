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
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l111l11l_opy_, bstack1lll1ll1ll_opy_, bstack1111l11l1_opy_, bstack1l11l11ll_opy_
from bstack_utils.messages import bstack1l1ll1l11_opy_, bstack1l1l11ll1l_opy_
from bstack_utils.proxy import bstack1ll111l1l_opy_, bstack1l1l11111_opy_
bstack111l11111_opy_ = Config.bstack1l11l1111_opy_()
def bstack11l1l1l1ll_opy_(config):
    return config[bstack11l11l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᇟ")]
def bstack11l1ll11l1_opy_(config):
    return config[bstack11l11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᇠ")]
def bstack111l1l1l1_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111ll111ll_opy_(obj):
    values = []
    bstack111lll1111_opy_ = re.compile(bstack11l11l_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᇡ"), re.I)
    for key in obj.keys():
        if bstack111lll1111_opy_.match(key):
            values.append(obj[key])
    return values
def bstack111ll11ll1_opy_(config):
    tags = []
    tags.extend(bstack111ll111ll_opy_(os.environ))
    tags.extend(bstack111ll111ll_opy_(config))
    return tags
def bstack111llll1ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack111llll1l1_opy_(bstack111lllll11_opy_):
    if not bstack111lllll11_opy_:
        return bstack11l11l_opy_ (u"ࠧࠨᇢ")
    return bstack11l11l_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᇣ").format(bstack111lllll11_opy_.name, bstack111lllll11_opy_.email)
def bstack11l1ll1l1l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l1l1lll_opy_ = repo.common_dir
        info = {
            bstack11l11l_opy_ (u"ࠤࡶ࡬ࡦࠨᇤ"): repo.head.commit.hexsha,
            bstack11l11l_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᇥ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l11l_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᇦ"): repo.active_branch.name,
            bstack11l11l_opy_ (u"ࠧࡺࡡࡨࠤᇧ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l11l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᇨ"): bstack111llll1l1_opy_(repo.head.commit.committer),
            bstack11l11l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᇩ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l11l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᇪ"): bstack111llll1l1_opy_(repo.head.commit.author),
            bstack11l11l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᇫ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l11l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᇬ"): repo.head.commit.message,
            bstack11l11l_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᇭ"): repo.git.rev_parse(bstack11l11l_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᇮ")),
            bstack11l11l_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᇯ"): bstack111l1l1lll_opy_,
            bstack11l11l_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᇰ"): subprocess.check_output([bstack11l11l_opy_ (u"ࠣࡩ࡬ࡸࠧᇱ"), bstack11l11l_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᇲ"), bstack11l11l_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᇳ")]).strip().decode(
                bstack11l11l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᇴ")),
            bstack11l11l_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᇵ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l11l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᇶ"): repo.git.rev_list(
                bstack11l11l_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᇷ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111ll111l1_opy_ = []
        for remote in remotes:
            bstack111ll11l1l_opy_ = {
                bstack11l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨᇸ"): remote.name,
                bstack11l11l_opy_ (u"ࠤࡸࡶࡱࠨᇹ"): remote.url,
            }
            bstack111ll111l1_opy_.append(bstack111ll11l1l_opy_)
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇺ"): bstack11l11l_opy_ (u"ࠦ࡬࡯ࡴࠣᇻ"),
            **info,
            bstack11l11l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᇼ"): bstack111ll111l1_opy_
        }
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᇽ").format(err))
        return {}
def bstack1llllllll1_opy_():
    env = os.environ
    if (bstack11l11l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᇾ") in env and len(env[bstack11l11l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᇿ")]) > 0) or (
            bstack11l11l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣሀ") in env and len(env[bstack11l11l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤሁ")]) > 0):
        return {
            bstack11l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሂ"): bstack11l11l_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨሃ"),
            bstack11l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሄ"): env.get(bstack11l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥህ")),
            bstack11l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሆ"): env.get(bstack11l11l_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦሇ")),
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤለ"): env.get(bstack11l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥሉ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠧࡉࡉࠣሊ")) == bstack11l11l_opy_ (u"ࠨࡴࡳࡷࡨࠦላ") and bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤሌ"))):
        return {
            bstack11l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨል"): bstack11l11l_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦሎ"),
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሏ"): env.get(bstack11l11l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢሐ")),
            bstack11l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሑ"): env.get(bstack11l11l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥሒ")),
            bstack11l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሓ"): env.get(bstack11l11l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦሔ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠤࡆࡍࠧሕ")) == bstack11l11l_opy_ (u"ࠥࡸࡷࡻࡥࠣሖ") and bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦሗ"))):
        return {
            bstack11l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥመ"): bstack11l11l_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤሙ"),
            bstack11l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሚ"): env.get(bstack11l11l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣማ")),
            bstack11l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሜ"): env.get(bstack11l11l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧም")),
            bstack11l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሞ"): env.get(bstack11l11l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሟ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠨࡃࡊࠤሠ")) == bstack11l11l_opy_ (u"ࠢࡵࡴࡸࡩࠧሡ") and env.get(bstack11l11l_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤሢ")) == bstack11l11l_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦሣ"):
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣሤ"): bstack11l11l_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨሥ"),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሦ"): None,
            bstack11l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣሧ"): None,
            bstack11l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨረ"): None
        }
    if env.get(bstack11l11l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦሩ")) and env.get(bstack11l11l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧሪ")):
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣራ"): bstack11l11l_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢሬ"),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣር"): env.get(bstack11l11l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦሮ")),
            bstack11l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሯ"): None,
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሰ"): env.get(bstack11l11l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦሱ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠥࡇࡎࠨሲ")) == bstack11l11l_opy_ (u"ࠦࡹࡸࡵࡦࠤሳ") and bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦሴ"))):
        return {
            bstack11l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦስ"): bstack11l11l_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨሶ"),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሷ"): env.get(bstack11l11l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧሸ")),
            bstack11l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሹ"): None,
            bstack11l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሺ"): env.get(bstack11l11l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥሻ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠨࡃࡊࠤሼ")) == bstack11l11l_opy_ (u"ࠢࡵࡴࡸࡩࠧሽ") and bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦሾ"))):
        return {
            bstack11l11l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሿ"): bstack11l11l_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨቀ"),
            bstack11l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢቁ"): env.get(bstack11l11l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦቂ")),
            bstack11l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣቃ"): env.get(bstack11l11l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧቄ")),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቅ"): env.get(bstack11l11l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧቆ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠥࡇࡎࠨቇ")) == bstack11l11l_opy_ (u"ࠦࡹࡸࡵࡦࠤቈ") and bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣ቉"))):
        return {
            bstack11l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቊ"): bstack11l11l_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢቋ"),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቌ"): env.get(bstack11l11l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨቍ")),
            bstack11l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ቎"): env.get(bstack11l11l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ቏")),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦቐ"): env.get(bstack11l11l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤቑ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠢࡄࡋࠥቒ")) == bstack11l11l_opy_ (u"ࠣࡶࡵࡹࡪࠨቓ") and bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧቔ"))):
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣቕ"): bstack11l11l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢቖ"),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ቗"): env.get(bstack11l11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧቘ")),
            bstack11l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ቙"): env.get(bstack11l11l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥቚ")) or env.get(bstack11l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧቛ")),
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቜ"): env.get(bstack11l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨቝ"))
        }
    if bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢ቞"))):
        return {
            bstack11l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ቟"): bstack11l11l_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢበ"),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቡ"): bstack11l11l_opy_ (u"ࠤࡾࢁࢀࢃࠢቢ").format(env.get(bstack11l11l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ባ")), env.get(bstack11l11l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫቤ"))),
            bstack11l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢብ"): env.get(bstack11l11l_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧቦ")),
            bstack11l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨቧ"): env.get(bstack11l11l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣቨ"))
        }
    if bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦቩ"))):
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣቪ"): bstack11l11l_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨቫ"),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣቬ"): bstack11l11l_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧቭ").format(env.get(bstack11l11l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ቮ")), env.get(bstack11l11l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩቯ")), env.get(bstack11l11l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪተ")), env.get(bstack11l11l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧቱ"))),
            bstack11l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቲ"): env.get(bstack11l11l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤታ")),
            bstack11l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቴ"): env.get(bstack11l11l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣት"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤቶ")) and env.get(bstack11l11l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦቷ")):
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣቸ"): bstack11l11l_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨቹ"),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣቺ"): bstack11l11l_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤቻ").format(env.get(bstack11l11l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪቼ")), env.get(bstack11l11l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ች")), env.get(bstack11l11l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩቾ"))),
            bstack11l11l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧቿ"): env.get(bstack11l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦኀ")),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦኁ"): env.get(bstack11l11l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨኂ"))
        }
    if any([env.get(bstack11l11l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧኃ")), env.get(bstack11l11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢኄ")), env.get(bstack11l11l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨኅ"))]):
        return {
            bstack11l11l_opy_ (u"ࠥࡲࡦࡳࡥࠣኆ"): bstack11l11l_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦኇ"),
            bstack11l11l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣኈ"): env.get(bstack11l11l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ኉")),
            bstack11l11l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤኊ"): env.get(bstack11l11l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨኋ")),
            bstack11l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣኌ"): env.get(bstack11l11l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣኍ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤ኎")):
        return {
            bstack11l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ኏"): bstack11l11l_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨነ"),
            bstack11l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥኑ"): env.get(bstack11l11l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥኒ")),
            bstack11l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦና"): env.get(bstack11l11l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤኔ")),
            bstack11l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥን"): env.get(bstack11l11l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥኖ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢኗ")) or env.get(bstack11l11l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤኘ")):
        return {
            bstack11l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨኙ"): bstack11l11l_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥኚ"),
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨኛ"): env.get(bstack11l11l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣኜ")),
            bstack11l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢኝ"): bstack11l11l_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨኞ") if env.get(bstack11l11l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤኟ")) else None,
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢአ"): env.get(bstack11l11l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢኡ"))
        }
    if any([env.get(bstack11l11l_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣኢ")), env.get(bstack11l11l_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧኣ")), env.get(bstack11l11l_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧኤ"))]):
        return {
            bstack11l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦእ"): bstack11l11l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨኦ"),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦኧ"): None,
            bstack11l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦከ"): env.get(bstack11l11l_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢኩ")),
            bstack11l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥኪ"): env.get(bstack11l11l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢካ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤኬ")):
        return {
            bstack11l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧክ"): bstack11l11l_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦኮ"),
            bstack11l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧኯ"): env.get(bstack11l11l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤኰ")),
            bstack11l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ኱"): bstack11l11l_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨኲ").format(env.get(bstack11l11l_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩኳ"))) if env.get(bstack11l11l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥኴ")) else None,
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢኵ"): env.get(bstack11l11l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ኶"))
        }
    if bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦ኷"))):
        return {
            bstack11l11l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኸ"): bstack11l11l_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨኹ"),
            bstack11l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤኺ"): env.get(bstack11l11l_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦኻ")),
            bstack11l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኼ"): env.get(bstack11l11l_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧኽ")),
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤኾ"): env.get(bstack11l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ኿"))
        }
    if bstack1l1ll111l1_opy_(env.get(bstack11l11l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨዀ"))):
        return {
            bstack11l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ዁"): bstack11l11l_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣዂ"),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦዃ"): bstack11l11l_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥዄ").format(env.get(bstack11l11l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧዅ")), env.get(bstack11l11l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨ዆")), env.get(bstack11l11l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬ዇"))),
            bstack11l11l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣወ"): env.get(bstack11l11l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤዉ")),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢዊ"): env.get(bstack11l11l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤዋ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠥࡇࡎࠨዌ")) == bstack11l11l_opy_ (u"ࠦࡹࡸࡵࡦࠤው") and env.get(bstack11l11l_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧዎ")) == bstack11l11l_opy_ (u"ࠨ࠱ࠣዏ"):
        return {
            bstack11l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዐ"): bstack11l11l_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣዑ"),
            bstack11l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧዒ"): bstack11l11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨዓ").format(env.get(bstack11l11l_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨዔ"))),
            bstack11l11l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢዕ"): None,
            bstack11l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዖ"): None,
        }
    if env.get(bstack11l11l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥ዗")):
        return {
            bstack11l11l_opy_ (u"ࠣࡰࡤࡱࡪࠨዘ"): bstack11l11l_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦዙ"),
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዚ"): None,
            bstack11l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዛ"): env.get(bstack11l11l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨዜ")),
            bstack11l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዝ"): env.get(bstack11l11l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨዞ"))
        }
    if any([env.get(bstack11l11l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦዟ")), env.get(bstack11l11l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤዠ")), env.get(bstack11l11l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣዡ")), env.get(bstack11l11l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧዢ"))]):
        return {
            bstack11l11l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥዣ"): bstack11l11l_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤዤ"),
            bstack11l11l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥዥ"): None,
            bstack11l11l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥዦ"): env.get(bstack11l11l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥዧ")) or None,
            bstack11l11l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤየ"): env.get(bstack11l11l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨዩ"), 0)
        }
    if env.get(bstack11l11l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥዪ")):
        return {
            bstack11l11l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦያ"): bstack11l11l_opy_ (u"ࠢࡈࡱࡆࡈࠧዬ"),
            bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦይ"): None,
            bstack11l11l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦዮ"): env.get(bstack11l11l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣዯ")),
            bstack11l11l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥደ"): env.get(bstack11l11l_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦዱ"))
        }
    if env.get(bstack11l11l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦዲ")):
        return {
            bstack11l11l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧዳ"): bstack11l11l_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦዴ"),
            bstack11l11l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧድ"): env.get(bstack11l11l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤዶ")),
            bstack11l11l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዷ"): env.get(bstack11l11l_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣዸ")),
            bstack11l11l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧዹ"): env.get(bstack11l11l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧዺ"))
        }
    return {bstack11l11l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢዻ"): None}
def get_host_info():
    return {
        bstack11l11l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦዼ"): platform.node(),
        bstack11l11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧዽ"): platform.system(),
        bstack11l11l_opy_ (u"ࠦࡹࡿࡰࡦࠤዾ"): platform.machine(),
        bstack11l11l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨዿ"): platform.version(),
        bstack11l11l_opy_ (u"ࠨࡡࡳࡥ࡫ࠦጀ"): platform.architecture()[0]
    }
def bstack1llll11l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111lll11l1_opy_():
    if bstack111l11111_opy_.get_property(bstack11l11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨጁ")):
        return bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧጂ")
    return bstack11l11l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨጃ")
def bstack11l1111l11_opy_(driver):
    info = {
        bstack11l11l_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩጄ"): driver.capabilities,
        bstack11l11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨጅ"): driver.session_id,
        bstack11l11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ጆ"): driver.capabilities.get(bstack11l11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫጇ"), None),
        bstack11l11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩገ"): driver.capabilities.get(bstack11l11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩጉ"), None),
        bstack11l11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫጊ"): driver.capabilities.get(bstack11l11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩጋ"), None),
    }
    if bstack111lll11l1_opy_() == bstack11l11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪጌ"):
        info[bstack11l11l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ግ")] = bstack11l11l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬጎ") if bstack1l1llll1ll_opy_() else bstack11l11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩጏ")
    return info
def bstack1l1llll1ll_opy_():
    if bstack111l11111_opy_.get_property(bstack11l11l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧጐ")):
        return True
    if bstack1l1ll111l1_opy_(os.environ.get(bstack11l11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ጑"), None)):
        return True
    return False
def bstack1llll11l1_opy_(bstack111ll1l111_opy_, url, data, config):
    headers = config.get(bstack11l11l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫጒ"), None)
    proxies = bstack1ll111l1l_opy_(config, url)
    auth = config.get(bstack11l11l_opy_ (u"ࠫࡦࡻࡴࡩࠩጓ"), None)
    response = requests.request(
            bstack111ll1l111_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll111l1ll_opy_(bstack1lll1lll11_opy_, size):
    bstack1l1lll1111_opy_ = []
    while len(bstack1lll1lll11_opy_) > size:
        bstack1ll1l1lll_opy_ = bstack1lll1lll11_opy_[:size]
        bstack1l1lll1111_opy_.append(bstack1ll1l1lll_opy_)
        bstack1lll1lll11_opy_ = bstack1lll1lll11_opy_[size:]
    bstack1l1lll1111_opy_.append(bstack1lll1lll11_opy_)
    return bstack1l1lll1111_opy_
def bstack111ll1l1l1_opy_(message, bstack111l1l11ll_opy_=False):
    os.write(1, bytes(message, bstack11l11l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫጔ")))
    os.write(1, bytes(bstack11l11l_opy_ (u"࠭࡜࡯ࠩጕ"), bstack11l11l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭጖")))
    if bstack111l1l11ll_opy_:
        with open(bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧ጗") + os.environ[bstack11l11l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨጘ")] + bstack11l11l_opy_ (u"ࠪ࠲ࡱࡵࡧࠨጙ"), bstack11l11l_opy_ (u"ࠫࡦ࠭ጚ")) as f:
            f.write(message + bstack11l11l_opy_ (u"ࠬࡢ࡮ࠨጛ"))
def bstack111l1ll1l1_opy_():
    return os.environ[bstack11l11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩጜ")].lower() == bstack11l11l_opy_ (u"ࠧࡵࡴࡸࡩࠬጝ")
def bstack1ll1llll1_opy_(bstack111l1l1l1l_opy_):
    return bstack11l11l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧጞ").format(bstack11l111l11l_opy_, bstack111l1l1l1l_opy_)
def bstack1lllll11_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack11l11l_opy_ (u"ࠩ࡝ࠫጟ")
def bstack111ll1ll1l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l11l_opy_ (u"ࠪ࡞ࠬጠ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l11l_opy_ (u"ࠫ࡟࠭ጡ")))).total_seconds() * 1000
def bstack11l1111111_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack11l11l_opy_ (u"ࠬࡠࠧጢ")
def bstack111l1ll111_opy_(bstack111llll11l_opy_):
    date_format = bstack11l11l_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫጣ")
    bstack111lll1l11_opy_ = datetime.datetime.strptime(bstack111llll11l_opy_, date_format)
    return bstack111lll1l11_opy_.isoformat() + bstack11l11l_opy_ (u"࡛ࠧࠩጤ")
def bstack111l1l1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨጥ")
    else:
        return bstack11l11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩጦ")
def bstack1l1ll111l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l11l_opy_ (u"ࠪࡸࡷࡻࡥࠨጧ")
def bstack111l1lll11_opy_(val):
    return val.__str__().lower() == bstack11l11l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪጨ")
def bstack1l1111l11l_opy_(bstack111l1l11l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l1l11l1_opy_ as e:
                print(bstack11l11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧጩ").format(func.__name__, bstack111l1l11l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111lllll1l_opy_(bstack111ll1l1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111ll1l1ll_opy_(cls, *args, **kwargs)
            except bstack111l1l11l1_opy_ as e:
                print(bstack11l11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨጪ").format(bstack111ll1l1ll_opy_.__name__, bstack111l1l11l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111lllll1l_opy_
    else:
        return decorator
def bstack111ll11l1_opy_(bstack11ll1llll1_opy_):
    if bstack11l11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫጫ") in bstack11ll1llll1_opy_ and bstack111l1lll11_opy_(bstack11ll1llll1_opy_[bstack11l11l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬጬ")]):
        return False
    if bstack11l11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫጭ") in bstack11ll1llll1_opy_ and bstack111l1lll11_opy_(bstack11ll1llll1_opy_[bstack11l11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬጮ")]):
        return False
    return True
def bstack1111ll1l_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack11ll1l1l1_opy_(hub_url):
    if bstack1l1ll1l1_opy_() <= version.parse(bstack11l11l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫጯ")):
        if hub_url != bstack11l11l_opy_ (u"ࠬ࠭ጰ"):
            return bstack11l11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢጱ") + hub_url + bstack11l11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦጲ")
        return bstack1111l11l1_opy_
    if hub_url != bstack11l11l_opy_ (u"ࠨࠩጳ"):
        return bstack11l11l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦጴ") + hub_url + bstack11l11l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦጵ")
    return bstack1l11l11ll_opy_
def bstack111ll11lll_opy_():
    return isinstance(os.getenv(bstack11l11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪጶ")), str)
def bstack111l1111_opy_(url):
    return urlparse(url).hostname
def bstack1111ll1l1_opy_(hostname):
    for bstack111ll11l_opy_ in bstack1lll1ll1ll_opy_:
        regex = re.compile(bstack111ll11l_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111llllll1_opy_(bstack111l1ll1ll_opy_, file_name, logger):
    bstack11lllll1_opy_ = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"ࠬࢄࠧጷ")), bstack111l1ll1ll_opy_)
    try:
        if not os.path.exists(bstack11lllll1_opy_):
            os.makedirs(bstack11lllll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l11l_opy_ (u"࠭ࡾࠨጸ")), bstack111l1ll1ll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l11l_opy_ (u"ࠧࡸࠩጹ")):
                pass
            with open(file_path, bstack11l11l_opy_ (u"ࠣࡹ࠮ࠦጺ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1ll1l11_opy_.format(str(e)))
def bstack111ll1lll1_opy_(file_name, key, value, logger):
    file_path = bstack111llllll1_opy_(bstack11l11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩጻ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11l1l11l_opy_ = json.load(open(file_path, bstack11l11l_opy_ (u"ࠪࡶࡧ࠭ጼ")))
        else:
            bstack1l11l1l11l_opy_ = {}
        bstack1l11l1l11l_opy_[key] = value
        with open(file_path, bstack11l11l_opy_ (u"ࠦࡼ࠱ࠢጽ")) as outfile:
            json.dump(bstack1l11l1l11l_opy_, outfile)
def bstack1lllll11ll_opy_(file_name, logger):
    file_path = bstack111llllll1_opy_(bstack11l11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬጾ"), file_name, logger)
    bstack1l11l1l11l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l11l_opy_ (u"࠭ࡲࠨጿ")) as bstack1l1l111l1_opy_:
            bstack1l11l1l11l_opy_ = json.load(bstack1l1l111l1_opy_)
    return bstack1l11l1l11l_opy_
def bstack1l1111111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫፀ") + file_path + bstack11l11l_opy_ (u"ࠨࠢࠪፁ") + str(e))
def bstack1l1ll1l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l11l_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦፂ")
def bstack1llll1ll1l_opy_(config):
    if bstack11l11l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩፃ") in config:
        del (config[bstack11l11l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪፄ")])
        return False
    if bstack1l1ll1l1_opy_() < version.parse(bstack11l11l_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫፅ")):
        return False
    if bstack1l1ll1l1_opy_() >= version.parse(bstack11l11l_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬፆ")):
        return True
    if bstack11l11l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧፇ") in config and config[bstack11l11l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨፈ")] is False:
        return False
    else:
        return True
def bstack1ll111lll_opy_(args_list, bstack111lllllll_opy_):
    index = -1
    for value in bstack111lllllll_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l1111llll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l1111llll_opy_ = bstack1l1111llll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩፉ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l11l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪፊ"), exception=exception)
    def bstack11ll1l111l_opy_(self):
        if self.result != bstack11l11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫፋ"):
            return None
        if bstack11l11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣፌ") in self.exception_type:
            return bstack11l11l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢፍ")
        return bstack11l11l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣፎ")
    def bstack11l1111ll1_opy_(self):
        if self.result != bstack11l11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨፏ"):
            return None
        if self.bstack1l1111llll_opy_:
            return self.bstack1l1111llll_opy_
        return bstack111ll1111l_opy_(self.exception)
def bstack111ll1111l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111lll1l1l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack111111ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l11lll111_opy_(config, logger):
    try:
        import playwright
        bstack111ll1l11l_opy_ = playwright.__file__
        bstack11l1111lll_opy_ = os.path.split(bstack111ll1l11l_opy_)
        bstack111lll1ll1_opy_ = bstack11l1111lll_opy_[0] + bstack11l11l_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬፐ")
        os.environ[bstack11l11l_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ፑ")] = bstack1l1l11111_opy_(config)
        with open(bstack111lll1ll1_opy_, bstack11l11l_opy_ (u"ࠫࡷ࠭ፒ")) as f:
            bstack11111ll11_opy_ = f.read()
            bstack11l11111l1_opy_ = bstack11l11l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫፓ")
            bstack111l1llll1_opy_ = bstack11111ll11_opy_.find(bstack11l11111l1_opy_)
            if bstack111l1llll1_opy_ == -1:
              process = subprocess.Popen(bstack11l11l_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥፔ"), shell=True, cwd=bstack11l1111lll_opy_[0])
              process.wait()
              bstack111lll11ll_opy_ = bstack11l11l_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧፕ")
              bstack11l111111l_opy_ = bstack11l11l_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧፖ")
              bstack111l1lll1l_opy_ = bstack11111ll11_opy_.replace(bstack111lll11ll_opy_, bstack11l111111l_opy_)
              with open(bstack111lll1ll1_opy_, bstack11l11l_opy_ (u"ࠩࡺࠫፗ")) as f:
                f.write(bstack111l1lll1l_opy_)
    except Exception as e:
        logger.error(bstack1l1l11ll1l_opy_.format(str(e)))
def bstack11l1llll1_opy_():
  try:
    bstack111l1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪፘ"))
    bstack111l1lllll_opy_ = []
    if os.path.exists(bstack111l1l1111_opy_):
      with open(bstack111l1l1111_opy_) as f:
        bstack111l1lllll_opy_ = json.load(f)
      os.remove(bstack111l1l1111_opy_)
    return bstack111l1lllll_opy_
  except:
    pass
  return []
def bstack1l1lll11l_opy_(bstack1l1l11l1l_opy_):
  try:
    bstack111l1lllll_opy_ = []
    bstack111l1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫፙ"))
    if os.path.exists(bstack111l1l1111_opy_):
      with open(bstack111l1l1111_opy_) as f:
        bstack111l1lllll_opy_ = json.load(f)
    bstack111l1lllll_opy_.append(bstack1l1l11l1l_opy_)
    with open(bstack111l1l1111_opy_, bstack11l11l_opy_ (u"ࠬࡽࠧፚ")) as f:
        json.dump(bstack111l1lllll_opy_, f)
  except:
    pass
def bstack1l1ll11111_opy_(logger, bstack111l11lll1_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l11l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ፛"), bstack11l11l_opy_ (u"ࠧࠨ፜"))
    if test_name == bstack11l11l_opy_ (u"ࠨࠩ፝"):
        test_name = threading.current_thread().__dict__.get(bstack11l11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨ፞"), bstack11l11l_opy_ (u"ࠪࠫ፟"))
    bstack111l11llll_opy_ = bstack11l11l_opy_ (u"ࠫ࠱ࠦࠧ፠").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111l11lll1_opy_:
        bstack1ll11lll_opy_ = os.environ.get(bstack11l11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ፡"), bstack11l11l_opy_ (u"࠭࠰ࠨ።"))
        bstack1llll1l1ll_opy_ = {bstack11l11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ፣"): test_name, bstack11l11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ፤"): bstack111l11llll_opy_, bstack11l11l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ፥"): bstack1ll11lll_opy_}
        bstack111lll1lll_opy_ = []
        bstack111llll111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩ፦"))
        if os.path.exists(bstack111llll111_opy_):
            with open(bstack111llll111_opy_) as f:
                bstack111lll1lll_opy_ = json.load(f)
        bstack111lll1lll_opy_.append(bstack1llll1l1ll_opy_)
        with open(bstack111llll111_opy_, bstack11l11l_opy_ (u"ࠫࡼ࠭፧")) as f:
            json.dump(bstack111lll1lll_opy_, f)
    else:
        bstack1llll1l1ll_opy_ = {bstack11l11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ፨"): test_name, bstack11l11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ፩"): bstack111l11llll_opy_, bstack11l11l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭፪"): str(multiprocessing.current_process().name)}
        if bstack11l11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬ፫") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1llll1l1ll_opy_)
  except Exception as e:
      logger.warn(bstack11l11l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ፬").format(e))
def bstack1l11l1l1_opy_(error_message, test_name, index, logger):
  try:
    bstack111lll111l_opy_ = []
    bstack1llll1l1ll_opy_ = {bstack11l11l_opy_ (u"ࠪࡲࡦࡳࡥࠨ፭"): test_name, bstack11l11l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ፮"): error_message, bstack11l11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ፯"): index}
    bstack111l1l1ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11l11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧ፰"))
    if os.path.exists(bstack111l1l1ll1_opy_):
        with open(bstack111l1l1ll1_opy_) as f:
            bstack111lll111l_opy_ = json.load(f)
    bstack111lll111l_opy_.append(bstack1llll1l1ll_opy_)
    with open(bstack111l1l1ll1_opy_, bstack11l11l_opy_ (u"ࠧࡸࠩ፱")) as f:
        json.dump(bstack111lll111l_opy_, f)
  except Exception as e:
    logger.warn(bstack11l11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ፲").format(e))
def bstack1l11l11l1_opy_(bstack111ll11ll_opy_, name, logger):
  try:
    bstack1llll1l1ll_opy_ = {bstack11l11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ፳"): name, bstack11l11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ፴"): bstack111ll11ll_opy_, bstack11l11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ፵"): str(threading.current_thread()._name)}
    return bstack1llll1l1ll_opy_
  except Exception as e:
    logger.warn(bstack11l11l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ፶").format(e))
  return
def bstack111ll1llll_opy_():
    return platform.system() == bstack11l11l_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧ፷")
def bstack11l1l11l1_opy_(bstack111ll11111_opy_, config, logger):
    bstack111l1l111l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack111ll11111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l11l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ፸").format(e))
    return bstack111l1l111l_opy_
def bstack111l1ll11l_opy_(bstack111ll11l11_opy_, bstack111ll1ll11_opy_):
    bstack11l11111ll_opy_ = version.parse(bstack111ll11l11_opy_)
    bstack11l1111l1l_opy_ = version.parse(bstack111ll1ll11_opy_)
    if bstack11l11111ll_opy_ > bstack11l1111l1l_opy_:
        return 1
    elif bstack11l11111ll_opy_ < bstack11l1111l1l_opy_:
        return -1
    else:
        return 0