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
            '64ad817f-f3c6-4b09-a1b0-4bd569b15d03': self.model.STATUS.inactive, # revoked
            'd9e3e257-9eca-4cbf-959f-149cca968349': self.model.STATUS.inactive, # suspended
            '6e3c5cc6-0734-4edf-8f51-40d3a865a94f': self.model.STATUS.inactive, # merged
            'bd4721e7-addd-4854-9888-8a705725f748': self.model.STATUS.inactive, # closed
            'e04744e6-b743-4247-92c2-2950855b3a93': self.model.STATUS.inactive, # expired
            '55a97973-02c3-414a-bbef-22181ad46e85': self.model.STATUS.active, # pending
            'bb1ee6f6-a2c5-4615-b6ad-76130c37b1e6': self.model.STATUS.active, # pending voluntary
            'd7102af8-013a-40e7-bc85-0b00766ed124': self.model.STATUS.active, # awaiting
            'f3facc00-1990-4c68-9052-39e066906a38': self.model.STATUS.active, # prospective
            '4bfee76f-3110-4c32-bade-e5044fdd5fa2': self.model.STATUS.active, # licensed
            '7b9e5e34-a7c5-4f1e-9fc5-656caa74b3c7': self.model.STATUS.active, # active
        }
        status = status_map.get(status_id, None)

        # AIC
        aic_map = {
            "500983": "After Hours",
            "501972": "Main Street",
            "501329": "Forefront",
            "500922": "Instant Classic",
            "304772": "Musical Island Boys",
            "500000": "Masterpiece",
            "501150": "Ringmasters",
            "317293": "Old School",
            "286100": "Storm Front",
            "500035": "Crossroads",
            "297201": "OC Times",
            "299233": "Max Q",
            "302244": "Vocal Spectrum",
            "299608": "Realtime",
            "6158": "Gotcha!",
            "2496": "Power Play",
            "276016": "Four Voices",
            "5619": "Michigan Jake",
            "6738": "Platinum",
            "3525": "FRED",
            "5721": "Revival",
            "2079": "Yesteryear",
            "2163": "Nightlife",
            "4745": "Marquis",
            "3040": "Joker's Wild",
            "1259": "Gas House Gang",
            "2850": "Keepsake",
            "1623": "The Ritz",
            "3165": "Acoustix",
            "1686": "Second Edition",
            "492": "Chiefs of Staff",
            "1596": "Interstate Rivals",
            "1654": "Rural Route 4",
            "406": "The New Tradition",
            "1411": "Rapscallions",
            "1727": "Side Street Ramblers",
            "545": "Classic Collection",
            "490": "Chicago News",
            "329": "Boston Common",
            "4034": "Grandma's Boys",
            "318": "Bluegrass Student Union",
            "362": "Most Happy Fellows",
            "1590": "Innsiders",
            "1440": "Happiness Emporium",
            "1427": "Regents",
            "627": "Dealer's Choice",
            "1288": "Golden Staters",
            "1275": "Gentlemen's Agreement",
            "709": "Oriole Four",
            "711": "Mark IV",
            "2047": "Western Continentals",
            "1110": "Four Statesmen",
            "713": "Auto Towners",
            "715": "Four Renegades",
            "1729": "Sidewinders",
            "718": "Town and Country 4",
            "719": "Gala Lads",
            "1871": "The Suntones",
            "722": "Evans Quartet",
            "724": "Four Pitchikers",
            "726": "Gaynotes",
            "729": "Lads of Enchantment",
            "731": "Confederates",
            "732": "Four Hearsemen",
            "736": "The Orphans",
            "739": "Vikings",
            "743": "Four Teens",
            "746": "Schmitt Brothers",
            "748": "Buffalo Bills",
            "750": "Mid-States Four",
            "753": "Pittsburghers",
            "756": "Doctors of Harmony",
            "759": "Garden State Quartet",
            "761": "Misfits",
            "764": "Harmony Halls",
            "766": "Four Harmonizers",
            "770": "Elastic Four",
            "773": "Chord Busters",
            "775": "Flat Foot Four",
            "776": "Bartlsesville Barflies",
        }

        # Overwrite status for AIC
        if bhs_id in aic_map:
            status = -5

        # Construct the group name
        if kind == self.model.KIND.quartet:
            # If the name has not been assigned, use preferred. Otherwise, call unknown.
            if not name:
                name = preferred_name if preferred_name else 'UNKNOWN'
        else:
            name = name if name else 'UNKNOWN'

        # Overwrite name for AIC
        name = aic_map.get(bhs_id, name)

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


class MemberManager(Manager):
    def update_or_create_from_join(self, join):
        # Extract
        start_date = join['startest_date']
        end_date = join['endest_date']
        vocal_part = join['vocal_part']
        group_id = join['structure__id']
        person_id = join['subscription__human__id']
        status = join['status']

        # Transform
        part = getattr(
            self.model.PART,
            vocal_part.strip().lower() if vocal_part else '',
            None,
        )

        # Build dictionary
        defaults = {
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
            'part': part,
        }

        # Load
        member, created = self.update_or_create(
            person_id=person_id,
            group_id=group_id,
            defaults=defaults,
        )
        return member, created


class OfficerManager(Manager):
    def update_or_create_from_role(self, role):
        # Extract
        name = role['name']
        start_date = role['startest_date']
        end_date = role['endest_date']
        person_id = role['human_id']
        group_id = role['structure_id']
        status = role['status']

        # Transform
        name_map = {
            'Chapter President': 310,
            'Chapter Secretary': 320,
            'Chorus Director': 320,
            'Chorus Associate or Assistant Director': 340,
            'Chorus Manager': 350,
            'Quartet Admin': 410,
        }

        office = name_map.get(name, None)

        defaults = {
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        }

        # Load
        officer, created = self.update_or_create(
            office=office,
            person_id=person_id,
            group_id=group_id,
            defaults=defaults,
        )
        return officer, created
