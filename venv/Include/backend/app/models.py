from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    """
    Модель пользователя
    """

    id = fields.IntField(pk=True)
    #: Id телеграм-аккаунта
    telegram_id = fields.IntField(unique=True)
    #: Имя
    first_name = fields.CharField(max_length=50, null=True)
    #: Фамилия
    last_name = fields.CharField(max_length=50, null=True)
    #: Роль
    role = fields.CharField(max_length=60)
    #: Город
    city = fields.CharField(max_length=20)
    #: Дата вступления
    startdate = fields.DateField(blank=False)
    #: Электронная почта
    email = fields.CharField(max_length=60)
    #: Ссылка на фейсбук
    fb = fields.CharField(max_length=60)
    #: Ссылка на вконтакте
    vk = fields.CharField(max_length=60)
    #: Номер телефона
    telnum = fields.CharField(max_length=60)
    #: День рождения
    birthday = fields.DateField(blank=False)
    #: Группа
    group = fields.CharField(max_length=60)
    #: Секрет-строка
    token = fields.CharField(max_length=20)
    #: Тип прав
    roots = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    #def full_name(self) -> str:
    #    """
    #    Returns the best name
    #    """
    #    if self.first_name or self.last_name:
    #        return f"{self.first_name or ''} {self.last_name or ''}".strip()
    #    return self.telegramid

    #class PydanticMeta:
    #    computed = ["full_name"]


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

class Groups(models.Model):
    """
    Модель группы участников
    """

    id = fields.IntField(pk=True)
    #: ID группы
    group_id = fields.CharField(max_length=50)
    #: Название группы
    group = fields.CharField(max_length=50)
    #: Фонд
    fond = fields.CharField(max_length=100)
    #: Город
    city = fields.CharField(max_length=25)
    #: Год
    year = fields.TextField()

Group_Pydantic = pydantic_model_creator(Groups, name="Group")
GroupIn_Pydantic = pydantic_model_creator(Groups, name="GroupIn", exclude_readonly=True)

class Hobbies(models.Model):
    """
    Модель интереса
    """

    id = fields.IntField(pk=True)
    #: Хэштег
    hashtag = fields.CharField(max_length=50)
    #: Id пользователя (telegram)
    telegram_id = fields.IntField()

Hobby_Pydantic = pydantic_model_creator(Hobbies, name="Hobby")
HobbyIn_Pydantic = pydantic_model_creator(Hobbies, name="HobbyIn", exclude_readonly=True)

class Competences(models.Model):
    """
    Модель компетенции
    """

    id = fields.IntField(pk=True)
    #: Хэштег
    hashtag = fields.CharField(max_length=50)
    #: Id пользователя (telegram)
    telegram_id = fields.IntField()

Competence_Pydantic = pydantic_model_creator(Competences, name="Competence")
CompetenceIn_Pydantic = pydantic_model_creator(Competences, name="CompetenceIn", exclude_readonly=True)

class Projects(models.Model):
    """
    Модель проекта
    """

    id = fields.IntField(pk=True)
    #: Название проекта
    name = fields.CharField(max_length=50)
    #: Описание проекта
    description = fields.TextField()
    #: Статус проекта (0 - продолжается, 1 - закончен)
    status = fields.IntField()
    #: Дата начала проекта
    startdate = fields.DateField()
    #: Дата окончания проекта
    enddate = fields.DateField()
    #: Инвестиционный статус проекта (0 - не получены, 1 - получены)
    is_investment_status_accept = fields.IntField()
    #: Инвестор проекта (если есть)
    investor = fields.CharField(max_length=50)
    #: Нужен ли проекту инвестор (0 - не нужен, 1 - нужен)
    is_invest_need = fields.IntField()
    #: Сумма требуемых инвестиций (если требуются)
    investneedsum = fields.IntField()
    #: Id пользователя (telegram)
    telegram_id = fields.IntField()

Project_Pydantic = pydantic_model_creator(Projects, name="Project")
ProjectIn_Pydantic = pydantic_model_creator(Projects, name="ProjectIn", exclude_readonly=True)

class Works(models.Model):
    """
    Модель работы
    """

    id = fields.IntField(pk=True)
    #: Название организации
    name = fields.CharField(max_length=70)
    #: Должность
    position = fields.CharField(max_length=50)
    #: Статус работы (0 - актуально, 1 - закончил)
    status = fields.IntField()
    #: Дата начала работы
    startdate = fields.DateField()
    #: Дата окончания работы (если закончил)
    enddate = fields.DateField()
    #: Id пользователя (telegram)
    telegram_id = fields.IntField()

Work_Pydantic = pydantic_model_creator(Works, name="Work")
WorkIn_Pydantic = pydantic_model_creator(Works, name="WorkIn", exclude_readonly=True)

class Studies(models.Model):
    """
    Модель учёбы
    """

    id = fields.IntField(pk=True)
    #: Тип (ВУЗ/Школа)
    type = fields.CharField(max_length=50)
    #: Наименование образовательной организации
    name = fields.CharField(max_length=100)
    #: Статус учёбы (0 - актуально, 1 - закончил)
    status = fields.IntField()
    #: Класс/курс
    step = fields.IntField()
    #: Если ВУЗ - тип (Бакалавриат, магистратура, кадидат, доктор)
    type = fields.CharField(max_length=100)
    #: Если ВУЗ - специальность
    speciality = fields.CharField(max_length=100)
    #: Id пользователя (telegram)
    telegram_id = fields.IntField()

Study_Pydantic = pydantic_model_creator(Studies, name="Study")
StudyIn_Pydantic = pydantic_model_creator(Studies, name="StudyIn", exclude_readonly=True)


class Events(models.Model):
    """
    Модель мероприятия
    """

    id = fields.IntField(pk=True)
    #: Название мероприятия
    name = fields.CharField(max_length=100)
    #: Описание мероприятия
    description = fields.TextField()
    #: Информация о формате и месте проведения мероприятия
    event_format = fields.CharField(max_length=160)
    #: Дата начала мероприятия
    startdate = fields.DatetimeField()
    #: Дата окончания мероприятия
    enddate = fields.DatetimeField()
    #: Образовательная траектория (например, school-moscow-2019 или school-peterburg)
    trajectory = fields.CharField(max_length=100)

Event_Pydantic = pydantic_model_creator(Events, name="Event")
EventIn_Pydantic = pydantic_model_creator(Events, name="EventIn", exclude_readonly=True)

class EventResponses(models.Model):
    """
    Модель мероприятия
    """

    id = fields.IntField(pk=True)
    #: Ответ
    rsns = fields.CharField(max_length=100)
    #: Событие (например, event-2 или message-12)
    event = fields.CharField(max_length=100)
    #: Автор (telegram id)
    telegram_id = fields.IntField()
    #: Дата ответа
    created_at = fields.DatetimeField(auto_now_add=True)

EventResponse_Pydantic = pydantic_model_creator(EventResponses, name="EventResponse")
EventResponseIn_Pydantic = pydantic_model_creator(EventResponses, name="EventResponseIn", exclude_readonly=True)