from re import S
from pydantic import BaseModel
from typing import Optional, List
from enum import IntEnum

class OrganicProductionType(IntEnum):
    Conventional = 0
    Organic = 1
    Undetermined = 2
    
class FADNProductJsonDTO(BaseModel):
    fadnIdentifier: str
    description: str
    productType: str
    arable: bool
    
class PolicyJsonDTO(BaseModel):
    populationId: int
    policyIdentifier: str
    isCoupled: bool
    policyDescription: str
    economicCompensation: float

    
class PolicyGroupRelationJsonDTO(BaseModel):
    populationId: int
    policyIdentifier: str
    productGroupName: str
    economicCompensation: float
    
class ProductGroupJsonDTO(BaseModel):
    name: str
    productType: str
    originalNameDatasource: str
    productsIncludedInOriginalDataset: str
    modelSpecificCategories: List[str]
    organic: OrganicProductionType
    fadnProducts: List[FADNProductJsonDTO]
    
class LandRentJsonDTO(BaseModel):
    yearNumber: int
    originFarmCode: str
    destinationFarmCode: str
    # Total Rent Price [€]
    rentValue: float
    # Total Rent Area [ha]
    rentArea: float
    
class LandRentDTO(BaseModel):
    yearId: int
    originFarmId: int
    destinationFarmId: int
    # Total Rent Price [€]
    rentValue: float
    # Total Rent Area [ha]
    rentArea: float