from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from typing import List

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", response_model=List[schemas.Item])
def get_items(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    """
    Get items of all users.
    """
    items = (
        db.query(models.Item)
        .filter(models.Item.name.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return items


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
def create_item(
    new_item: schemas.ItemBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Create item which belong to user.
    """
    item = models.Item(owner_id=current_user.id, **new_item.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{id}")
def get_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Get item of chosen id.
    """
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id: {id} not found",
        )

    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action",
        )
    return item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Delete item with chosen id.
    """
    item = db.query(models.Item).filter(models.Item.id == id)
    if item.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id:{id} does not exist",
        )
    if item.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action",
        )
    item.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Item)
def update_item(
    id: int,
    item: schemas.ItemBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Update item with chosen id.
    """
    item_query = db.query(models.Item).filter(models.Item.id == id)
    if item_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id:{id} does not exist",
        )
    if item_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Authorized to perform requested action",
        )
    print(item.dict())
    item_query.update(item.dict(), synchronize_session=False)
    db.commit()
    return item_query.first()


@router.patch("/book/{id}", response_model=schemas.Item)
def book_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Book item of chosen id.
    """
    print(current_user.email)
    item_query = db.query(models.Item).filter(models.Item.id == id)
    if not item_query.first().in_stock:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Already booked"
        )
    item_query.update({"in_stock": False, "booked_by": current_user.email})
    db.commit()
    return item_query.first()


@router.patch("/return/{id}", response_model=schemas.Item)
def return_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Rerun booked item.
    """
    item_query = db.query(models.Item).filter(models.Item.id == id)
    if (
        item_query.first().in_stock
        or item_query.first().booked_by != current_user.email
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't return item"
        )

    item_query.update({"in_stock": True, "booked_by": None})
    db.commit()
    return item_query.first()
