from __future__ import annotations

from egglog import *

from .egglog_model import Bit

x, y, z = vars_("x y z", Bit)

bit_rules = ruleset(
    rewrite(x & Bit(1)).to(x),
    rewrite(x & Bit(0)).to(Bit(0)),
    rewrite(x | Bit(1)).to(Bit(1)),
    rewrite(x | Bit(0)).to(x),
    rewrite(x & x).to(x),
    rewrite(x | x).to(x),
    rewrite(x ^ x).to(Bit(0)),
    rewrite(x | ~x).to(Bit(1)),
    # 可交换/结合式简化的基础骨架，后面再扩展
    rewrite((x & y) | (x & z)).to(x & (y | z)),
)