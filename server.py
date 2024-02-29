from aiohttp import web
import json
from models import engine, init_db, Session, User, Advertisement
from sqlalchemy.exc import IntegrityError

app = web.Application()

# Контекстный менеджер (миграции)
async def orm_context(app):
    print('start server !!')
    print(' - # '*13)
    await init_db()
    yield
    await engine.dispose()
    print(' :      _finish !')
app.cleanup_ctx.append(orm_context)

# обёртка для сессии
@web.middleware
async def session_middleware(request, handler):
	async with Session() as session :
		request.session = session
		response = await handler(request)
		return response
app.middlewares.append(session_middleware)

# асф получения юзера и НЕасф ошибок
def get_error(error_class, message):
	return error_class(text= json.dumps({'error':message}), 
		content_type='application/json')

async def get_user_by_id(session, user_id):
	user = await session.get(User, user_id)
	if user is None:
		raise get_error(error_class= web.HTTPNotFound, 
			message= f'User with id {user_id} not found' )
	return user

async def add_user(session, user):
	try:
		session.add(user)
		await session.commit() 
	except IntegrityError:
		raise get_error(error_class= web.HTTPConflict, 
			message= f'User with name {user.name} already exists')
	return user.id




class UserView(web.View):
	
    @property
    def session(self):
        return self.request.session

    @property
    def user_id(self):
        return int(self.request.match_info['user_id']) 
	
    async def get_user(self):
        user = await get_user_by_id(self.session, self.user_id)
        return user

    # HANDLERS
    async def get(self):
        user = await self.get_user()
        return web.json_response(user.make_dict)
 
    async def post(self):
        user_data = await self.request.json()
        user = User(**user_data)
        await add_user(self.session, user)
        return web.json_response(user.make_dict)

# funk for advertisements

async def get_adv_by_id(session, adv_id):
    adv = await session.get(Advertisement, adv_id)
    if adv is None :
        raise get_error(error_class= web.HTTPNotFound, 
                        message= f'Advertisement with id {adv_id} not found' )
    return adv

async def add_adv(session, adv: Advertisement):
    try:
        session.add(adv)
        await session.commit() 
    except IntegrityError :
        raise get_error(error_class= web.HTTPNotFound, message= f'owner is not found')
    # return adv.id



class AdvertisementView(web.View):
	
    @property
    def session(self):
        return self.request.session
    
    @property
    def adv_id(self):
        return int(self.request.match_info['adv_id']) 
	
    async def get_advertisement(self):
        adv = await get_adv_by_id(self.session, self.adv_id)
        return adv


    # HANDLERS

    async def get(self):
        adv = await self.get_advertisement()
        return web.json_response(adv.make_dict)

    async def post(self):
        adv_data = await self.request.json()     
        adv = Advertisement(**adv_data)
        await add_adv(self.session, adv)
        return web.json_response(adv.make_dict)

    async def delete(self):
        adv = await self.get_advertisement()
        await self.session.delete(adv)
        await self.session.commit()
        return web.json_response({'status': 'delete'})










# ROUTS
app.add_routes([
	web.get('/user/{user_id:\d+}', UserView),
	web.post('/user', UserView),
      
	web.get('/advertisement/{adv_id:\d+}', AdvertisementView),
	web.post('/advertisement', AdvertisementView),
	web.delete('/advertisement/{adv_id:\d+}', AdvertisementView),
])


# START APP
web.run_app(app)