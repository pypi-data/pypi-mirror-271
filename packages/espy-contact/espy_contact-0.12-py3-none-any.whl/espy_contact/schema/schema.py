"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from datetime import datetime, date
from pydantic import BaseModel, EmailStr,Field
from espy_contact.util.enums import AccessRoleEnum, StatusEnum
from typing import List, Optional, Union
import uuid
class ReachBase(BaseModel):
    id: str
    timestamp: datetime
class SeoRequest(BaseModel):
    url: str = Field(min_length=4, description="Your website url")
class WebbuilderRequest(BaseModel):
    id: str
    content: str
    product_id: int

class UserResponse(BaseModel):
    id: Optional[Union[str, int]] = str(uuid.uuid4())
    timestamp: Optional[datetime] = None
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool = False
    status: StatusEnum = StatusEnum.NEW
    role: List[AccessRoleEnum]
class AddressDto(BaseModel):
    id: Optional[str] = None
    street: str
    city: str
    state: str
    zip_code: int
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    country: str


class AppuserDto(UserResponse):
    password: str
    address: AddressDto

    class Config:
        from_attributes = True


class EnrollmentDto(UserResponse):
    dob: date
    gender: str
    nationality: str
    address: AddressDto
    parent_email: str
    current_school: str
    current_class: str
    achievements: str
    extracurricular: str
    parent_phone: str
    parent_name: str
    parent_occupation: str
    religion: str
    password: Optional[str] = None
    photo: Optional[Union[str, bytes]] = None
    birth_certificate: Optional[Union[str, bytes]] = None
    signature: str
    is_paid: Optional[bool] = False

    class Config:
        from_attributes = True


class SchoolDto(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    name: str
    address: AddressDto
    owner: str


class SchoolResponse(BaseModel):
    id: str
    name: str
    create_at: datetime
    address_id: str
    owner_id: str


class AcademicHistory(ReachBase):
    """Student or teacher can have multiple AcademicHistory."""

    school_name: str
    start_date: str
    end_date: str
    grade_level: str
    reason_for_leaving: str
    classroom: str  # ForeignKey to Classroom or String
    owner: AppuserDto  # ForeignKey to StudentProfile or None

    # teacher: Teacher  # Optional ForeignKey to Teacher (null allowed) or None
    class Config:
        from_attributes = True