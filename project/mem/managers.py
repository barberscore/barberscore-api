# Django
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from phonenumber_field.validators import validate_international_phonenumber
from django.db.models import Manager


class PersonManager(Manager):
    def update_or_create_from_human(self, human):
        # Extract
        pk = human.id
        first_name = human.first_name
        middle_name = human.middle_name
        last_name = human.last_name
        nick_name = human.nick_name
        email = human.email
        birth_date = human.birth_date
        home_phone = human.phone
        cell_phone = human.cell_phone
        work_phone = human.work_phone
        bhs_id = human.bhs_id
        gender = human.sex
        part = human.primary_voice_part
        is_deceased = human.is_deceased
        mon = human.mon

        # Transform
        first_name = first_name.strip()
        try:
            middle_name = middle_name.strip()
        except AttributeError:
            middle_name = None
        last_name = last_name.strip()
        try:
            nick_name = nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        except AttributeError:
            nick_name = None
        if nick_name == first_name:
            nick_name = None
        if email:
            email = email.strip().lower()
            try:
                validate_email(email)
            except ValidationError:
                email = None
        else:
            email = None
        if home_phone:
            try:
                validate_international_phonenumber(home_phone)
            except ValidationError:
                home_phone = ""
        else:
            home_phone = ""
        if cell_phone:
            try:
                validate_international_phonenumber(cell_phone)
            except ValidationError:
                cell_phone = ""
        else:
            cell_phone = ""
        if work_phone:
            try:
                validate_international_phonenumber(work_phone)
            except ValidationError:
                work_phone = ""
        else:
            work_phone = ""
        if gender:
            gender = getattr(self.model.GENDER, gender.casefold(), None)
        else:
            gender = None
        if part:
            part = getattr(self.model.PART, part.casefold(), None)
        else:
            part = None

        is_deceased = bool(is_deceased)

        defaults = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'nick_name': nick_name,
            'email': email,
            'birth_date': birth_date,
            'home_phone': home_phone,
            'cell_phone': cell_phone,
            'work_phone': work_phone,
            'bhs_id': bhs_id,
            'gender': gender,
            'part': part,
            'is_deceased': is_deceased,
            'mon': mon,
        }

        # Update or create
        person, created = self.update_or_create(
            id=pk,
            defaults=defaults,
        )
        return person, created
