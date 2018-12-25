import os

import asyncpg


class Connection:

    INSERT_TASK_QUERY = '''
INSERT INTO task (name, "start", "end") VALUES ($1, $2, $3)
'''
    INSERT_TASK_TAG_NEW_QUERY = '''
INSERT INTO task_tag (tag_id, task_id)
VALUES (currval(\'tag_id_seq\'), currval(\'task_id_seq\'))
'''
    INSERT_TASK_TAG_QUERY = '''
INSERT INTO task_tag (tag_id, task_id)
VALUES ($1, currval(\'task_id_seq\'))
'''
    INSERT_TAG_QUERY = 'INSERT INTO tag (name) VALUES ($1)'
    SELECT_TAG_QUERY = 'SELECT id FROM tag WHERE name = $1'
    SELECT_TAG_REPORT_QUERY = '''
SELECT tag.name, sum(task.end - task.start) AS time
FROM task, tag, task_tag
WHERE task.id = task_tag.task_id
    AND task_tag.tag_id = tag.id
    AND task.start >= $1
    AND task.start < $2
GROUP BY tag.id;
'''

    def __init__(self, pool):
        self._pool = pool

    async def _async_init(self):
        self._connection = await self._pool.acquire()
        return self

    def __await__(self):
        return self._async_init().__await__()

    async def release(self):
        await self._pool.release(self._connection)

    async def create_task_tags(self, tags):
        for tag in tags:
            row = await self._connection.fetchrow(self.SELECT_TAG_QUERY, tag)
            if not row:
                await self._connection.execute(self.INSERT_TAG_QUERY, tag)
                await self._connection.execute(self.INSERT_TASK_TAG_NEW_QUERY)
            else:
                await self._connection.execute(
                    self.INSERT_TASK_TAG_QUERY, row['id'])

    async def create_tasks(self, tasks):
        async with self._connection.transaction():
            for task in tasks:
                await self._connection.execute(
                    self.INSERT_TASK_QUERY,
                    task[0], task[2], task[3])
                await self.create_task_tags(task[1])

    async def get_tag_report(self, start, end):
        return list(map(
            lambda tag: (tag['name'], tag['time']),
            await self._connection.fetch(
                self.SELECT_TAG_REPORT_QUERY, start, end)))

    @staticmethod
    async def create_pool():
        return await asyncpg.create_pool(
            min_size=int(os.environ.get('DB_POOL_MIN_SIZE', '1')),
            max_size=int(os.environ.get('DB_POOL_MAX_SIZE', '5')),
            user=os.environ['DB_USER'],
            database=os.environ['DB_NAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=os.environ['DB_PORT'])
