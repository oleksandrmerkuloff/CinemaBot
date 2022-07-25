import psycopg
from botConfiguration import bot
from handlers.keyboards.clientKB import createKb
from smtp_sender import send_email

async def sql_start_work():
    async with await psycopg.AsyncConnection.connect("dbname=botname user=postgres password=pass") as connect:
    
        async with connect.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS going_films(
                    poster_img text,
                    film_title varchar(50) not null PRIMARY KEY,
                    genre varchar(50) not null,
                    age_limit varchar not null,
                    description text not null,
                    film_url text
                )
                """
            )
            await connect.commit()
        async with connect.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS resume_forms(
                    full_name text,
                    document text
                )
                """
                 )
            await connect.commit()
async def add_new_resume_forms(state):
    
    async with await psycopg.AsyncConnection.connect("dbname=botname user=postgres password=pass") as d_base:

        async with d_base.cursor() as cur:

            async with state.proxy() as data:
                
                await cur.execute(
                    "INSERT INTO resume_forms VALUES (%s, %s)",
                    tuple(data.values()))
                
                await d_base.commit()

async def add_new_film_in_table(state):                
    async with await psycopg.AsyncConnection.connect("dbname=botname user=postgres password=pass") as d_base:
        async with d_base.cursor as cur:
            async with state.proxy() as data:
                
                await cur.execute(
                    "INSERT INTO going_films VALUES (%s, %s, %s, %s, %s, %s)",
                    tuple(data.values()))
                
                await d_base.commit()


async def sql_films_read(message):
    async with await psycopg.AsyncConnection.connect("dbname=botname user=postgres password=pass") as d_base:
        async with d_base.cursor() as cur:
            await cur.execute('SELECT * FROM going_films')
            #await cur.fetchall() смысла его испльзовать не было, так как fetchall возвращает список значений
            async for film in cur:
                unique_kb = createKb(film[5])
                await bot.send_photo(message.from_user.id, film[0], f"Назва фільму: {film[1]}\nЖанр: {film[2]}\nВікове обмеження: {film[3]}\nКороткий опис: {film[4]}\n", reply_markup=unique_kb) 
                
async def sql_resume_read(message):
    async with await psycopg.AsyncConnection.connect("dbname=botname user=postgres password=pass") as d_base:
        async with d_base.cursor() as cur:
            await cur.execute('SELECT * FROM resume_forms')
            async for resume in cur:
                await bot.send_document(message.from_user.id, document=resume[1], caption=f'{resume[0]}') 
                
                