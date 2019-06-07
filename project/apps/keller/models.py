import uuid

from model_utils import Choices

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.apps import apps

from .managers import RawSongManager
from .managers import RawPanelistManager
from .managers import CleanPanelistManager
from .managers import CleanSongManager
from .managers import CleanFlatManager
from .managers import CompleteManager
from .managers import SelectionManager


class CleanPanelist(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )
    year = models.IntegerField(
    )
    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )
    season = models.IntegerField(
        choices=SEASON,
    )
    district = models.CharField(
        max_length=255,
    )
    convention = models.CharField(
        max_length=255,
    )
    SESSION = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )
    session = models.IntegerField(
        choices=SESSION,
    )
    ROUND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )
    round = models.IntegerField(
        choices=ROUND,
    )
    CATEGORY = Choices(
        (30, 'mus', 'Music'),
        (40, 'per', 'Performance'),
        (50, 'sng', 'Singing'),
    )
    category = models.IntegerField(
        choices=CATEGORY,
    )
    num = models.IntegerField(
    )
    legacy_person = models.CharField(
        max_length=255,
    )
    scores = JSONField(
    )
    panelist = models.OneToOneField(
        'api.panelist',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    objects = CleanPanelistManager()

    def get_convention(self):
        Convention = apps.get_model('cmanager.convention')
        year = self.year
        name = self.convention

        district_map = {
            'Cardinal District': 'CAR',
            'Carolinas District': 'NSC',
            'Central States District': 'CSD',
            'Dixie District': 'DIX',
            'EVG': 'EVG',
            'EVG Division': 'EVG',
            'EVG Prelims': 'EVG',
            'Evergreen District': 'EVG',
            'FWD': 'FWD',
            'FWD Division': 'FWD',
            'FWD Prelims': 'FWD',
            'Far Western District': 'FWD',
            'Illinois District': 'ILL',
            'International': 'BHS',
            'JAD': 'JAD',
            'JAD Prelims': 'JAD',
            'Johnny Appleseed District': 'JAD',
            'LOL': 'LOL',
            'LOL Division': 'LOL',
            'LOL Prelims': 'LOL',
            'Land O\' Lakes District': 'LOL',
            'MAD': 'MAD',
            'MAD Division': 'MAD',
            'MAD Prelims': 'MAD',
            'Mid-Atlantic District': 'MAD',
            'NED': 'NED',
            'NED Division': 'NED',
            'NED Patriot': 'NED',
            'NED Prelims': 'NED',
            'Northeastern District': 'NED',
            'Ontario District': 'ONT',
            'Pioneer District': 'PIO',
            'RMD/FWD': 'RMD',
            'Rocky Mountain District': 'RMD',
            'SWD': 'SWD',
            'SWD Division': 'SWD',
            'SWD Prelims': 'SWD',
            'Seneca Land District': 'SLD',
            'Southwestern District': 'SWD',
            'Sunshine District': 'SUN',
        }
        district = district_map.get(self.district)

        season_map = {
            'Fall': Convention.SEASON.fall,
            'Spring': Convention.SEASON.spring,
        }
        season = season_map.get(self.season)
        if self.district == 'BHS':
            season = Convention.SEASON.spring
        convention = Convention.objects.get(
            district=district,
            season=season,
            year=year,
            # name=name,
        )
        return convention

    def get_panelist(self):
        Panelist = apps.get_model('api.panelist')
        Convention = apps.get_model('cmanager.convention')
        Session = apps.get_model('smanager.session')
        Round = apps.get_model('api.round')

        year = self.year
        num = self.num

        name = self.convention

        district_map = {
            'Cardinal District': 'CAR',
            'Carolinas District': 'NSC',
            'Central States District': 'CSD',
            'Dixie District': 'DIX',
            'EVG': 'EVG',
            'EVG Division': 'EVG',
            'EVG Prelims': 'EVG',
            'Evergreen District': 'EVG',
            'FWD': 'FWD',
            'FWD Division': 'FWD',
            'FWD Prelims': 'FWD',
            'Far Western District': 'FWD',
            'Illinois District': 'ILL',
            'International': 'BHS',
            'JAD': 'JAD',
            'JAD Prelims': 'JAD',
            'Johnny Appleseed District': 'JAD',
            'LOL': 'LOL',
            'LOL Division': 'LOL',
            'LOL Prelims': 'LOL',
            'Land O\' Lakes District': 'LOL',
            'MAD': 'MAD',
            'MAD Division': 'MAD',
            'MAD Prelims': 'MAD',
            'Mid-Atlantic District': 'MAD',
            'NED': 'NED',
            'NED Division': 'NED',
            'NED Patriot': 'NED',
            'NED Prelims': 'NED',
            'Northeastern District': 'NED',
            'Ontario District': 'ONT',
            'Pioneer District': 'PIO',
            'RMD/FWD': 'RMD',
            'Rocky Mountain District': 'RMD',
            'SWD': 'SWD',
            'SWD Division': 'SWD',
            'SWD Prelims': 'SWD',
            'Seneca Land District': 'SLD',
            'Southwestern District': 'SWD',
            'Sunshine District': 'SUN',
        }
        district = district_map.get(self.district)

        season_map = {
            'Fall': Convention.SEASON.fall,
            'Spring': Convention.SEASON.spring,
        }
        season = season_map.get(self.season)
        if self.district == 'BHS':
            season = Convention.SEASON.spring

        session_map = {
            'Chorus': Session.KIND.chorus,
            'College': Session.KIND.quartet,
            'Quartet': Session.KIND.quartet,
            'Quartet College': Session.KIND.quartet,
            'Senior Chorus': Session.KIND.chorus,
            'Seniors': Session.KIND.quartet,
            'VLQ': Session.KIND.chorus,
        }
        session = session_map.get(self.session)

        round_map = {
            'Finals': Round.KIND.finals,
            'Quarter-Finals': Round.KIND.quarters,
            'Semi-Finals': Round.KIND.semis,
            'Youth Finals': Round.KIND.finals,
        }
        round = round_map.get(self.round)
        if self.district == 'BHS':
            season = Convention.SEASON.spring

        category_map = {
            'MUS': Panelist.CATEGORY.music,
            'PER': Panelist.CATEGORY.performance,
            'PRS': Panelist.CATEGORY.performance,
            'SNG': Panelist.CATEGORY.singing,
        }
        category = category_map.get(self.category)

        query = {
            'round__session__convention__district': district,
            'round__session__convention__season': season,
            'round__session__convention__year': year,
            'round__session__convention__name': name,
            'round__session__kind': session,
            'round__kind': round,
            'category': category,
            'num': num,
        }
        panelist = Panelist.objects.get(**query)
        return panelist

    def get_person(self):
        person_map = {
            '(Unknown)': 'ce995c5b-0909-4358-8628-5a6da2463fb8',
            'Adkisson,Russ': 'd3f74d4e-519a-4dd9-8d8c-fc67f61bde5d',
            'Agnew,Paul': '32827174-32b5-4ffc-bdf0-1834eac92354',
            'Aramian,Terry': '7cc07e45-8ea1-4e9b-9ae6-2d87b9cc5ef4',
            'Armstrong,Steve': '2bef5a76-f6d2-4ae3-8dcd-71ab391f3ef7',
            'Arnold,Chris': '2a7c0481-e973-4013-a948-e137698e4321',
            'Bagby,Jim': '50500277-ff98-4301-9e00-31f392e63d03',
            'Balsley,Toby': 'b18d647f-85eb-4434-8c76-e0ab3c6ea38d',
            'Barford,Brian': '7b3e1eb3-4e89-4976-97ef-9a8841d0dcc0',
            'Barr,Jimmy': 'f07c8761-147b-443f-a087-b38574ca080b',
            'Bartholomew,Anthony': '1a814045-747f-41e0-9235-df1b98ea4e58',
            'Beck,Brian': '441c1874-dc30-4006-88a1-88f256ae3e70',
            'Benedict,Lou': 'ddb940e0-8e14-4fda-aa03-4c1b44d2cd3e',
            'Black,Ron': 'bc886d31-3049-46ec-b7e2-bc774a6ec849',
            'Boegehold,Evan': 'd97d723b-8fc8-4948-8733-bdb159281cb0',
            'Bolles,Gary': 'ecac9f60-16bf-43ac-bc1e-d5807f98ee0a',
            'Brobst,Dwain': '8f75b926-8611-47b8-ad40-22a7d223f4f9',
            'Brockman,John': '9b1abd18-0bc9-40b1-81b5-16368d3922d5',
            'Brooks,Tim': 'e3ecd591-9b2f-4b5f-b924-81afaa71c8c2',
            'Bureau,Anne': 'e7912273-3631-4d76-aac2-08533dc8f3af',
            'Burns,Cary': '1ee9d1f4-22b7-49db-b179-c35e9a9481da',
            'Burri,John': '48595b7b-b31c-4c6c-b297-4ab72f0240d3',
            'Butterfield,Dr. Jay': 'bbe37cf8-1d22-4d29-8378-0f02ec30c7d6',
            'Caetano,Greg': '63e69c71-5680-4f3b-9ffd-d6ed58a727d2',
            'Campbell,Rob': 'de3e965d-713a-4dc4-8d5c-f81c70ab12cb',
            'Carolan,Andrew': '9fe604d8-3799-4230-8639-49d58a55ea88',
            'Cating,Mike': '0223ea0f-e03a-4aaf-b351-ca6e62360c5d',
            'Cerutti,Joe': '97fba197-b3c9-429e-a0c3-1f714dde427e',
            'Challman,Don': '78f86bb4-f985-41e9-9038-f8e085c1d2d5',
            'Clapper,Barry': 'fbba2b81-793f-41a7-ac79-d13def56fd4e',
            'Clemons,Larry': '8523efd2-4c3c-458b-948d-5fe402ab0364',
            'Coates,Diane': 'b76777b7-19d4-4690-adf7-6598dd5bde5b',
            'Coates,Jim': 'd0895a57-496c-4679-bce5-ee4cfa2c9e6d',
            'Coffin,John': '581772df-0da8-4fbb-ab1d-4f1812bb05df',
            'Colosimo,Anthony': '1f7e8fe0-2839-499e-b624-e6e5946bb273',
            'Comer,Dale': '9fd578a5-d6ac-412d-b93a-46fed2d31674',
            'Connelly,Joe': '0abd95f5-3f9e-4898-adc5-413c54babc90',
            'Conover,Jeremy': 'd4bb2cef-1171-42d1-a1bd-90351bee50b6',
            'Curulla,Steve': '9404c593-71fc-4bcd-85de-3678615cfb56',
            'Dalbey,Eric': '5fcb0a7e-09d4-4145-afc6-261b5de3b113',
            'Dale,Aaron': '83e1303c-5e8d-4e07-b2b9-4a4b6db4a02c',
            'DeBar,Phil': 'f6459f6f-1d05-4762-bd55-43fc9ef12db9',
            'DeBusman,Jim': 'fa85a8c9-0346-45fc-9ddf-ce2904629ed8',
            'Delehanty,Steve': 'a43de3b9-4359-4875-bdff-879e91bfe18e',
            'Deters,Larry': '77c7263f-0ec7-49fa-b892-52dfdc7aa0fd',
            'Devine,Sean': '27c91e4c-f926-4a83-8cba-a91b0eff39c6',
            'Dorn,Steve': 'c0410c98-f588-45de-a990-cef8df3a2847',
            'Dougherty,Jay': 'abad5b86-13f1-411c-a68e-ee507e27d960',
            'Driscoll,Denny': '1cf3a872-d1d1-4526-8e4f-d126bf2cc5cc',
            'Dunckel,Kevin': '7b5f2a0e-01eb-460a-b9e7-b892d0e2ec5c',
            'Ellis,Dave': 'e75f45e6-94e5-4cf4-8798-e1b5676adee0',
            'Emery,Jim': '10b951d4-e687-4fa2-9fdf-78e9b67522e4',
            'Engel,Paul': '4ae23b05-dd5f-4c27-893b-a00407947f5e',
            'Estes,James': '4e33ff4d-c023-42ae-9aa9-b5f3870cc35e',
            'Ewing,Craig': '4980d81f-79c5-4a4c-b210-fa0e1586880a',
            'Fellows,Matt': '7f435501-221d-4d15-8780-fd2d0be54f30',
            'Fisher,Ken': 'bffe2ba1-f0de-40c7-9dbf-0d7d07ca4a55',
            'Fisk,Al': 'a97a4de2-6982-4fa5-8790-3e951dcd9aad',
            'Flinn,Darryl': 'ce568aef-9ff1-4a61-a978-26350c2f001a',
            'Fobart,Dave': 'b6b50ed8-c89b-48a4-acdb-9c9249367572',
            'Foris,Russ': 'dc2de1bd-6803-4d95-9aef-8156c62ecee8',
            'Fredstrom,Martin': '821c0663-c28f-4342-a37e-91fc4b99b673',
            'Fritzen Jr,Ed': '7967a4e4-1ec2-488b-b2b2-36e5679e7c49',
            'Gasper,Allen': 'a0fd37eb-c4ce-41a4-97dd-016cfecbde83',
            'Gentry,Tom': '119e40e0-c751-43da-b866-4975c688a4c4',
            'Giallombardo,Jay': '3bac474a-9900-4e19-82c9-71cb5069b036',
            'Gifford,Matt': '532d2a87-1766-4d4e-b591-fca466c0834a',
            'Gipp,George': '7e41e7fe-7309-49ab-afde-fa8416895ccc',
            'Gordon,Alan': 'f9e641ae-0795-4cc0-8ffd-58c52aaef99c',
            'Graham,Brent': '30b1cf32-af91-4178-9bf2-a05bd02e1304',
            'Gray Jr.,Bobby': 'b6ed48b2-44cb-4987-8c63-f88334abb1e8',
            'Gray,Don': '57444738-b0ab-430a-99ec-111779e790b7',
            'Greason,Kathy': '64a2f4a1-493c-495e-bc22-93f783beb71a',
            'Guyton,Brandon': '16e5b10d-3b34-4e1a-b82a-e593a22c6c5c',
            'Guyton,Chad': 'd79dce71-b5e3-48f0-867f-79178b568ace',
            'Haflett,Harry': '275383f4-0402-44f8-969a-01b362c29d8d',
            'Hale,Mark': 'aef24022-ceee-446e-a5de-9ec5a0b45003',
            'Hammer,Hank': '7e7fe166-c921-45a0-98c7-1e52ea83d34b',
            'Hansen,Pete': 'd28d2d8b-0f40-464d-ac40-c467e4a07e94',
            'Hasty,Rich': '2ccaf9b2-c4eb-4a31-9ac8-5c7303b677a5',
            'Hawkins,Gary': '360e84b9-3ed0-4093-8698-5c6a33a61d0c',
            'Hebert,Chris': '9022834e-52aa-4c99-a003-27175a2e9e78',
            'Hettinga,Warren': 'e5601cf5-22e3-498b-8133-586904475ee0',
            'Hicks,Theo': '76e1e3a0-12fb-40ef-926e-ceb478831f79',
            'Hine,Clay': 'a3ba1654-3aa4-49af-9986-64388566cc8b',
            'Hodges,Bob': '4cba73cc-2361-4ff9-9899-eec8ba101acb',
            'Holdeman,Mark': 'cc495d67-d74a-4af2-9ce8-045034fa5f05',
            'Hunter Jr,Joe': '80426bd5-d2c1-4d85-86a6-f49b525097e2',
            'Israel,Marty': '658528a4-cd84-4b5e-a2a9-f626d798ae38',
            'Jakovac,Ig': '19aa5ee0-1733-42df-8cb8-045c3c4fb3fa',
            'Jamison,Stephen': 'da4620f6-94da-4239-b647-161228e57fba',
            'Jamison,Steve': 'da4620f6-94da-4239-b647-161228e57fba',
            'Janes,Linda': '69d3d446-212c-4168-b5b7-6c99fb9dd38e',
            'Janes,Steve': 'bab35f64-5a50-48a2-b675-d54d8478fffa',
            'Johnson,Rik': '9cd3610f-fef4-4523-8936-457a397e3ce4',
            'Johnson,Steve': '9218d51d-5e37-4e45-8705-a21e789d5e24',
            'Kahl,Don': 'd287f8c8-3aef-4263-9d25-e7aa64b2b295',
            'Kahlke,Jim': '55e23c66-20cf-4b74-af41-3618b0a44559',
            'Kastler,James': '350f7026-b5cb-4952-8771-c8632478cc4b',
            'Keil,Connie': '711bbfec-8b1d-4721-ac13-dfcf07819913',
            'Keller,Kevin': '5befc9d9-5ddf-4aa0-990d-d4804bf7346d',
            'Kelly,Michael': '2ac2bd0e-07f0-49f7-82fb-fa99c6e5a022',
            'Kettner,Mark': 'df77a58b-f948-40e2-b857-b3059381243d',
            'Kitzmiller,Kyle': '1dd340af-2aa7-4391-bf01-6649b6a30dd9',
            'Kitzmiller,Scott': '88ae88e6-b5e7-4217-a8bb-d6fbc42678d8',
            'Krause,David': '31727391-3a0a-42f9-a574-107769a0853e',
            'Krigström,Rasmus': 'a90db836-f980-4891-a11f-eaa66fe7af3a',
            'Krumbholz,Jay': '3d81f71e-ea9f-462f-8461-b288dd182522',
            'LaBar,Dave': '7ff892f9-e235-48e8-8f08-db82ea033910',
            'Lancaster,Opie': '1235d3d0-deb6-4244-941c-556451e3b985',
            'Lavene,Ritchie': '4af9ee85-0364-434b-8090-bdd18ef5364a',
            'Leeder,David': '8842343b-25cc-4fcb-a7bf-480910ff1e1e',
            'Lenoil,Robert': '72805b77-6243-45b6-8a51-6d65816cf94c',
            'Leontovich,Adrian': '8b6cc2f6-bd27-4d0b-a778-0bc4a8c09631',
            'Lewellen,Richard': '5ebe059e-93bd-4090-904e-a5bf22e4b591',
            'Lewis,Roger': 'a513de98-7c62-47eb-a62e-5d3fb68a4e14',
            'Lietke,Mike': 'ac7076d8-14bd-42f5-8677-9bc4a9756fab',
            'Liles,Joe': '9fce5388-eb53-408c-baf8-073da3937156',
            'Lindeman,Lauren': 'bd09dd72-51c5-432f-abe2-1603e60627e0',
            'Littlefield,Brett': '286ab890-b389-4195-8ab2-bcff313489b2',
            'Louque,Mike': '8c3e12fb-f23a-4a31-84ca-653d4a1dd20b',
            'Lovick,Marty': '9f96d62a-ee6d-4f4a-87f6-024bf51b9aaa',
            'Lower,Chuck': '414579a3-6384-4fd4-8ba2-7a00ab0c2323',
            'Lyne,Greg': '256e1b55-976e-4440-b6ad-0c8c8ab059eb',
            'Magness,Mark': 'edd43e42-0ca2-40fc-8ebe-a397750e5a76',
            'Mallett,John': '72ecd9c2-0f4f-4a23-86ad-be0d6f64ea82',
            'Mance,Rob': '7190cada-10a6-4092-8104-365d9ab2c57b',
            'Marron,Tim': '009a4092-88be-430c-8c9d-0affc34845a5',
            'Martinez,Eddie': '2e97992a-ac0a-4a59-949e-2cd4b1d26d1e',
            'Massey,Jim': '5489cd94-63a3-4e25-8dcd-79f192b9a4a0',
            'Matchinsky,Tom': '1dbb16b8-9df3-4560-9efd-a509a33170a9',
            'McAdory,Howard': '60df9301-34e4-43f2-8f19-b1ba6af4337e',
            'McEachern,David': '2dc14d08-a3ad-446f-bcce-cfff7a061e83',
            'McFadden,Robert': 'b418d44e-4298-42c3-90e7-6af6de4cd445',
            'McQueeny,Tom': '290a27f0-e25a-4384-ab66-c3b1f5203bc9',
            'Miller,Doug': '90c0f35c-d740-4eef-b85e-3026fc203af3',
            'Miller,Justin': '1da2e653-a166-42e1-90bf-047456a7545e',
            'Mills,David': '46daa784-8781-49a3-bfd9-42e23abfe23c',
            'Mills,Roger': '0778cc57-e63d-429e-91ef-7361bf58c212',
            'Mondragon,Shawn': 'c2c87d87-fc96-49bf-9268-175ebc5a1904',
            'Moorehead,Bob': '86bf785c-3b45-43f6-9435-b7d946eac0f4',
            'Morris,Alex': '69ab9e28-9fec-4b20-9be5-20f9797ccc1c',
            'Nau,Ev': '0fffa36b-84e7-4c00-b70c-363e223762cb',
            "O' Leary,Brian": 'ae3dbdad-42e5-4645-9a16-71cec0f1c22e',
            "O'Brien,Dan": 'd846a92b-2cb0-4741-94a4-b59fb625d6a6',
            "O'Dell,Brian": 'f0d8fec9-7961-440c-8a1d-57bf310710ed',
            "O'Donnell,Mike": 'a4d2d415-1946-40d1-a255-9f084878461c',
            'Ordaz,Phil': '5a2740e1-8539-45a1-b3cb-bbff0e4e3feb',
            'Orff,Judd': '12228bea-a02f-48fb-91bb-c1f3d3ae87fd',
            'Oxford,Dylan': 'dd1a4856-9f5a-4112-af6c-15560d2d3c9f',
            'Papageorge,Nick': 'ab9d3c3a-c377-44ac-b5a7-32709de2cfe6',
            'Papageorge,Sam': '965df9dd-6de4-4d60-b62f-f5c4966a07ee',
            'Payne,Roger': '6806d24d-67e6-440e-a59e-8e5b1e380f51',
            'Peterson,Chris': '871c1b01-3e0e-42e0-a82a-b2025083ca49',
            'Pirner,Jake': '9560e272-ea4d-4660-8626-842c9f5c704e',
            'Plaag,Gary': 'b0555de3-ec3d-4d9d-93ea-ffa04b1fe7f5',
            'Plumb,Steve': 'c8ca0b04-9816-4c7f-82a8-e2f216b05136',
            'Pope,Jeremiah': '5634dde5-e994-48f2-8e8c-31f384643bc1',
            'Porter,Adam': '15e9f720-f112-48f7-b682-f06d816f37e7',
            'Potter,Ken': 'eddabad4-5107-46f6-b5b6-fc6d8c956884',
            'Radcliffe,Shelagh': '81d45c9a-5ad0-44e8-893a-af04269a4e74',
            'Ramsson,Beth': '1ad0e4e7-fdbf-4d56-b0ae-b30e9c7c2a43',
            'Randall,Lynn': 'f5d701c6-3bad-435f-8110-dcbb4c5ac6ca',
            'Rank,Ron': 'ee83334b-4f61-4aef-8c21-95abb199e0d1',
            'Rashleigh,Bill': 'a1f74fdd-5fad-466a-a144-1559a9cb7731',
            'Reimnitz,Adam': '573b41f4-9d60-4de7-bc8f-01992d30009f',
            'Reinhart,Larry': '632c2500-f2e8-4766-baff-978eeb966800',
            'Reynolds,Tim': 'be8bdf9c-02aa-49d4-ba38-67901f387deb',
            'Richards,Chris': '24569050-9553-487b-ac01-f338c9ebfccd',
            'Richards,Jim': 'c073eeee-c438-4cc6-9eac-4513a8c1652f',
            'Ross,Roger': 'ea7a4da7-8443-4c65-aab9-61749e358a74',
            'Rubin,Alex': '7a5ccf95-59a2-4c47-8e8b-c5ccdb4373b3',
            'Rubin,David': 'cdbeff1e-868a-446d-87b9-02ac2ebf5c2a',
            'Sawyer,Joe': '3d864631-ebe9-4e79-aa8e-5bfcc28b6f52',
            'Schleier,Dusty': '7c21cf56-7bfa-4d86-9dbf-824aa42362a6',
            'Schlinkert,Mark': '09aa8ec8-54dd-491d-aedf-c8e870121417',
            'Schlinkert,Tom': 'eceeda02-6386-4ce7-ad7e-2cfa33d36f16',
            'Schwarzkopf,Raymond': '7b4c736c-ddf0-4483-b4ab-3e7a3299437b',
            'Scott,Adam': '04681ad6-f976-4326-8640-61cac4f82e9f',
            'Scott,Steve': '82df9e3f-13a0-409c-8378-23de4d111f31',
            'Sgrignoli,Rod': '62abb8b6-497c-4232-9c7a-88f8112a596f',
            'Sherburn,John': 'eb3d4bec-02d1-45ee-97df-113c769abedd',
            'Signor,Dan': '06a40f51-224d-4173-9e0c-dee248a4d55e',
            'Smeltz,Doug': 'dbb47dc6-7984-4825-8617-2bda17cc4d5e',
            'Sorge,Denny': '62fb396a-adfe-4a7e-8f4d-cf6906feea0c',
            'Sparks,Tony': '159d0475-8d03-49c3-96ef-a05741068c6c',
            'Spencer,Rick': '80b0c024-95d0-40e3-a480-a7d1a311ce5a',
            'Spilker,Gene': 'dc7084e2-e164-41c4-b457-d719735338b0',
            'Squires,Bob': '799be1ba-b0ba-4c52-b5e5-2f3b4c6c9f41',
            'St. John,Chad': '56d01389-4308-4fd4-afdd-a2f293d0b94f',
            'Stamm,Gary': '5e52c512-6728-4946-951a-2286c60105d6',
            'Stanfield,Roger': '893f10e6-5c56-4cbf-bc2a-be921e66301c',
            'Steinkamp,Gary': 'c801bc32-94dc-4832-94ae-396061ef511b',
            'Stevens,Jack': '5be6ef27-eb3a-4528-a583-fd0662ad3a00',
            'Stewart,Reid': '8bfd0c5f-0a50-409a-a41d-a318039cb64a',
            'Stock,Mark': '6115dc18-8c3e-469d-845c-96d3b63b4843',
            'Stone,Kathy': '133d38a6-5a19-4293-8b98-269b6769cf30',
            'Stothard,Don': 'f06bd51e-22b1-4883-8e88-4f0a42830745',
            'Stringfellow,Randy': 'c40c1ad1-af60-4068-9e0b-3b8b207839fc',
            'Strong,Robert': 'bbdce34b-1040-4535-8e43-576c4f3e2009',
            'Swann,Matt': 'bd590eaf-975f-4205-987b-258385d66a62',
            'Tautkus,Dave': 'b7113b04-5eca-4657-9f24-3178b3294d50',
            'Taylor,Jeff': '249684f8-e08d-4ab8-a98c-372cb45dd69a',
            'Towner,Barry': 'ed09401c-4ada-479c-a89a-d2849419f812',
            'Tramack,Renee': 'e51b2df8-9a51-4a05-b298-52309949a687',
            'Tramack,Steve': '5772e91e-d65b-4812-9b74-903af160c239',
            'Travis,Jordan': 'cd1d1390-0a37-448e-b7cb-9e5690495f51',
            'Treptow,Trep': '4f6ea184-cd50-4645-936f-c78410312350',
            'Vaughn,Chris': '439d94d2-1916-4913-8d5c-136eedc1ce40',
            'Waesche III,Ed': '8279a9a8-349c-4b07-bd4f-0d00332341e9',
            'Walker,Bob': '73222097-3fe8-4625-8b9e-e53db6d381fa',
            'Ward,John': 'c8cc5820-9a78-4528-a8b2-ab9e50c1d349',
            'Weatherbee,Theresa': '0017fae1-e2b1-481b-b5cc-cd8a68186d8e',
            'Wenner,Bruce': '29402acb-0c71-4ede-b4f1-961041bf278d',
            'Westin,Jan-Ake': '84e9e308-32b6-4d42-8fe8-306d1f022acf',
            'Wheaton,Drew': '8242039a-cbea-41b3-83fd-fcb7423c07c4',
            'Wietlisbach,Paul': '9f679a38-ad8c-415b-a1c3-706ce2d8b18a',
            'Wigley,Paul': 'da3a7b77-23fa-4cb4-8785-a9532a07251e',
            'Williams,Brian': '58677db2-f061-4477-b351-9cfd60a5abbc',
            'Williamson,Ed': '9073ac0d-095b-4c02-bf60-3c671595c53b',
            'Wilson,Scott': '2ebdb287-985a-4c0e-866d-da33a838b07a',
            'Wood,Susan': 'a829c680-343a-4270-8592-388f370befab',
            'Woodall,Tim': 'b60bada5-3286-4421-aeb3-fa1664d39ba6',
            'Woodall,Tom': '216d7713-7533-455c-8c7c-c9ff9c02139f',
            'Woods,Adam': 'df902e1f-38e9-4a6c-9860-42d061054055',
            'Wright,David': 'a107ed12-9fb2-47bb-b22e-4b19d8e27d3c',
            'Wright,Sandi': 'c8601cef-aaad-44f3-8193-ea39fe4f7b6a',
            'Wright,Wayne': 'f48d981c-0e4a-4cf5-858a-d774f14df898',
            'Wulf,Chad': 'a438868e-c55d-4813-9db7-a2fb397b371b',
            'Wulf,Gary': '97dda86e-1d10-4cae-aa49-a46609d2c54a',
            'Young,Kirk': 'dafdc134-975a-4d3d-a0d5-cf22c4b5775f',
            'Young,Russ': 'd5e3500b-c941-4069-9f2b-775421b47d62',
            'Zimmerman,David': '805cfe9b-8a20-4c13-b75a-17cffa35d37e',
            'Zink,Brian': 'e48534e3-02e3-4097-93e6-9753f453dac0',
            'Ryner,Jayson': '0c7bedfa-7449-4b58-8888-0b7f5824e268',
            'Hawker,Ben': 'c381968b-aa87-4fbf-a2de-a4b8bc595c69',
            'McAlexander,Patrick': '2792fb1e-8c64-48b6-93a9-35c959c26706',
            'Bugarin,Johnny': '6c5427e8-e127-4e6c-b7c3-9b821436d0c9',
            'Metzger,Charlie': '34d35e9c-9870-49af-92aa-4255cfbec3d6',
            'Baughman,Will': '37a61340-bdbf-4a15-ae7f-88caa5f63e96',
            'LeClair,Liz': 'b9083bf7-4f6b-4f0c-a00b-70544627299f',
            'Rembecki,Andrew': '2ee78623-a987-4faa-b8ff-872b2bf7e7bf',

            '': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            'Butterfield,Jay': 'bbe37cf8-1d22-4d29-8378-0f02ec30c7d6',
            'Campbell,Robert': 'de3e965d-713a-4dc4-8d5c-f81c70ab12cb',
            'Debar,Phil': 'f6459f6f-1d05-4762-bd55-43fc9ef12db9',
            'Debusman,Jim': 'fa85a8c9-0346-45fc-9ddf-ce2904629ed8',
            'Fritzen,Ed': '7967a4e4-1ec2-488b-b2b2-36e5679e7c49',
            'Gray Jr,Bobby': 'b6ed48b2-44cb-4987-8c63-f88334abb1e8',
            'Gray,Bobby': 'b6ed48b2-44cb-4987-8c63-f88334abb1e8',
            'Hunter,Joe C.': '80426bd5-d2c1-4d85-86a6-f49b525097e2',
            'Hunter,Jr,Joe': '80426bd5-d2c1-4d85-86a6-f49b525097e2',
            'McFadden,Bob': 'b418d44e-4298-42c3-90e7-6af6de4cd445',
            'McQueeney,Tom': '290a27f0-e25a-4384-ab66-c3b1f5203bc9',
            'Missing': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            "O'Leary,L. Brian": 'ae3dbdad-42e5-4645-9a16-71cec0f1c22e',
            'Payne,Rog': '6806d24d-67e6-440e-a59e-8e5b1e380f51',
            'Peterson,Christopher': '871c1b01-3e0e-42e0-a82a-b2025083ca49',
            'Rashleigh,William': 'a1f74fdd-5fad-466a-a144-1559a9cb7731',
            'Rubin,Dave': 'cdbeff1e-868a-446d-87b9-02ac2ebf5c2a',
            'Treptow,Richard': '4f6ea184-cd50-4645-936f-c78410312350',
            'XXX': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            'XXX,': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            'Brock,Bob': 'de6bca7e-f2ab-45f2-b527-b8ed84b482cf',
            'Clemons,Larry': '963ea6a1-feb2-48ac-b66b-304c76d208ec',
            'Coates,Diane': 'fbabb671-406a-4f40-ab11-db576dd37c72',
            'Ramsson,Beth': '3e103600-9cb4-49e3-aee7-c9e3d0e1aebc',
            'Lancaster,Opie': 'c964c74c-37c4-43e2-85c7-f1af66af5977',
            'Janes,Linda': '38167299-686e-4090-95f7-9e48cea2170d',
        }
        return person_map.get(self.judge)


class CleanSong(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )
    year = models.IntegerField(
    )
    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )
    season = models.IntegerField(
        choices=SEASON,
    )
    district = models.CharField(
        max_length=255,
    )
    convention = models.CharField(
        max_length=255,
    )
    SESSION = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )
    session = models.IntegerField(
        choices=SESSION,
    )
    ROUND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )
    round = models.IntegerField(
        choices=ROUND,
    )
    appearance_num = models.IntegerField(
    )
    song_num = models.IntegerField(
    )
    legacy_group = models.CharField(
        max_length=255,
    )
    legacy_chart = models.CharField(
        max_length=255,
    )
    scores = JSONField(
    )
    appearance = models.ForeignKey(
        'api.appearance',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    song = models.OneToOneField(
        'api.song',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    objects = CleanSongManager()


class CleanFlat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    cleanpanelist = models.ForeignKey(
        'CleanPanelist',
        related_name='cleanflats',
        on_delete=models.CASCADE,
    )
    cleansong = models.ForeignKey(
        'CleanSong',
        related_name='cleanflats',
        on_delete=models.CASCADE,
    )
    points = models.IntegerField(
    )
    score = models.OneToOneField(
        'api.score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    objects = CleanFlatManager()

    class Meta:
        unique_together = (
            ('cleanpanelist', 'cleansong',)
        )


class RawPanelist(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )
    year = models.IntegerField(
    )
    season = models.CharField(
        max_length=255,
    )
    district = models.CharField(
        max_length=255,
    )
    convention = models.CharField(
        max_length=255,
    )
    session = models.CharField(
        max_length=255,
    )
    round = models.CharField(
        max_length=255,
    )
    category = models.CharField(
        max_length=255,
    )
    num = models.IntegerField(
        null=True,
        blank=True,
    )
    judge = models.CharField(
        max_length=255,
    )
    scores = JSONField(
    )
    objects = RawPanelistManager()

    def get_convention(self):
        Convention = apps.get_model('cmanager.convention')
        year = self.year
        name = self.convention

        district_map = {
            'Cardinal District': 'CAR',
            'Carolinas District': 'NSC',
            'Central States District': 'CSD',
            'Dixie District': 'DIX',
            'EVG': 'EVG',
            'EVG Division': 'EVG',
            'EVG Prelims': 'EVG',
            'Evergreen District': 'EVG',
            'FWD': 'FWD',
            'FWD Division': 'FWD',
            'FWD Prelims': 'FWD',
            'Far Western District': 'FWD',
            'Illinois District': 'ILL',
            'International': 'BHS',
            'JAD': 'JAD',
            'JAD Prelims': 'JAD',
            'Johnny Appleseed District': 'JAD',
            'LOL': 'LOL',
            'LOL Division': 'LOL',
            'LOL Prelims': 'LOL',
            'Land O\' Lakes District': 'LOL',
            'MAD': 'MAD',
            'MAD Division': 'MAD',
            'MAD Prelims': 'MAD',
            'Mid-Atlantic District': 'MAD',
            'NED': 'NED',
            'NED Division': 'NED',
            'NED Patriot': 'NED',
            'NED Prelims': 'NED',
            'Northeastern District': 'NED',
            'Ontario District': 'ONT',
            'Pioneer District': 'PIO',
            'RMD/FWD': 'RMD',
            'Rocky Mountain District': 'RMD',
            'SWD': 'SWD',
            'SWD Division': 'SWD',
            'SWD Prelims': 'SWD',
            'Seneca Land District': 'SLD',
            'Southwestern District': 'SWD',
            'Sunshine District': 'SUN',
        }
        district = district_map.get(self.district)

        season_map = {
            'Fall': Convention.SEASON.fall,
            'Spring': Convention.SEASON.spring,
        }
        season = season_map.get(self.season)
        if self.district == 'BHS':
            season = Convention.SEASON.spring
        convention = Convention.objects.get(
            district=district,
            season=season,
            year=year,
            # name=name,
        )
        return convention

    def get_panelist(self):
        Panelist = apps.get_model('api.panelist')
        Convention = apps.get_model('cmanager.convention')
        Session = apps.get_model('smanager.session')
        Round = apps.get_model('api.round')

        year = self.year
        num = self.num

        name = self.convention

        district_map = {
            'Cardinal District': 'CAR',
            'Carolinas District': 'NSC',
            'Central States District': 'CSD',
            'Dixie District': 'DIX',
            'EVG': 'EVG',
            'EVG Division': 'EVG',
            'EVG Prelims': 'EVG',
            'Evergreen District': 'EVG',
            'FWD': 'FWD',
            'FWD Division': 'FWD',
            'FWD Prelims': 'FWD',
            'Far Western District': 'FWD',
            'Illinois District': 'ILL',
            'International': 'BHS',
            'JAD': 'JAD',
            'JAD Prelims': 'JAD',
            'Johnny Appleseed District': 'JAD',
            'LOL': 'LOL',
            'LOL Division': 'LOL',
            'LOL Prelims': 'LOL',
            'Land O\' Lakes District': 'LOL',
            'MAD': 'MAD',
            'MAD Division': 'MAD',
            'MAD Prelims': 'MAD',
            'Mid-Atlantic District': 'MAD',
            'NED': 'NED',
            'NED Division': 'NED',
            'NED Patriot': 'NED',
            'NED Prelims': 'NED',
            'Northeastern District': 'NED',
            'Ontario District': 'ONT',
            'Pioneer District': 'PIO',
            'RMD/FWD': 'RMD',
            'Rocky Mountain District': 'RMD',
            'SWD': 'SWD',
            'SWD Division': 'SWD',
            'SWD Prelims': 'SWD',
            'Seneca Land District': 'SLD',
            'Southwestern District': 'SWD',
            'Sunshine District': 'SUN',
        }
        district = district_map.get(self.district)

        season_map = {
            'Fall': Convention.SEASON.fall,
            'Spring': Convention.SEASON.spring,
        }
        season = season_map.get(self.season)
        if self.district == 'BHS':
            season = Convention.SEASON.spring

        session_map = {
            'Chorus': Session.KIND.chorus,
            'College': Session.KIND.quartet,
            'Quartet': Session.KIND.quartet,
            'Quartet College': Session.KIND.quartet,
            'Senior Chorus': Session.KIND.chorus,
            'Seniors': Session.KIND.quartet,
            'VLQ': Session.KIND.chorus,
        }
        session = session_map.get(self.session)

        round_map = {
            'Finals': Round.KIND.finals,
            'Quarter-Finals': Round.KIND.quarters,
            'Semi-Finals': Round.KIND.semis,
            'Youth Finals': Round.KIND.finals,
        }
        round = round_map.get(self.round)
        if self.district == 'BHS':
            season = Convention.SEASON.spring

        category_map = {
            'MUS': Panelist.CATEGORY.music,
            'PER': Panelist.CATEGORY.performance,
            'PRS': Panelist.CATEGORY.performance,
            'SNG': Panelist.CATEGORY.singing,
        }
        category = category_map.get(self.category)

        query = {
            'round__session__convention__district': district,
            'round__session__convention__season': season,
            'round__session__convention__year': year,
            'round__session__convention__name': name,
            'round__session__kind': session,
            'round__kind': round,
            'category': category,
            'num': num,
        }
        panelist = Panelist.objects.get(**query)
        return panelist

    def get_person(self):
        person_map = {
            '(Unknown)': 'ce995c5b-0909-4358-8628-5a6da2463fb8',
            'Adkisson,Russ': 'd3f74d4e-519a-4dd9-8d8c-fc67f61bde5d',
            'Agnew,Paul': '32827174-32b5-4ffc-bdf0-1834eac92354',
            'Aramian,Terry': '7cc07e45-8ea1-4e9b-9ae6-2d87b9cc5ef4',
            'Armstrong,Steve': '2bef5a76-f6d2-4ae3-8dcd-71ab391f3ef7',
            'Arnold,Chris': '2a7c0481-e973-4013-a948-e137698e4321',
            'Bagby,Jim': '50500277-ff98-4301-9e00-31f392e63d03',
            'Balsley,Toby': 'b18d647f-85eb-4434-8c76-e0ab3c6ea38d',
            'Barford,Brian': '7b3e1eb3-4e89-4976-97ef-9a8841d0dcc0',
            'Barr,Jimmy': 'f07c8761-147b-443f-a087-b38574ca080b',
            'Bartholomew,Anthony': '1a814045-747f-41e0-9235-df1b98ea4e58',
            'Beck,Brian': '441c1874-dc30-4006-88a1-88f256ae3e70',
            'Benedict,Lou': 'ddb940e0-8e14-4fda-aa03-4c1b44d2cd3e',
            'Black,Ron': 'bc886d31-3049-46ec-b7e2-bc774a6ec849',
            'Boegehold,Evan': 'd97d723b-8fc8-4948-8733-bdb159281cb0',
            'Bolles,Gary': 'ecac9f60-16bf-43ac-bc1e-d5807f98ee0a',
            'Brobst,Dwain': '8f75b926-8611-47b8-ad40-22a7d223f4f9',
            'Brockman,John': '9b1abd18-0bc9-40b1-81b5-16368d3922d5',
            'Brooks,Tim': 'e3ecd591-9b2f-4b5f-b924-81afaa71c8c2',
            'Bureau,Anne': 'e7912273-3631-4d76-aac2-08533dc8f3af',
            'Burns,Cary': '1ee9d1f4-22b7-49db-b179-c35e9a9481da',
            'Burri,John': '48595b7b-b31c-4c6c-b297-4ab72f0240d3',
            'Butterfield,Dr. Jay': 'bbe37cf8-1d22-4d29-8378-0f02ec30c7d6',
            'Caetano,Greg': '63e69c71-5680-4f3b-9ffd-d6ed58a727d2',
            'Campbell,Rob': 'de3e965d-713a-4dc4-8d5c-f81c70ab12cb',
            'Carolan,Andrew': '9fe604d8-3799-4230-8639-49d58a55ea88',
            'Cating,Mike': '0223ea0f-e03a-4aaf-b351-ca6e62360c5d',
            'Cerutti,Joe': '97fba197-b3c9-429e-a0c3-1f714dde427e',
            'Challman,Don': '78f86bb4-f985-41e9-9038-f8e085c1d2d5',
            'Clapper,Barry': 'fbba2b81-793f-41a7-ac79-d13def56fd4e',
            'Clemons,Larry': '8523efd2-4c3c-458b-948d-5fe402ab0364',
            'Coates,Diane': 'b76777b7-19d4-4690-adf7-6598dd5bde5b',
            'Coates,Jim': 'd0895a57-496c-4679-bce5-ee4cfa2c9e6d',
            'Coffin,John': '581772df-0da8-4fbb-ab1d-4f1812bb05df',
            'Colosimo,Anthony': '1f7e8fe0-2839-499e-b624-e6e5946bb273',
            'Comer,Dale': '9fd578a5-d6ac-412d-b93a-46fed2d31674',
            'Connelly,Joe': '0abd95f5-3f9e-4898-adc5-413c54babc90',
            'Conover,Jeremy': 'd4bb2cef-1171-42d1-a1bd-90351bee50b6',
            'Curulla,Steve': '9404c593-71fc-4bcd-85de-3678615cfb56',
            'Dalbey,Eric': '5fcb0a7e-09d4-4145-afc6-261b5de3b113',
            'Dale,Aaron': '83e1303c-5e8d-4e07-b2b9-4a4b6db4a02c',
            'DeBar,Phil': 'f6459f6f-1d05-4762-bd55-43fc9ef12db9',
            'DeBusman,Jim': 'fa85a8c9-0346-45fc-9ddf-ce2904629ed8',
            'Delehanty,Steve': 'a43de3b9-4359-4875-bdff-879e91bfe18e',
            'Deters,Larry': '77c7263f-0ec7-49fa-b892-52dfdc7aa0fd',
            'Devine,Sean': '27c91e4c-f926-4a83-8cba-a91b0eff39c6',
            'Dorn,Steve': 'c0410c98-f588-45de-a990-cef8df3a2847',
            'Dougherty,Jay': 'abad5b86-13f1-411c-a68e-ee507e27d960',
            'Driscoll,Denny': '1cf3a872-d1d1-4526-8e4f-d126bf2cc5cc',
            'Dunckel,Kevin': '7b5f2a0e-01eb-460a-b9e7-b892d0e2ec5c',
            'Ellis,Dave': 'e75f45e6-94e5-4cf4-8798-e1b5676adee0',
            'Emery,Jim': '10b951d4-e687-4fa2-9fdf-78e9b67522e4',
            'Engel,Paul': '4ae23b05-dd5f-4c27-893b-a00407947f5e',
            'Estes,James': '4e33ff4d-c023-42ae-9aa9-b5f3870cc35e',
            'Ewing,Craig': '4980d81f-79c5-4a4c-b210-fa0e1586880a',
            'Fellows,Matt': '7f435501-221d-4d15-8780-fd2d0be54f30',
            'Fisher,Ken': 'bffe2ba1-f0de-40c7-9dbf-0d7d07ca4a55',
            'Fisk,Al': 'a97a4de2-6982-4fa5-8790-3e951dcd9aad',
            'Flinn,Darryl': 'ce568aef-9ff1-4a61-a978-26350c2f001a',
            'Fobart,Dave': 'b6b50ed8-c89b-48a4-acdb-9c9249367572',
            'Foris,Russ': 'dc2de1bd-6803-4d95-9aef-8156c62ecee8',
            'Fredstrom,Martin': '821c0663-c28f-4342-a37e-91fc4b99b673',
            'Fritzen Jr,Ed': '7967a4e4-1ec2-488b-b2b2-36e5679e7c49',
            'Gasper,Allen': 'a0fd37eb-c4ce-41a4-97dd-016cfecbde83',
            'Gentry,Tom': '119e40e0-c751-43da-b866-4975c688a4c4',
            'Giallombardo,Jay': '3bac474a-9900-4e19-82c9-71cb5069b036',
            'Gifford,Matt': '532d2a87-1766-4d4e-b591-fca466c0834a',
            'Gipp,George': '7e41e7fe-7309-49ab-afde-fa8416895ccc',
            'Gordon,Alan': 'f9e641ae-0795-4cc0-8ffd-58c52aaef99c',
            'Graham,Brent': '30b1cf32-af91-4178-9bf2-a05bd02e1304',
            'Gray Jr.,Bobby': 'b6ed48b2-44cb-4987-8c63-f88334abb1e8',
            'Gray,Don': '57444738-b0ab-430a-99ec-111779e790b7',
            'Greason,Kathy': '64a2f4a1-493c-495e-bc22-93f783beb71a',
            'Guyton,Brandon': '16e5b10d-3b34-4e1a-b82a-e593a22c6c5c',
            'Guyton,Chad': 'd79dce71-b5e3-48f0-867f-79178b568ace',
            'Haflett,Harry': '275383f4-0402-44f8-969a-01b362c29d8d',
            'Hale,Mark': 'aef24022-ceee-446e-a5de-9ec5a0b45003',
            'Hammer,Hank': '7e7fe166-c921-45a0-98c7-1e52ea83d34b',
            'Hansen,Pete': 'd28d2d8b-0f40-464d-ac40-c467e4a07e94',
            'Hasty,Rich': '2ccaf9b2-c4eb-4a31-9ac8-5c7303b677a5',
            'Hawkins,Gary': '360e84b9-3ed0-4093-8698-5c6a33a61d0c',
            'Hebert,Chris': '9022834e-52aa-4c99-a003-27175a2e9e78',
            'Hettinga,Warren': 'e5601cf5-22e3-498b-8133-586904475ee0',
            'Hicks,Theo': '76e1e3a0-12fb-40ef-926e-ceb478831f79',
            'Hine,Clay': 'a3ba1654-3aa4-49af-9986-64388566cc8b',
            'Hodges,Bob': '4cba73cc-2361-4ff9-9899-eec8ba101acb',
            'Holdeman,Mark': 'cc495d67-d74a-4af2-9ce8-045034fa5f05',
            'Hunter Jr,Joe': '80426bd5-d2c1-4d85-86a6-f49b525097e2',
            'Israel,Marty': '658528a4-cd84-4b5e-a2a9-f626d798ae38',
            'Jakovac,Ig': '19aa5ee0-1733-42df-8cb8-045c3c4fb3fa',
            'Jamison,Stephen': 'da4620f6-94da-4239-b647-161228e57fba',
            'Jamison,Steve': 'da4620f6-94da-4239-b647-161228e57fba',
            'Janes,Linda': '69d3d446-212c-4168-b5b7-6c99fb9dd38e',
            'Janes,Steve': 'bab35f64-5a50-48a2-b675-d54d8478fffa',
            'Johnson,Rik': '9cd3610f-fef4-4523-8936-457a397e3ce4',
            'Johnson,Steve': '9218d51d-5e37-4e45-8705-a21e789d5e24',
            'Kahl,Don': 'd287f8c8-3aef-4263-9d25-e7aa64b2b295',
            'Kahlke,Jim': '55e23c66-20cf-4b74-af41-3618b0a44559',
            'Kastler,James': '350f7026-b5cb-4952-8771-c8632478cc4b',
            'Keil,Connie': '711bbfec-8b1d-4721-ac13-dfcf07819913',
            'Keller,Kevin': '5befc9d9-5ddf-4aa0-990d-d4804bf7346d',
            'Kelly,Michael': '2ac2bd0e-07f0-49f7-82fb-fa99c6e5a022',
            'Kettner,Mark': 'df77a58b-f948-40e2-b857-b3059381243d',
            'Kitzmiller,Kyle': '1dd340af-2aa7-4391-bf01-6649b6a30dd9',
            'Kitzmiller,Scott': '88ae88e6-b5e7-4217-a8bb-d6fbc42678d8',
            'Krause,David': '31727391-3a0a-42f9-a574-107769a0853e',
            'Krigström,Rasmus': 'a90db836-f980-4891-a11f-eaa66fe7af3a',
            'Krumbholz,Jay': '3d81f71e-ea9f-462f-8461-b288dd182522',
            'LaBar,Dave': '7ff892f9-e235-48e8-8f08-db82ea033910',
            'Lancaster,Opie': '1235d3d0-deb6-4244-941c-556451e3b985',
            'Lavene,Ritchie': '4af9ee85-0364-434b-8090-bdd18ef5364a',
            'Leeder,David': '8842343b-25cc-4fcb-a7bf-480910ff1e1e',
            'Lenoil,Robert': '72805b77-6243-45b6-8a51-6d65816cf94c',
            'Leontovich,Adrian': '8b6cc2f6-bd27-4d0b-a778-0bc4a8c09631',
            'Lewellen,Richard': '5ebe059e-93bd-4090-904e-a5bf22e4b591',
            'Lewis,Roger': 'a513de98-7c62-47eb-a62e-5d3fb68a4e14',
            'Lietke,Mike': 'ac7076d8-14bd-42f5-8677-9bc4a9756fab',
            'Liles,Joe': '9fce5388-eb53-408c-baf8-073da3937156',
            'Lindeman,Lauren': 'bd09dd72-51c5-432f-abe2-1603e60627e0',
            'Littlefield,Brett': '286ab890-b389-4195-8ab2-bcff313489b2',
            'Louque,Mike': '8c3e12fb-f23a-4a31-84ca-653d4a1dd20b',
            'Lovick,Marty': '9f96d62a-ee6d-4f4a-87f6-024bf51b9aaa',
            'Lower,Chuck': '414579a3-6384-4fd4-8ba2-7a00ab0c2323',
            'Lyne,Greg': '256e1b55-976e-4440-b6ad-0c8c8ab059eb',
            'Magness,Mark': 'edd43e42-0ca2-40fc-8ebe-a397750e5a76',
            'Mallett,John': '72ecd9c2-0f4f-4a23-86ad-be0d6f64ea82',
            'Mance,Rob': '7190cada-10a6-4092-8104-365d9ab2c57b',
            'Marron,Tim': '009a4092-88be-430c-8c9d-0affc34845a5',
            'Martinez,Eddie': '2e97992a-ac0a-4a59-949e-2cd4b1d26d1e',
            'Massey,Jim': '5489cd94-63a3-4e25-8dcd-79f192b9a4a0',
            'Matchinsky,Tom': '1dbb16b8-9df3-4560-9efd-a509a33170a9',
            'McAdory,Howard': '60df9301-34e4-43f2-8f19-b1ba6af4337e',
            'McEachern,David': '2dc14d08-a3ad-446f-bcce-cfff7a061e83',
            'McFadden,Robert': 'b418d44e-4298-42c3-90e7-6af6de4cd445',
            'McQueeny,Tom': '290a27f0-e25a-4384-ab66-c3b1f5203bc9',
            'Miller,Doug': '90c0f35c-d740-4eef-b85e-3026fc203af3',
            'Miller,Justin': '1da2e653-a166-42e1-90bf-047456a7545e',
            'Mills,David': '46daa784-8781-49a3-bfd9-42e23abfe23c',
            'Mills,Roger': '0778cc57-e63d-429e-91ef-7361bf58c212',
            'Mondragon,Shawn': 'c2c87d87-fc96-49bf-9268-175ebc5a1904',
            'Moorehead,Bob': '86bf785c-3b45-43f6-9435-b7d946eac0f4',
            'Morris,Alex': '69ab9e28-9fec-4b20-9be5-20f9797ccc1c',
            'Nau,Ev': '0fffa36b-84e7-4c00-b70c-363e223762cb',
            "O' Leary,Brian": 'ae3dbdad-42e5-4645-9a16-71cec0f1c22e',
            "O'Brien,Dan": 'd846a92b-2cb0-4741-94a4-b59fb625d6a6',
            "O'Dell,Brian": 'f0d8fec9-7961-440c-8a1d-57bf310710ed',
            "O'Donnell,Mike": 'a4d2d415-1946-40d1-a255-9f084878461c',
            'Ordaz,Phil': '5a2740e1-8539-45a1-b3cb-bbff0e4e3feb',
            'Orff,Judd': '12228bea-a02f-48fb-91bb-c1f3d3ae87fd',
            'Oxford,Dylan': 'dd1a4856-9f5a-4112-af6c-15560d2d3c9f',
            'Papageorge,Nick': 'ab9d3c3a-c377-44ac-b5a7-32709de2cfe6',
            'Papageorge,Sam': '965df9dd-6de4-4d60-b62f-f5c4966a07ee',
            'Payne,Roger': '6806d24d-67e6-440e-a59e-8e5b1e380f51',
            'Peterson,Chris': '871c1b01-3e0e-42e0-a82a-b2025083ca49',
            'Pirner,Jake': '9560e272-ea4d-4660-8626-842c9f5c704e',
            'Plaag,Gary': 'b0555de3-ec3d-4d9d-93ea-ffa04b1fe7f5',
            'Plumb,Steve': 'c8ca0b04-9816-4c7f-82a8-e2f216b05136',
            'Pope,Jeremiah': '5634dde5-e994-48f2-8e8c-31f384643bc1',
            'Porter,Adam': '15e9f720-f112-48f7-b682-f06d816f37e7',
            'Potter,Ken': 'eddabad4-5107-46f6-b5b6-fc6d8c956884',
            'Radcliffe,Shelagh': '81d45c9a-5ad0-44e8-893a-af04269a4e74',
            'Ramsson,Beth': '1ad0e4e7-fdbf-4d56-b0ae-b30e9c7c2a43',
            'Randall,Lynn': 'f5d701c6-3bad-435f-8110-dcbb4c5ac6ca',
            'Rank,Ron': 'ee83334b-4f61-4aef-8c21-95abb199e0d1',
            'Rashleigh,Bill': 'a1f74fdd-5fad-466a-a144-1559a9cb7731',
            'Reimnitz,Adam': '573b41f4-9d60-4de7-bc8f-01992d30009f',
            'Reinhart,Larry': '632c2500-f2e8-4766-baff-978eeb966800',
            'Reynolds,Tim': 'be8bdf9c-02aa-49d4-ba38-67901f387deb',
            'Richards,Chris': '24569050-9553-487b-ac01-f338c9ebfccd',
            'Richards,Jim': 'c073eeee-c438-4cc6-9eac-4513a8c1652f',
            'Ross,Roger': 'ea7a4da7-8443-4c65-aab9-61749e358a74',
            'Rubin,Alex': '7a5ccf95-59a2-4c47-8e8b-c5ccdb4373b3',
            'Rubin,David': 'cdbeff1e-868a-446d-87b9-02ac2ebf5c2a',
            'Sawyer,Joe': '3d864631-ebe9-4e79-aa8e-5bfcc28b6f52',
            'Schleier,Dusty': '7c21cf56-7bfa-4d86-9dbf-824aa42362a6',
            'Schlinkert,Mark': '09aa8ec8-54dd-491d-aedf-c8e870121417',
            'Schlinkert,Tom': 'eceeda02-6386-4ce7-ad7e-2cfa33d36f16',
            'Schwarzkopf,Raymond': '7b4c736c-ddf0-4483-b4ab-3e7a3299437b',
            'Scott,Adam': '04681ad6-f976-4326-8640-61cac4f82e9f',
            'Scott,Steve': '82df9e3f-13a0-409c-8378-23de4d111f31',
            'Sgrignoli,Rod': '62abb8b6-497c-4232-9c7a-88f8112a596f',
            'Sherburn,John': 'eb3d4bec-02d1-45ee-97df-113c769abedd',
            'Signor,Dan': '06a40f51-224d-4173-9e0c-dee248a4d55e',
            'Smeltz,Doug': 'dbb47dc6-7984-4825-8617-2bda17cc4d5e',
            'Sorge,Denny': '62fb396a-adfe-4a7e-8f4d-cf6906feea0c',
            'Sparks,Tony': '159d0475-8d03-49c3-96ef-a05741068c6c',
            'Spencer,Rick': '80b0c024-95d0-40e3-a480-a7d1a311ce5a',
            'Spilker,Gene': 'dc7084e2-e164-41c4-b457-d719735338b0',
            'Squires,Bob': '799be1ba-b0ba-4c52-b5e5-2f3b4c6c9f41',
            'St. John,Chad': '56d01389-4308-4fd4-afdd-a2f293d0b94f',
            'Stamm,Gary': '5e52c512-6728-4946-951a-2286c60105d6',
            'Stanfield,Roger': '893f10e6-5c56-4cbf-bc2a-be921e66301c',
            'Steinkamp,Gary': 'c801bc32-94dc-4832-94ae-396061ef511b',
            'Stevens,Jack': '5be6ef27-eb3a-4528-a583-fd0662ad3a00',
            'Stewart,Reid': '8bfd0c5f-0a50-409a-a41d-a318039cb64a',
            'Stock,Mark': '6115dc18-8c3e-469d-845c-96d3b63b4843',
            'Stone,Kathy': '133d38a6-5a19-4293-8b98-269b6769cf30',
            'Stothard,Don': 'f06bd51e-22b1-4883-8e88-4f0a42830745',
            'Stringfellow,Randy': 'c40c1ad1-af60-4068-9e0b-3b8b207839fc',
            'Strong,Robert': 'bbdce34b-1040-4535-8e43-576c4f3e2009',
            'Swann,Matt': 'bd590eaf-975f-4205-987b-258385d66a62',
            'Tautkus,Dave': 'b7113b04-5eca-4657-9f24-3178b3294d50',
            'Taylor,Jeff': '249684f8-e08d-4ab8-a98c-372cb45dd69a',
            'Towner,Barry': 'ed09401c-4ada-479c-a89a-d2849419f812',
            'Tramack,Renee': 'e51b2df8-9a51-4a05-b298-52309949a687',
            'Tramack,Steve': '5772e91e-d65b-4812-9b74-903af160c239',
            'Travis,Jordan': 'cd1d1390-0a37-448e-b7cb-9e5690495f51',
            'Treptow,Trep': '4f6ea184-cd50-4645-936f-c78410312350',
            'Vaughn,Chris': '439d94d2-1916-4913-8d5c-136eedc1ce40',
            'Waesche III,Ed': '8279a9a8-349c-4b07-bd4f-0d00332341e9',
            'Walker,Bob': '73222097-3fe8-4625-8b9e-e53db6d381fa',
            'Ward,John': 'c8cc5820-9a78-4528-a8b2-ab9e50c1d349',
            'Weatherbee,Theresa': '0017fae1-e2b1-481b-b5cc-cd8a68186d8e',
            'Wenner,Bruce': '29402acb-0c71-4ede-b4f1-961041bf278d',
            'Westin,Jan-Ake': '84e9e308-32b6-4d42-8fe8-306d1f022acf',
            'Wheaton,Drew': '8242039a-cbea-41b3-83fd-fcb7423c07c4',
            'Wietlisbach,Paul': '9f679a38-ad8c-415b-a1c3-706ce2d8b18a',
            'Wigley,Paul': 'da3a7b77-23fa-4cb4-8785-a9532a07251e',
            'Williams,Brian': '58677db2-f061-4477-b351-9cfd60a5abbc',
            'Williamson,Ed': '9073ac0d-095b-4c02-bf60-3c671595c53b',
            'Wilson,Scott': '2ebdb287-985a-4c0e-866d-da33a838b07a',
            'Wood,Susan': 'a829c680-343a-4270-8592-388f370befab',
            'Woodall,Tim': 'b60bada5-3286-4421-aeb3-fa1664d39ba6',
            'Woodall,Tom': '216d7713-7533-455c-8c7c-c9ff9c02139f',
            'Woods,Adam': 'df902e1f-38e9-4a6c-9860-42d061054055',
            'Wright,David': 'a107ed12-9fb2-47bb-b22e-4b19d8e27d3c',
            'Wright,Sandi': 'c8601cef-aaad-44f3-8193-ea39fe4f7b6a',
            'Wright,Wayne': 'f48d981c-0e4a-4cf5-858a-d774f14df898',
            'Wulf,Chad': 'a438868e-c55d-4813-9db7-a2fb397b371b',
            'Wulf,Gary': '97dda86e-1d10-4cae-aa49-a46609d2c54a',
            'Young,Kirk': 'dafdc134-975a-4d3d-a0d5-cf22c4b5775f',
            'Young,Russ': 'd5e3500b-c941-4069-9f2b-775421b47d62',
            'Zimmerman,David': '805cfe9b-8a20-4c13-b75a-17cffa35d37e',
            'Zink,Brian': 'e48534e3-02e3-4097-93e6-9753f453dac0',
            'Ryner,Jayson': '0c7bedfa-7449-4b58-8888-0b7f5824e268',
            'Hawker,Ben': 'c381968b-aa87-4fbf-a2de-a4b8bc595c69',
            'McAlexander,Patrick': '2792fb1e-8c64-48b6-93a9-35c959c26706',
            'Bugarin,Johnny': '6c5427e8-e127-4e6c-b7c3-9b821436d0c9',
            'Metzger,Charlie': '34d35e9c-9870-49af-92aa-4255cfbec3d6',
            'Baughman,Will': '37a61340-bdbf-4a15-ae7f-88caa5f63e96',
            'LeClair,Liz': 'b9083bf7-4f6b-4f0c-a00b-70544627299f',
            'Rembecki,Andrew': '2ee78623-a987-4faa-b8ff-872b2bf7e7bf',

            '': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            'Butterfield,Jay': 'bbe37cf8-1d22-4d29-8378-0f02ec30c7d6',
            'Campbell,Robert': 'de3e965d-713a-4dc4-8d5c-f81c70ab12cb',
            'Debar,Phil': 'f6459f6f-1d05-4762-bd55-43fc9ef12db9',
            'Debusman,Jim': 'fa85a8c9-0346-45fc-9ddf-ce2904629ed8',
            'Fritzen,Ed': '7967a4e4-1ec2-488b-b2b2-36e5679e7c49',
            'Gray Jr,Bobby': 'b6ed48b2-44cb-4987-8c63-f88334abb1e8',
            'Gray,Bobby': 'b6ed48b2-44cb-4987-8c63-f88334abb1e8',
            'Hunter,Joe C.': '80426bd5-d2c1-4d85-86a6-f49b525097e2',
            'Hunter,Jr,Joe': '80426bd5-d2c1-4d85-86a6-f49b525097e2',
            'McFadden,Bob': 'b418d44e-4298-42c3-90e7-6af6de4cd445',
            'McQueeney,Tom': '290a27f0-e25a-4384-ab66-c3b1f5203bc9',
            'Missing': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            "O'Leary,L. Brian": 'ae3dbdad-42e5-4645-9a16-71cec0f1c22e',
            'Payne,Rog': '6806d24d-67e6-440e-a59e-8e5b1e380f51',
            'Peterson,Christopher': '871c1b01-3e0e-42e0-a82a-b2025083ca49',
            'Rashleigh,William': 'a1f74fdd-5fad-466a-a144-1559a9cb7731',
            'Rubin,Dave': 'cdbeff1e-868a-446d-87b9-02ac2ebf5c2a',
            'Treptow,Richard': '4f6ea184-cd50-4645-936f-c78410312350',
            'XXX': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            'XXX,': 'fafadbd6-5317-456c-b288-0de64ea83f25',
            'Brock,Bob': 'de6bca7e-f2ab-45f2-b527-b8ed84b482cf',
            'Clemons,Larry': '963ea6a1-feb2-48ac-b66b-304c76d208ec',
            'Coates,Diane': 'fbabb671-406a-4f40-ab11-db576dd37c72',
            'Ramsson,Beth': '3e103600-9cb4-49e3-aee7-c9e3d0e1aebc',
            'Lancaster,Opie': 'c964c74c-37c4-43e2-85c7-f1af66af5977',
            'Janes,Linda': '38167299-686e-4090-95f7-9e48cea2170d',
        }
        return person_map.get(self.judge)


class RawSong(models.Model):
    id = models.IntegerField(
        primary_key=True,
        editable=False,
    )
    season = models.CharField(
        max_length=255,
    )
    year = models.IntegerField(
    )
    district = models.CharField(
        max_length=255,
    )
    event = models.CharField(
        max_length=255,
    )
    session = models.CharField(
        max_length=255,
    )
    group_name = models.CharField(
        max_length=255,
    )
    appearance_num = models.IntegerField(
    )
    song_num = models.IntegerField(
    )
    song_title = models.CharField(
        max_length=255,
    )
    totals = models.IntegerField(
    )
    scores = JSONField(
    )
    objects = RawSongManager()

    def get_convention(self):
        Convention = apps.get_model('cmanager.convention')
        year = self.year
        name = self.event

        district_map = {
            'CAR': 'CAR',
            'CSD': 'CSD',
            'CSD/ILL': 'CSD',
            'College': 'BHS',
            'DIX': 'DIX',
            'EVG': 'EVG',
            'FWD': 'FWD',
            'ILL': 'ILL',
            'INTL': 'BHS',
            'Int\'l': 'BHS',
            'International': 'BHS',
            'Intl': 'BHS',
            'JAD': 'JAD',
            'LOL': 'LOL',
            'MAD': 'MAD',
            'Midwinter': 'BHS',
            'NED': 'NED',
            'NSC': 'NSC',
            'ONT': 'ONT',
            'PIO': 'PIO',
            'PRS': 'NSC',
            'RMD': 'RMD',
            'RMD/FWD': 'RMD',
            'SLD': 'SLD',
            'SUN': 'SUN',
            'SWD': 'SWD',
            'Senior': 'BHS',
         }
        district = district_map.get(self.district)

        season_map = {
            'Fall': Convention.SEASON.fall,
            'Spring': Convention.SEASON.spring,
        }
        season = season_map.get(self.season)
        if self.district == 'BHS':
            season = Convention.SEASON.spring
        convention = Convention.objects.get(
            district=district,
            season=season,
            year=year,
            # name=name,
        )
        return convention


    def get_song(self):
        Song = apps.get_model('api.song')
        Convention = apps.get_model('cmanager.convention')
        Session = apps.get_model('smanager.session')
        Round = apps.get_model('api.round')

        year = self.year
        name = self.event
        appearance_num = self.appearance_num
        song_num = self.song_num

        district_map = {
            'CAR': 'CAR',
            'CSD': 'CSD',
            'CSD/ILL': 'CSD',
            'College': 'BHS',
            'DIX': 'DIX',
            'EVG': 'EVG',
            'FWD': 'FWD',
            'ILL': 'ILL',
            'INTL': 'BHS',
            'Int\'l': 'BHS',
            'International': 'BHS',
            'Intl': 'BHS',
            'JAD': 'JAD',
            'LOL': 'LOL',
            'MAD': 'MAD',
            'Midwinter': 'BHS',
            'NED': 'NED',
            'NSC': 'NSC',
            'ONT': 'ONT',
            'PIO': 'PIO',
            'PRS': 'NSC',
            'RMD': 'RMD',
            'RMD/FWD': 'RMD',
            'SLD': 'SLD',
            'SUN': 'SUN',
            'SWD': 'SWD',
            'Senior': 'BHS',
         }
        district = district_map.get(self.district)

        season_map = {
            'Fall': Convention.SEASON.fall,
            'Spring': Convention.SEASON.spring,
        }
        season = season_map.get(self.season)
        if self.district == 'BHS':
            season = Convention.SEASON.spring

        session_map = {
            'Chorus Finals': Session.KIND.chorus,
            'Chorus Semi-Finals': Session.KIND.chorus,
            'Quartet Finals': Session.KIND.quartet,
            'Quartet Finals Colle': Session.KIND.quartet,
            'Quartet Finals Senio': Session.KIND.quartet,
            'Quartet Finals Seniors': Session.KIND.quartet,
            'Quartet Finals Youth': Session.KIND.quartet,
            'Quartet Quarter-Fina': Session.KIND.quartet,
            'Quartet Quarterfinals': Session.KIND.quartet,
            'Quartet Semi-Finals': Session.KIND.quartet,
            'Quartet Semifinals':Session.KIND.quartet,
            'Seniors Chorus': Session.KIND.chorus,
            'Very Large Quartet': Session.KIND.chorus,
        }
        session = session_map.get(self.session)

        round_map = {
            'Chorus Finals': Round.KIND.finals,
            'Chorus Semi-Finals': Round.KIND.semis,
            'Quartet Finals': Round.KIND.finals,
            'Quartet Finals Colle': Round.KIND.finals,
            'Quartet Finals Senio': Round.KIND.finals,
            'Quartet Finals Seniors': Round.KIND.finals,
            'Quartet Finals Youth': Round.KIND.finals,
            'Quartet Quarter-Fina': Round.KIND.quarters,
            'Quartet Quarterfinals': Round.KIND.quarters,
            'Quartet Semi-Finals': Round.KIND.semis,
            'Quartet Semifinals': Round.KIND.semis,
            'Seniors Chorus': Round.KIND.finals,
            'Very Large Quartet': Round.KIND.finals,
         }
        round = round_map.get(self.session)

        query = {
            'appearance__round__session__convention__season': season,
            'appearance__round__session__convention__year': year,
            'appearance__round__session__convention__district': district,
            # 'appearance__round__session__convention__name': name,
            'appearance__round__session__kind': session,
            'appearance__round__kind': round,
            'appearance__num': appearance_num,
            'num': song_num,
            # 'appearance__group__id': group_id,
            # 'chart__id': song_id,
        }
        try:
            song = Song.objects.get(**query)
        except Song.DoesNotExist:
            return query
        return


class Flat(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    complete = models.ForeignKey(
        'Complete',
        related_name='flats',
        on_delete=models.CASCADE,
    )
    selection = models.ForeignKey(
        'Selection',
        related_name='flats',
        on_delete=models.CASCADE,
    )
    score = models.OneToOneField(
        'api.score',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    class Meta:
        unique_together = (
            ('complete', 'selection', 'score'),
        )

    def clean(self):
        if self.complete.panelist.round != self.selection.song.appearance.round:
            raise ValidationError('Rounds do not match')


class Selection(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    mark = models.BooleanField(
        default=False,
    )

    row_id = models.IntegerField(
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        null=True,
        blank=True,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    season_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SEASON
    )

    district_code = models.CharField(
        blank=True,
        max_length=255,
    )

    convention_name = models.CharField(
        blank=True,
        max_length=255,
    )

    SESSION_KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )

    session_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SESSION_KIND
    )

    ROUND_KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )

    round_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=ROUND_KIND
    )

    group_name = models.CharField(
        blank=True,
        max_length=255,
    )

    appearance_num = models.IntegerField(
        null=True,
        blank=True,
    )

    song_num = models.IntegerField(
        null=True,
        blank=True,
    )

    song_title = models.CharField(
        blank=True,
        max_length=255,
    )

    totals = models.IntegerField(
        null=True,
        blank=True,
    )

    points = ArrayField(
        base_field=models.IntegerField(
            null=True,
            blank=True,
        ),
        null=True,
        blank=True,
    )

    song = models.OneToOneField(
        'api.song',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = SelectionManager()


class Complete(models.Model):
    """LCD: Panelist"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    row_id = models.IntegerField(
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        null=True,
        blank=True,
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    season_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SEASON
    )

    SEASON = Choices(
        (1, 'summer', 'Summer',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
    )

    district_code = models.CharField(
        blank=True,
        max_length=255,
    )

    convention_name = models.CharField(
        blank=True,
        max_length=255,
    )

    SESSION_KIND = Choices(
        (32, 'chorus', "Chorus"),
        (41, 'quartet', "Quartet"),
        (42, 'mixed', "Mixed"),
        (43, 'senior', "Senior"),
        (44, 'youth', "Youth"),
        (45, 'unknown', "Unknown"),
        (46, 'vlq', "VLQ"),
    )

    session_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=SESSION_KIND
    )

    ROUND_KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semi-Finals'),
        (3, 'quarters', 'Quarter-Finals'),
    )

    round_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=ROUND_KIND
    )

    CATEGORY_KIND = Choices(
        (30, 'mus', 'Music'),
        (40, 'per', 'Performance'),
        (50, 'sng', 'Singing'),
    )

    category_kind = models.IntegerField(
        null=True,
        blank=True,
        choices=CATEGORY_KIND
    )

    points = ArrayField(
        base_field=models.IntegerField(
            null=True,
            blank=True,
        ),
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        'bhs.person',
        related_name='completes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    panelist = models.OneToOneField(
        'api.panelist',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = CompleteManager()
