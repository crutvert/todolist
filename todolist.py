# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task + self.deadline


def print_menu():
    print()
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


def print_tasks(data, day=0):
    n = 1
    for row in data:
        if day == 0:
            print(f"{n}. {row.task}")
        else:
            print(f"{n}. {row.task}. {datetime.strftime(row.deadline, '%d %b')}")
        n += 1


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today()
while True:
    print_menu()
    choose = input()
    if choose == '1':
        # print today's tasks
        print(f"Today {datetime.strftime(today, '%d %b')}:")
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            print_tasks(rows)
    elif choose == '2':
        # Week's tasks
        for i in range(7):
            print(f"{datetime.strftime(today + timedelta(days=i), '%A %d %b')}:")
            rows = session.query(Table).filter(Table.deadline == today.date() + timedelta(days=i)).all()
            if len(rows) == 0:
                print("Nothing to do!")
            else:
                print_tasks(rows)
            print()
    elif choose == '3':
        # All tasks
        print("All tasks:")
        rows = session.query(Table).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            print_tasks(rows, day=1)
    elif choose == '4':
        # Missed tasks
        print("Missed tasks:")
        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        if len(rows) == 0:
            print("Nothing is missed!")
        else:
            print_tasks(rows, day=1)
    elif choose == '5':
        # add task
        print("Enter task")
        new_task = input()
        print("Enter deadline")
        new_deadline = input()
        new_row = Table(task=new_task, deadline=datetime.strptime(new_deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif choose == '6':
        # Delete task
        print("Chose the number of the task you want to delete:")
        rows = session.query(Table).all()
        if len(rows) == 0:
            print("Nothing to delete!")
        else:
            print_tasks(rows, day=1)
            delete_n = int(input())
            specific_row = rows[delete_n - 1]
            session.delete(specific_row)
            session.commit()
            print("The task has been deleted!")
    elif choose == '0':
        # Exit
        print()
        print("Bye!")
        break
