import sqlite3

class Database:
    def __init__(self,db_name = "fitness.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            create table if not exists users(
                id integer primary key autoincrement,
                name text unique,
                workout_days text,
                workout_time text,
                daily_streak integer,
                weekly_streak integer,
                last_workout_date text
            )
        """)
        self.cursor.execute("""
            create table if not exists workouts(
                id integer primary key autoincrement,
                user_id integer,
                date text,
                workout_name text,
                reps_duration text,
                foreign key (user_id) references users (id)            
            )
        """)
        self.conn.commit()

    def add_user(self,name,workout_days,workout_time):
        sql = """
            insert into users(name,workout_days,workout_time,daily_streak,weekly_streak)
            values(?,?,?,?,?)
        """    
        self.cursor.execute(sql,(name,workout_days,workout_time,0,0))
        self.conn.commit()

    def get_user(self,name):
        sql = """
            select * from users where name = ?
        """    
        self.cursor.execute(sql,(name,))
        return self.cursor.fetchone()
    
    def log_workout(self,user_id,date,workout_name,reps_duration):
        sql = """
            insert into workouts(user_id,date,workout_name,reps_duration)
            values (?,?,?,?)
        """
        self.cursor.execute(sql,(user_id,date,workout_name,reps_duration))
        self.conn.commit()
    
    def update_user_stats(self,user_id,daily_streak,weekly_streak,last_workout_date):
        sql = """
            update users
            set daily_streak = ?,weekly_streak =?,last_workout_date = ?
            where id = ?
        """
        self.cursor.execute(sql, (daily_streak, weekly_streak, last_workout_date, user_id))
        self.conn.commit()

    def get_user_workouts(self,user_id):
        sql = """
        select date,workout_name,reps_duration
        from workouts
        where user_id = ?
        """
        self.cursor.execute(sql,(user_id,))
        return self.cursor.fetchall()
