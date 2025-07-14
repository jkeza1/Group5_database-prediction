from fastapi import APIRouter, HTTPException, status, Path
from bson import ObjectId
from models.teen import TeenModel, PhoneUsageModel, MentalHealthModel, AppUsageModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

# Initialize router
router = APIRouter()

# MongoDB client and collections
client = AsyncIOMotorClient("mongodb+srv://Igaius:Bingo000@cluster0.yfs4grd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["teen_phone_survey"]

teens_collection = db["Teens"]
phone_usage_collection = db["PhoneUsage"]
mental_health_collection = db["MentalHealth"]
app_usage_collection = db["AppUsage"]

# Helper: Validate ObjectId
def validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    return ObjectId(id)

# ----------------------------
#         UPDATE ENDPOINTS
# ----------------------------
@router.put("/teens/{id}", response_model=TeenModel)
async def update_teen(id: str = Path(..., description="MongoDB ObjectId of the Teen document"),
                      teen: TeenModel = None):
    """
    Update a Teen document by ObjectId.
    """
    print(f"Updating teen with id: {id}")
    oid = validate_object_id(id)

    update_data = {k: v for k, v in teen.model_dump(exclude_unset=True).items() if k != "id"}
    print(f"Update data: {update_data}")

    result = await teens_collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        print(f"No teen found with id: {id}")
        raise HTTPException(status_code=404, detail="Teen not found")

    updated_doc = await teens_collection.find_one({"_id": oid})
    if updated_doc:
        
        updated_doc["id"] = str(updated_doc["_id"])
        del updated_doc["_id"]

    print(f"Update successful for id: {id}")
    return updated_doc

@router.put("/phone-usage/{id}", response_model=PhoneUsageModel)
async def update_phone_usage(id: str, usage: PhoneUsageModel):
    """
    Update a PhoneUsage document by ObjectId.
    """
    print(f"Updating phone usage with id: {id}")
    oid = validate_object_id(id)

    update_data = {k: v for k, v in usage.model_dump(exclude_unset=True).items() if k != "id"}
    print(f"Update data: {update_data}")

    result = await phone_usage_collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        print(f"No phone usage found with id: {id}")
        raise HTTPException(status_code=404, detail="PhoneUsage not found")

    updated_doc = await phone_usage_collection.find_one({"_id": oid})
    if updated_doc:
        updated_doc["id"] = str(updated_doc["_id"])
        updated_doc["teen_id"] = str(updated_doc["teen_id"])
        del updated_doc["_id"]

    print(f"Update successful for id: {id}")
    return updated_doc


@router.put("/mental-health/{id}", response_model=MentalHealthModel)
async def update_mental_health(id: str, stats: MentalHealthModel):
    """
    Update a MentalHealth document by ObjectId.
    """
    print(f"Updating mental health with id: {id}")
    oid = validate_object_id(id)

    update_data = {k: v for k, v in stats.model_dump(exclude_unset=True).items() if k != "id"}
    print(f"Update data: {update_data}")

    result = await mental_health_collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        print(f"No mental health record found with id: {id}")
        raise HTTPException(status_code=404, detail="MentalHealth entry not found")

    updated_doc = await mental_health_collection.find_one({"_id": oid})
    if updated_doc:
        updated_doc["id"] = str(updated_doc["_id"])
        updated_doc["teen_id"] = str(updated_doc["teen_id"])
        del updated_doc["_id"]

    print(f"Update successful for id: {id}")
    return updated_doc


@router.put("/app-usage/{id}", response_model=AppUsageModel)
async def update_app_usage(id: str, app: AppUsageModel):
    """
    Update an AppUsage document by ObjectId.
    """
    print(f"Updating app usage with id: {id}")
    oid = validate_object_id(id)

    update_data = {k: v for k, v in app.model_dump(exclude_unset=True).items() if k != "id"}
    print(f"Update data: {update_data}")

    result = await app_usage_collection.update_one({"_id": oid}, {"$set": update_data})
    if result.matched_count == 0:
        print(f"No app usage found with id: {id}")
        raise HTTPException(status_code=404, detail="AppUsage not found")

    updated_doc = await app_usage_collection.find_one({"_id": oid})
    if updated_doc:
        updated_doc["id"] = str(updated_doc["_id"])
        updated_doc["teen_id"] = str(updated_doc["teen_id"])
        del updated_doc["_id"]

    print(f"Update successful for id: {id}")
    return updated_doc


# ----------------------------
#         DELETE ENDPOINTS
# ----------------------------

@router.delete("/teens/{id}", status_code=204)
async def delete_teen(id: str):
    """
    Delete a Teen document by ObjectId.
    """
    oid = validate_object_id(id)
    result = await teens_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Teen not found")
    return


@router.delete("/phone-usage/{id}", status_code=204)
async def delete_phone_usage(id: str):
    """
    Delete a PhoneUsage document by ObjectId.
    """
    oid = validate_object_id(id)
    result = await phone_usage_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="PhoneUsage not found")
    return


@router.delete("/mental-health/{id}", status_code=204)
async def delete_mental_health(id: str):
    """
    Delete a MentalHealth document by ObjectId.
    """
    oid = validate_object_id(id)
    result = await mental_health_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="MentalHealth entry not found")
    return


@router.delete("/app-usage/{id}", status_code=204)
async def delete_app_usage(id: str):
    """
    Delete an AppUsage document by ObjectId.
    """
    oid = validate_object_id(id)
    result = await app_usage_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="AppUsage not found")
    return
