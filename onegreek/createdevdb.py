import sys, os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.contrib.auth.models import User
from events.models import Event
from chapters.models import Chapter
from universities.models import University
from fraternities.models import Fraternity



TEXT_BLOCK = open('lipsum.txt', 'r').read()


def create_user(i):
    return User.objects.create(
	username='testuser%d' % i, 
	password='default', 
	first_name='First%d' % i,
	last_name='First%d' % i, 
	phone=5555555555,
	email='examle%d@example.com' % i
)


def create_project(i, user_id):
    user = User.objects.get(id=user_id)
    return Project.objects.create(title="Test Project %d" % i, user=user, description=TEXT_BLOCK[:200])


def create_cat(i, parent=None):
    return TaskCategory.objects.create(title="Test Category %d" % i, description=TEXT_BLOCK[:90], parent=parent)


def create_task(i, cat_id, project_id):
    cat = TaskCategory.objects.get(id=cat_id)
    project = Project.objects.get(id=project_id)
    return Task.objects.create(title="Test Task %d" % i, category=cat, project=project, expense=i * 1000,
                               price=i * 500, description=TEXT_BLOCK[:100])

def create_change_order(i, project_id, *args):
    project = Project.objects.get(id=project_id)
    co = ChangeOrder.objects.create(title="Test Change Order %d" % i, description=TEXT_BLOCK[:200], project=project, approved=2)
    for arg in args:
        co.tasks.add(arg)
    co.save()

def create_update(i, project_id, *args):
    project = Project.objects.get(id=project_id)
    update = Update.objects.create(title="Test Update %d" % i, description=TEXT_BLOCK[:200], project=project)
    for arg in args:
        update.tasks.add(arg)
    update.save()


def main():
    u_count = int(sys.argv[1])
    p_count = int(sys.argv[2])
    c_count = int(sys.argv[3])
    t_count = int(sys.argv[4])

    cats_count = int(TaskCategory.objects.count())
    i = 0
    cat_parent = None
    for ic in range(0, c_count):
        new_cat = create_cat(cats_count + ic, cat_parent)
        if i == 2:
            cat_parent = new_cat
        elif i == 4:
            cat_parent = new_cat
        elif i == 7:
            cat_parent = new_cat
        elif i == 8:
            cat_parent = new_cat.parent.parent.parent
        elif i == 10:
            cat_parent = new_cat
        elif i == 12:
            cat_parent = new_cat
        elif i == 15:
            cat_parent = new_cat.parent.parent
        elif i == 17:
            cat_parent = new_cat
        elif i == 20:
            cat_parent = None
        elif i == 22:
            cat_parent = new_cat
        elif i == 25:
            cat_parent = new_cat.parent.parent
        elif i == 27:
            cat_parent = new_cat
        elif i == 30:
            cat_parent = None
        i += 1


    all_cats = TaskCategory.objects.all()

    users_count = int(User.objects.count())
    for iu in range(0, u_count):
        new_user = create_user(users_count + iu)
        projects_count = int(Project.objects.count())
        for ip in range(0, p_count):
            new_project = create_project(projects_count + ip, user_id=new_user.id)
            for cat in all_cats:
                tasks_count = int(Task.objects.count())
                for it in range(0, t_count):
                    create_task(tasks_count + it, cat.id, project_id=new_project.id)
            project_tasks = new_project.task_set.all()
            changes_count = int(ChangeOrder.objects.count())
            updates_count = int(Update.objects.count())
            for iup in range(0, project_tasks.count() - 2, 3):
                create_update(updates_count+(iup/3), new_project.id,
                              int(project_tasks[iup].id), int(project_tasks[iup + 1].id), int(project_tasks[iup + 2].id))
            for ico in range(0, project_tasks.count() - 2, 3):
                create_change_order(changes_count+(ico/3), new_project.id,
                              int(project_tasks[ico].id), int(project_tasks[ico + 1].id), int(project_tasks[ico + 2].id))



if __name__ == '__main__':
    main()
