
import datetime
from vital_ai_vitalsigns_core.model.VITAL_PeerEdge import VITAL_PeerEdge


class Edge_hasKGEdge(VITAL_PeerEdge):
        edgeName: str
        kGDataHash: str
        kGGraphAssertionDateTime: datetime
        kGIndexDateTime: datetime
        kGIndexStatusURI: str
        kGModelVersion: str
        kGTenantIdentifier: str
        kGValidTypeURI: str
        kGVersion: str
        kGraphDescription: str

