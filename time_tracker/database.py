import os

import asyncpg


class Database:
    '''
    .. warning::
        Public interface should use localized timestamps.
        Some database drivers return timestamps in UTC, even after
        changing connection timezone.
    '''

    CREATE_TASKS_QUERY = ('INSERT INTO task (name, "start", "end") '
                          'VALUES ($1, $2, $3)')

    def __init__(self, pool):
        self.__pool = pool

    async def __async_init(self):
        self.__connection = await self.__pool.acquire()
        return self

    def __await__(self):
        return self.__async_init().__await__()

    async def release(self):
        await self.__pool.release(self.__connection)

    async def create_tasks(self, tasks):
        await self.__connection.executemany(self.CREATE_TASKS_QUERY, tasks)

    @staticmethod
    async def create_pool(timezone):
        async def init_connection(connection):
            await connection.execute('SET timezone TO \'%s\'' % (timezone))
        return await asyncpg.create_pool(
            init=init_connection,
            min_size=int(os.environ.get('DB_POOL_MIN_SIZE', '1')),
            max_size=int(os.environ.get('DB_POOL_MAX_SIZE', '5')),
            user=os.environ['DB_USER'],
            database=os.environ['DB_NAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'])
