from fastapi import APIRouter, HTTPException, status, Path
from bson import ObjectId
from models.teen import TeenModel, PhoneUsageModel, MentalHealthModel, AppUsageModel
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional

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
#       CREATE ENDPOINTS
# ----------------------------

@router.post("/teens", response_model=TeenModel, status_code=status.HTTP_201_CREATED)
async def create_teen(teen: TeenModel):
    """
    Create a new Teen document.
    """
    # Serialize the incoming Pydantic model to dict
    teen_data = teen.model_dump()  
    result = await teens_collection.insert_one(teen_data)
    
    created = await teens_collection.find_one({"_id": result.inserted_id})
    # Convert ObjectId to string ID
    created["id"] = str(created["_id"])
    del created["_id"]
    return created


@router.post("/phone-usage", response_model=PhoneUsageModel, status_code=status.HTTP_201_CREATED)
async def create_phone_usage(usage: PhoneUsageModel):
    """
    Create a new PhoneUsage document.
    """
    usage_data = usage.model_dump()
    result = await phone_usage_collection.insert_one(usage_data)
    
    created = await phone_usage_collection.find_one({"_id": result.inserted_id})
    created["id"] = str(created["_id"])
    created["teen_id"] = str(created["teen_id"])
    del created["_id"]
    return created


@router.post("/mental-health", response_model=MentalHealthModel, status_code=status.HTTP_201_CREATED)
async def create_mental_health(stats: MentalHealthModel):
    """
    Create a new MentalHealth document.
    """
    stats_data = stats.model_dump()
    result = await mental_health_collection.insert_one(stats_data)
    
    created = await mental_health_collection.find_one({"_id": result.inserted_id})
    created["id"] = str(created["_id"])
    created["teen_id"] = str(created["teen_id"])
    del created["_id"]
    return created


@router.post("/app-usage", response_model=AppUsageModel, status_code=status.HTTP_201_CREATED)
async def create_app_usage(app: AppUsageModel):
    """
    Create a new AppUsage document.
    """
    app_data = app.model_dump()
    result = await app_usage_collection.insert_one(app_data)
    
    created = await app_usage_collection.find_one({"_id": result.inserted_id})
    created["id"] = str(created["_id"])
    created["teen_id"] = str(created["teen_id"])
    del created["_id"]
    return created



# ----------------------------
#        READ ENDPOINTS
# ----------------------------

@router.get("/teens", response_model=List[TeenModel])
async def list_teens():
    """
    Retrieve all Teen documents.
    """
    docs = []
    cursor = teens_collection.find({})
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        docs.append(doc)
    return docs


@router.get("/teens/{id}", response_model=TeenModel)
async def get_teen(id: str = Path(..., description="MongoDB ObjectId of the Teen document")):
    """
    Retrieve a single Teen by its ObjectId.
    """
    oid = validate_object_id(id)
    doc = await teens_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="Teen not found")
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


@router.get("/phone-usage", response_model=List[PhoneUsageModel])
async def list_phone_usage():
    docs = []
    cursor = phone_usage_collection.find({})
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["teen_id"] = str(doc["teen_id"])
        del doc["_id"]
        docs.append(doc)
    return docs


@router.get("/phone-usage/{id}", response_model=PhoneUsageModel)
async def get_phone_usage(id: str):
    oid = validate_object_id(id)
    doc = await phone_usage_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="PhoneUsage not found")
    doc["id"] = str(doc["_id"])
    doc["teen_id"] = str(doc["teen_id"])
    del doc["_id"]
    return doc


@router.get("/mental-health", response_model=List[MentalHealthModel])
async def list_mental_health():
    docs = []
    cursor = mental_health_collection.find({})
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["teen_id"] = str(doc["teen_id"])
        del doc["_id"]
        docs.append(doc)
    return docs


@router.get("/mental-health/{id}", response_model=MentalHealthModel)
async def get_mental_health(id: str):
    oid = validate_object_id(id)
    doc = await mental_health_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="MentalHealth not found")
    doc["id"] = str(doc["_id"])
    doc["teen_id"] = str(doc["teen_id"])
    del doc["_id"]
    return doc


@router.get("/app-usage", response_model=List[AppUsageModel])
async def list_app_usage():
    docs = []
    cursor = app_usage_collection.find({})
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc["teen_id"] = str(doc["teen_id"])
        del doc["_id"]
        docs.append(doc)
    return docs


@router.get("/app-usage/{id}", response_model=AppUsageModel)
async def get_app_usage(id: str):
    oid = validate_object_id(id)
    doc = await app_usage_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="AppUsage not found")
    doc["id"] = str(doc["_id"])
    doc["teen_id"] = str(doc["teen_id"])
    del doc["_id"]
    return doc


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
