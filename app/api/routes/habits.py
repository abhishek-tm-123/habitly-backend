from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.habit import HabitResponse,HabitCreate,HabitUpdate
from app.models.user import User
from app.models.habit import Habit
from app.dependencies import get_current_user
from app.db.database import get_db
from sqlalchemy import select

router = APIRouter(
    prefix="/habits",
    tags=["Habits"]
)

@router.post(
    "/",
    response_model=HabitResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_habit(
    data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    habit = Habit(
        name=data.name,
        user_id=current_user.id,
    )

    db.add(habit)

    await db.commit()
    await db.refresh(habit)

    return habit

@router.get(
    "/",
    response_model=list[HabitResponse],
)
async def get_habits(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Habit)
        .where(Habit.user_id == current_user.id)
        .order_by(Habit.id.desc())
    )

    habits = result.scalars().all()

    return habits

@router.patch(
    "/{habit_id}",
    response_model=HabitResponse,
)
async def update_habit(
    habit_id: int,
    data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == current_user.id,
        )
    )

    habit = result.scalar_one_or_none()

    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    if data.name is not None:
        habit.name = data.name

    if data.completed is not None:
        habit.completed = data.completed

    await db.commit()
    await db.refresh(habit)

    return habit
