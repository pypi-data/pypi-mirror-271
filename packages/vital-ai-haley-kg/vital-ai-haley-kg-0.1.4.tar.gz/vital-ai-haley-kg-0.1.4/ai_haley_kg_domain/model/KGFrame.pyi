
import datetime
from ai_haley_kg_domain.model.KGNode import KGNode


class KGFrame(KGNode):
        frameGraphURI: str
        frameSequence: int
        kGBeliefModeType: str
        kGExpressionType: str
        kGFrameType: str
        kGFrameTypeDescription: str
        parentFrameURI: str

