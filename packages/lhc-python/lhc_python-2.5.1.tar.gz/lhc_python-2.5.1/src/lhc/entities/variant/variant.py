from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Variant:
    chr: str
    pos: int
    ref: str
    alt: str
    id: Optional[str] = None
    qual: Optional[float] = None
    filter: Optional[str] = None
    info: Optional[Dict[str, str]] = None
    format: Optional[str] = None
    samples: Optional[Dict[str, Any]] = None
    lead: Optional[str] = None

    def __str__(self):
        res = []
        pos = self.pos
        ref = self.ref
        alt = self.alt
        if len(ref) > len(alt):
            d = len(ref) - len(alt)
            rng = str(pos + len(ref) - 1,) if d == 1 else '{}_{}'.format(pos + len(ref) - d, pos + len(ref) - 1)
            res.append('g.{}del'.format(rng))
        elif len(alt) > len(ref):
            res.append('g.{}_{}ins{}'.format(pos, pos + 1, alt))
        else:
            if len(ref) > 1 and ref == alt:
                res.append('g.{}_{}inv'.format(pos + 1, pos + len(ref)))
            else:
                res.append('g.{}{}>{}'.format(pos + 1, ref, alt))
        return ','.join(res)
