from enum import Enum


class ObjectType(Enum):
    DOOR = "door"
    ELEVATOR = "elevator"
    IMAGE = "image"
    PERSONNEL = "personnel"

    @property
    def complete(self):
        if self == self.DOOR:
            return "SoftwareHouse.NextGen.Common.SecurityObjects.Door"
        if self == self.ELEVATOR:
            return "SoftwareHouse.NextGen.Common.SecurityObjects.Elevator"
        if self == self.IMAGE:
            return "SoftwareHouse.NextGen.Common.SecurityObjects.Images"
        if self == self.PERSONNEL:
            return "SoftwareHouse.NextGen.Common.SecurityObjects.Personnel"


class ImageType(Enum):
    UNKNOWN = 0
    PORTRAIT = 1
    SIGNATURE = 2
    FINGERPRINT = 3
    HANDPRINT = 4
    DYNAMIC_BADGE_IMAGE = 5
    STATIC_BADGE_IMAGE = 6
    SYSTEM_IMAGE = 7
    PRIVATE_IMAGE = 8
    SHARED_IMAGE = 9
