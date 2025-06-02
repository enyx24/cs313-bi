from connectDB import connect_mysql
import csv
import json
conn = connect_mysql()


############## seeding undependent tables ##############
# seeding user_info
def seed_user_info():
    with open('data/user-info.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cursor = conn.cursor()
        for row in reader:
            cursor.execute(
                "INSERT INTO user_info (uid, name, gender, school, yob) VALUES (%s, %s, %s, %s, %s)",
                (row['id'], row['name'], row['gender'], row['school'], row['year_of_birth'])
            )
        conn.commit()
        cursor.close()

# seeding course_resource
def seed_course_resource():
    with open('data/filtered_course_resource.json', encoding='utf-8') as f:
        cursor = conn.cursor()
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            course_id = data["course_id"]
            resource_ids = data["resource_ids"]
            for resource_id in resource_ids:
                cursor.execute(
                    "INSERT INTO course_resource (cid, rid) VALUES (%s, %s)",
                    (course_id, resource_id)
                )
        conn.commit()
        cursor.close()

# seeding exercise-problem
def seed_exercise_problem():
    with open('data/exercise-problem.txt', encoding='utf-8') as f:
        cursor = conn.cursor()
        for line in f:
            eid, pid = line.strip().split('\t')
            cursor.execute(
                "INSERT INTO exercise_problem (eid, pid) VALUES (%s, %s)",
                (eid, pid)
            )
        conn.commit()
        cursor.close()

############## seeding dependent tables ##############
# seeding user_comment
def seed_user_comment(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cursor = conn.cursor()
        for row in reader:
            cursor.execute(
                "INSERT INTO user_comment (uid, time) VALUES (%s, %s)",
                (row['user_id'], row['time'])
            )
        conn.commit()
        cursor.close()

# seeding user_course
def seed_user_course(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cursor = conn.cursor()
        for row in reader:
            cursor.execute(
                "INSERT INTO user_course (uid, cid, time) VALUES (%s, %s, %s)",
                (row['user_id'], row['course_id'], row['time'])
            )
        conn.commit()
        cursor.close()

# seeding user_problem
def seed_user_problem(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cursor = conn.cursor()
        for row in reader:
            cursor.execute(
                "INSERT INTO user_problem (uid, pid, time) VALUES (%s, %s, %s)",
                (row['user_id'], row['problem_id'], row['submit_time'])
            )
        conn.commit()
        cursor.close()

# seeding user_video
def seed_user_video(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        cursor = conn.cursor()
        for row in reader:
            cursor.execute(
                "INSERT INTO user_video (uid, vid, time) VALUES (%s, %s, %s)",
                (row['user_id'], row['video_id'], row['time'])
            )
        conn.commit()
        cursor.close()

# seed_course_resource()
# seed_user_info()
# seed_exercise_problem()

import os
data_dir = './data'
dependent_seeders = {
    'user-comment.csv': seed_user_comment,
    'user-course.csv': seed_user_course,
    'user-problem.csv': seed_user_problem,
    'user-video.csv': seed_user_video,
}

for subdir in os.listdir(data_dir):
    subdir_path = os.path.join(data_dir, subdir)
    print(f"Processing subdirectory: {subdir_path}")
    if os.path.isdir(subdir_path):
        for csv_name, seeder_func in dependent_seeders.items():
            csv_path = os.path.join(subdir_path, csv_name)
            print(f"Checking for {csv_name} in {subdir_path}")
            if os.path.isfile(csv_path):
                print(f"Seeding {csv_name} from {csv_path}")
                seeder_func(csv_path)

# Close the database connection
conn.close()