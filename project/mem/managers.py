# Django
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from phonenumber_field.validators import validate_international_phonenumber
from django.db.models import Manager
from .validators import validate_bhs_id
from .validators import validate_tin
from .validators import validate_url

class PersonManager(Manager):
    def update_or_create_from_human(self, human):
        # Extract
        pk = human['id']
        first_name = human['first_name']
        middle_name = human['middle_name']
        last_name = human['last_name']
        nick_name = human['nick_name']
        email = human['email']
        birth_date = human['birth_date']
        is_deceased = human['is_deceased']
        home_phone = human['phone']
        cell_phone = human['cell_phone']
        work_phone = human['work_phone']
        bhs_id = human['bhs_id']
        gender = human['sex']
        part = human['primary_voice_part']
        mon = human['mon']

        # Transform
        first_name = first_name.replace(".", "").replace(",", "").strip()

        try:
            middle_name = middle_name.replace(".", "").replace(",", "").strip()
        except AttributeError:
            middle_name = ""
        last_name = last_name.replace(".", "").replace(",", "").strip()
        try:
            nick_name = nick_name.replace("'", "").replace('"', '').replace("(", "").replace(")", "").strip()
        except AttributeError:
            nick_name = ""
        if nick_name == first_name:
            nick_name = ""
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

        # Load
        person, created = self.update_or_create(
            id=pk,
            defaults=defaults,
        )
        return person, created


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure):
        # Extract
        pk = structure['id']
        name = structure['name']
        kind = structure['kind']
        gender = structure['gender']
        division = structure['division']
        bhs_id = structure['bhs_id']
        legacy_code = structure['chapter_code']
        website = structure['website']
        email = structure['email']
        main_phone = structure['phone']
        fax_phone = structure['fax']
        facebook = structure['facebook']
        twitter = structure['twitter']
        youtube = structure['youtube']
        pinterest = structure['pinterest']
        flickr = structure['flickr']
        instagram = structure['instagram']
        soundcloud = structure['soundcloud']
        tin = structure['tin']
        preferred_name = structure['preferred_name']
        first_alternate_name = structure['first_alternate_name']
        second_alternate_name = structure['second_alternate_name']
        # description = structure['description']
        visitor_information = structure['visitor_information']
        established_date = structure['established_date']
        chartered_date = structure['chartered_date']
        licensed_date = structure['licenced_date']
        deleted_date = structure['deleted']
        status_id = structure['status_id']
        parent_pk = structure['parent_id']

        # Transform
        status_map = {
            '64ad817f-f3c6-4b09-a1b0-4bd569b15d03': self.model.STATUS.revoked,
            'd9e3e257-9eca-4cbf-959f-149cca968349': self.model.STATUS.suspended,
            '6e3c5cc6-0734-4edf-8f51-40d3a865a94f': self.model.STATUS.merged,
            'bd4721e7-addd-4854-9888-8a705725f748': self.model.STATUS.closed,
            'e04744e6-b743-4247-92c2-2950855b3a93': self.model.STATUS.expired,
            '55a97973-02c3-414a-bbef-22181ad46e85': self.model.STATUS.pending,
            'bb1ee6f6-a2c5-4615-b6ad-76130c37b1e6': self.model.STATUS.penvol,
            'd7102af8-013a-40e7-bc85-0b00766ed124': self.model.STATUS.awaiting,
            'f3facc00-1990-4c68-9052-39e066906a38': self.model.STATUS.prospective,
            '4bfee76f-3110-4c32-bade-e5044fdd5fa2': self.model.STATUS.licensed,
            '7b9e5e34-a7c5-4f1e-9fc5-656caa74b3c7': self.model.STATUS.active,
        }
        status = status_map.get(status_id, None)

        # Construct the group name
        if kind == self.model.KIND.quartet:
            # If the name has not been assigned, use preferred. Otherwise, call unknown.
            if not name:
                name = preferred_name if preferred_name else 'UNKNOWN'
        else:
            name = name if name else 'UNKNOWN'

        # Re-construct dangling article
        if name.endswith(", The"):
            parsed = name.partition(", The")
            name = "The {0}".format(parsed[0])

        name = name.strip() if name else '{0} (NAME APPROVAL PENDING)'.format(preferred_name.strip() if preferred_name else '')

        kind_map = {
            'quartet': self.model.KIND.quartet,
            'chorus': self.model.KIND.chorus,
            'chapter': self.model.KIND.chapter,
            'group': self.model.KIND.group,
            'district': self.model.KIND.district,
            'organization': self.model.KIND.organization,
        }
        kind = kind_map.get(kind, None)

        gender_map = {
            'men': self.model.GENDER.male,
            'women': self.model.GENDER.female,
            'mixed': self.model.GENDER.mixed,
        }
        gender = gender_map.get(gender, None)

        division_map = {
            'EVG Division I': self.model.DIVISION.evgd1,
            'EVG Division II': self.model.DIVISION.evgd2,
            'EVG Division III': self.model.DIVISION.evgd3,
            'EVG Division IV': self.model.DIVISION.evgd4,
            'EVG Division V': self.model.DIVISION.evgd5,
            'FWD Arizona': self.model.DIVISION.fwdaz,
            'FWD Northeast': self.model.DIVISION.fwdne,
            'FWD Northwest': self.model.DIVISION.fwdnw,
            'FWD Southeast': self.model.DIVISION.fwdse,
            'FWD Southwest': self.model.DIVISION.fwdsw,
            'LOL 10000 Lakes': self.model.DIVISION.lol10l,
            'LOL Division One': self.model.DIVISION.lolone,
            'LOL Northern Plains': self.model.DIVISION.lolnp,
            'LOL Packerland': self.model.DIVISION.lolpkr,
            'LOL Southwest': self.model.DIVISION.lolsw,
            'MAD Central': self.model.DIVISION.madcen,
            'MAD Northern': self.model.DIVISION.madnth,
            'MAD Southern': self.model.DIVISION.madsth,
            'NED Granite and Pine': self.model.DIVISION.nedgp,
            'NED Mountain': self.model.DIVISION.nedmtn,
            'NED Patriot': self.model.DIVISION.nedpat,
            'NED Sunrise': self.model.DIVISION.nedsun,
            'NED Yankee': self.model.DIVISION.nedyke,
            'SWD Northeast': self.model.DIVISION.swdne,
            'SWD Northwest': self.model.DIVISION.swdnw,
            'SWD Southeast': self.model.DIVISION.swdse,
            'SWD Southwest': self.model.DIVISION.swdsw,
        }
        division = division_map.get(division, None)

        if bhs_id:
            try:
                validate_bhs_id(bhs_id)
            except ValidationError:
                bhs_id = None
        else:
            bhs_id = None

        legacy_code = legacy_code.strip() if legacy_code else ''

        if main_phone:
            try:
                validate_international_phonenumber(main_phone.strip())
            except ValidationError:
                main_phone = ""
        else:
            main_phone = ""
        if fax_phone:
            try:
                validate_international_phonenumber(fax_phone.strip())
            except ValidationError:
                fax_phone = ""
        else:
            fax_phone = ""

        try:
            validate_url(website)
        except ValidationError:
            website = ""

        if email:
            email = email.strip().lower()
            try:
                validate_email(email)
            except ValidationError:
                email = None
        else:
            email = None

        try:
            validate_url(facebook)
        except ValidationError:
            facebook = ""

        try:
            validate_url(twitter)
        except ValidationError:
            twitter = ""

        try:
            validate_url(youtube)
        except ValidationError:
            youtube = ""
        try:
            validate_url(pinterest)
        except ValidationError:
            pinterest = ""

        try:
            validate_url(flickr)
        except ValidationError:
            flickr = ""

        try:
            validate_url(instagram)
        except ValidationError:
            instagram = ""

        try:
            validate_url(soundcloud)
        except ValidationError:
            soundcloud = ""

        try:
            validate_tin(tin)
        except ValidationError:
            tin = ''

        preferred_name = preferred_name.strip() if preferred_name else ''
        first_alternate_name = first_alternate_name.strip() if first_alternate_name else ''
        second_alternate_name = second_alternate_name.strip() if second_alternate_name else ''
        visitor_information = visitor_information.strip() if visitor_information else ''

        defaults = {
            'status': status,
            'name': name,
            'kind': kind,
            'gender': gender,
            'division': division,
            'bhs_id': bhs_id,
            'legacy_code': legacy_code,
            'website': website,
            'email': email,
            'main_phone': main_phone,
            'fax_phone': fax_phone,
            'facebook': facebook,
            'twitter': twitter,
            'youtube': youtube,
            'pinterest': pinterest,
            'flickr': flickr,
            'instagram': instagram,
            'soundcloud': soundcloud,
            'tin': tin,
            'preferred_name': preferred_name,
            'first_alternate_name': first_alternate_name,
            'second_alternate_name': second_alternate_name,
            'visitor_information': visitor_information,
            'established_date': established_date,
            'chartered_date': chartered_date,
            'licensed_date': licensed_date,
            'deleted_date': deleted_date,
            'parent_id': parent_pk,
        }

        # Load
        group, created = self.update_or_create(
            id=pk,
            defaults=defaults,
        )
        return group, created

class StreamManager(Manager):
    def update_or_create_from_join(self, join):
        # Extract
        pk = join['id']
        paid = join['paid']
        established_date = join['established_date']
        inactive_date = join['inactive_date']
        vocal_part = join['vocal_part']
        is_current = join['status']
        inactive_reason = join['inactive_reason']
        structure_id = join['structure__id']
        human_id = join['subscription__human__id']
        current_through = join['subscription__current_through']
        sub_status = join['subscription__status']
        mem_code = join['membership__code']
        join_created = join['created']
        join_modified = join['modified']
        join_deleted = join['deleted']
        mem_created = join['membership__created']
        mem_modified = join['membership__modified']
        mem_deleted = join['membership__deleted']
        sub_created = join['subscription__created']
        sub_modified = join['subscription__modified']
        sub_deleted = join['subscription__deleted']

        # Transform
        part = getattr(
            self.model.PART,
            vocal_part.strip().lower() if vocal_part else '',
            None,
        )
        code = getattr(
            self.model.CODE,
            mem_code,
            None,
        )
        status = getattr(
            self.model.STATUS,
            sub_status.replace('lapsedRenew', 'lapsed') if sub_status else '',
            None,
        )
        inactive_map = {
            'Non-renewal': 10,
            'Renewed': 20,
            'Not Cancelled': 30,
            'Non-Payment': 40,
            'changedOption': 70,
            'cancelled': 90,
            'Transferred': 100,
            'Expired': 50,
            'Deceased': 60,
            'Other': 80,
            'swappedChapter': 110,
            'swapped': 120,
        }
        inactive = inactive_map.get(inactive_reason, None)

        # Build dictionary
        defaults = {
            'is_paid': paid,
            'established_date': established_date,
            'inactive_date': inactive_date,
            'part': part,
            'is_current': is_current,
            'inactive': inactive,
            'group_id': structure_id,
            'person_id': human_id,
            'current_through': current_through,
            'status': status,
            'code': code,
            'join_created': join_created,
            'join_modified': join_modified,
            'join_deleted': join_deleted,
            'mem_created': mem_created,
            'mem_modified': mem_modified,
            'mem_deleted': mem_deleted,
            'sub_created': sub_created,
            'sub_modified': sub_modified,
            'sub_deleted': sub_deleted,
        }

        # Load
        stream, created = self.update_or_create(
            id=pk,
            defaults=defaults,
        )
        return stream, created
