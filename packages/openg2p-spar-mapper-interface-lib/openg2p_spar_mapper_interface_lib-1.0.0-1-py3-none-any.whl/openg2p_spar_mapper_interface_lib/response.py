from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class StatusEnum(Enum):
    rcvd = "rcvd"
    pdng = "pdng"
    succ = "succ"
    rjct = "rjct"


class MapperErrorCode(Enum):
    rjct_reference_id_invalid = "rjct.reference_id.invalid"
    rjct_reference_id_duplicate = "rjct.reference_id.duplicate"
    rjct_timestamp_invalid = "rjct.timestamp.invalid"
    rjct_id_invalid = "rjct.id.invalid"
    rjct_fa_invalid = "rjct.fa.invalid"
    rjct_name_invalid = "rjct.name.invalid"
    rjct_mobile_number_invalid = "rjct.mobile_number.invalid"
    rjct_unknown_retry = "rjct.unknown.retry"
    rjct_other_error = "rjct.other.error"


class MapperResponse(BaseModel):
    id: Optional[str] = None
    fa: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    account_provider_info: Optional[object] = (None,)
    additional_info: Optional[List[object]] = None
    status: Optional[str] = None
    mapper_error_code: Optional[str] = None
    mapper_error_message: Optional[str] = None
