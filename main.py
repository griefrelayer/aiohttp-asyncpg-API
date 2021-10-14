from datetime import datetime
from os import getenv
import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound
from aiohttp import web
from sqlalchemy import orm
from models import Employees, EmployeeCreateSchema, EmployeeUpdateSchema
from aiohttp_apispec import (
    request_schema,
    setup_aiohttp_apispec,
)
import aiohttp_sqlalchemy as ahsa

# Database configuration
db_type = getenv("DB_TYPE", "postgresql+asyncpg")
db_user = getenv("DB_USER", "docker")
db_password = getenv("DB_PASSWORD", "docker")
db_host = getenv("DB_HOST", "localhost")
db_port = getenv("DB_PORT", "5432")
db_name = getenv("DB_NAME", "staff")
metadata = sa.MetaData()
Base = orm.declarative_base(metadata=metadata)
CreateSchema = EmployeeCreateSchema()
UpdateSchema = EmployeeUpdateSchema()


async def list_employees(request):
    """
    API endpoint bound to /employees/ that returns list of Employees objects, works with GET method
    """
    sa_session = ahsa.get_session(request)
    result = await sa_session.execute(sa.select(Employees))
    result = result.scalars().all()
    return web.json_response([r.to_dict() for r in result])


async def retrieve_employee(request):
    """
    API endpoint bound to /employees/{id} that retrieves single Employees
    object by its integer id, works with GET method
    """
    sa_session = ahsa.get_session(request)
    result = await sa_session.execute(sa.select(Employees).where(Employees.id == int(request.match_info['id'])))
    result = result.scalar_one()
    return web.json_response(result.to_dict())


@request_schema(CreateSchema)
async def create_employee(request):
    """
    API endpoint bound to /employees/create that allows to create Employees object, works with POST method
    """
    request_data = await request.json()
    errors = CreateSchema.validate(request_data)
    if errors:
        return web.json_response(errors, status=400)

    new_employee = Employees(first_name=request_data['first_name'],
                             last_name=request_data['last_name'],
                             birth_date=datetime.strptime(request_data['birth_date'], "%Y-%m-%d"),
                             hire_date=datetime.strptime(request_data['hire_date'], "%Y-%m-%d"))
    sa_session = ahsa.get_session(request)
    async with sa_session.begin():
        sa_session.add(new_employee)
        await sa_session.flush()
    return web.json_response(new_employee.id, status=201)


@request_schema(UpdateSchema)
async def update_employee(request):
    """
    API endpoint bound to /employees/{id}/update that allows to update Employees object that is found by
    its integer id, works with PUT method
    """
    request_data = await request.json()
    errors = UpdateSchema.validate(request_data)
    if errors:
        return web.json_response(errors, status=400)
    sa_session = ahsa.get_session(request)
    async with sa_session.begin():
        try:
            employee = await sa_session.execute(
                sa.select(Employees).where(Employees.id == int(request.match_info['id'])))
            employee = employee.scalar_one()
        except NoResultFound:
            return web.json_response("not found")
        for key, value in request_data.items():
            try:
                if 'date' in key:
                    setattr(employee, key, datetime.strptime(value, '%Y-%m-%d'))
                else:
                    setattr(employee, key, value)
            except:
                continue
        await sa_session.flush()
    return web.json_response("ok")


async def delete_employee(request):
    """
    API endpoint bound to /employees/{id}/delete that allows to delete Employees object by
    its integer id, works with DELETE method
    """
    sa_session = ahsa.get_session(request)
    async with sa_session.begin():
        try:
            employee = await sa_session.execute(sa.select(Employees).where(Employees.id == int(request.match_info['id'])))
            employee = employee.scalar_one()
        except NoResultFound:
            return web.json_response("not found")
        await sa_session.delete(employee)
    return web.json_response("ok")


async def application():
    """
    All setup and routes is here
    """
    app = web.Application()

    ahsa.setup(app, [
        ahsa.bind(f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"),
    ])
    await ahsa.init_db(app, metadata)

    setup_aiohttp_apispec(
        app=app,
        title="API docs",
        version="v1",
        url="/docs/swagger.json",
        swagger_path="/docs",
    )

    app.add_routes([
        web.get('/employees/', list_employees),
        web.get(r'/employees/{id:\d+}', retrieve_employee),
        web.post('/employees/create', create_employee),
        web.put(r'/employees/{id:\d+}/update', update_employee),
        web.delete(r'/employees/{id:\d+}/delete', delete_employee)
        ])
    return app


'''
if __name__ == '__main__':
    app = app_factory()
    web.run_app(app)
'''