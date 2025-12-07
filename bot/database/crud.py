from datetime import datetime
from sqlalchemy import select, text, insert, update

from database.database import AsyncSession, connection, Users, Reminds

@connection
async def add_user(tg_id: int, session: AsyncSession):
    result = await session.execute(select(Users).where(Users.tg_id == tg_id))


    is_user = result.scalar_one_or_none()


    if is_user: pass
    else:
        user = Users(tg_id=tg_id, email=None, additional_remind_status=False)       
        session.add(user)

@connection
async def get_user(tg_id: int, session: AsyncSession):
    user = await session.execute(select(Users).where(Users.tg_id == tg_id))
    return user.scalar_one_or_none()

@connection
async def get_user_by_id(uid: int, session: AsyncSession):
    user = await session.execute(select(Users).where(Users.id == uid))
    return user.scalar_one_or_none()

# temp - функция
@connection 
async def clear_all_tables(session: AsyncSession):
    await session.execute(text("DROP TABLE Users CASCADE;"))
    await session.execute(text("DROP TABLE Reminds CASCADE;"))
    


@connection
async def add_remind(tg_id: int, date: datetime, text: str, session: AsyncSession):
    user = await get_user(tg_id=tg_id, session=session)
    remind = Reminds(user_id=user.id, date=date, text=text)
    session.add(remind)

    return remind

@connection
async def get_reminds_user(tg_id: int, session: AsyncSession):
    user = await get_user(tg_id=tg_id, session=session)

    reminds = await session.execute(select(Reminds).where(Reminds.user_id == user.id))

    return reminds.scalars().all()

async def is_count_reminds_less_fifteen(tg_id: int):
    reminds = await get_reminds_user(tg_id=tg_id)
    return len(reminds) <= 15


@connection
async def get_all_reminds(session: AsyncSession):
    reminds = await session.execute(select(Reminds))
    return reminds.scalars().all()


@connection
async def del_remind(rid: int, session: AsyncSession):
    result = await session.execute(select(Reminds).where(Reminds.id == rid))

    remind_to_delete = result.scalar_one_or_none()
     
    if remind_to_delete:
        await session.delete(remind_to_delete)
   
   
@connection
async def set_or_del_email(tg_id: int, email: str, session: AsyncSession):
    stmt = (
        update(Users)
        .where(Users.tg_id == tg_id)
        .values(email=email)
        .returning(Users.email)  
    )
    
    result = await session.execute(stmt)
    new_email = result.scalar_one_or_none()
    
    if new_email is not None:
        return True
    else:
        return False
    
@connection
async def switch_additional_remind_status(tg_id: int, session: AsyncSession):
    user = await get_user(tg_id=tg_id)
    stmt = (
        update(Users)
        .where(Users.tg_id == tg_id)
        .values(additional_remind_status = not user.additional_remind_status)
        .returning(Users.additional_remind_status)  
    )

    result = await session.execute(stmt)
    status = result.scalar_one_or_none()
    return status

@connection
async def get_additional_remind_status(tg_id: int, session: AsyncSession):
    user = await get_user(tg_id=tg_id, session=session)
    return user.additional_remind_status
    

