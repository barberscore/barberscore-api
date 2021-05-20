import json

# Third-Party
from model_utils import Choices
from distutils.util import strtobool

# Local
from apps.bhs.models import Convention, Award, Chart, Group, Person
from apps.registration.models import Contest, Session, Assignment, Entry

class SfConvention:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Name
        if hasattr(n, 'sf_Name'):
            d['name'] = str(n.sf_Name.cdata)

        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Season
        if hasattr(n, 'sf_BS_Season__c'):
            season = int(float(n.sf_BS_Season__c.cdata))
            d['season'] = season

        # Panel
        if hasattr(n, 'sf_BS_Panel__c'):
            d['panel'] = int(float(n.sf_BS_Panel__c.cdata))

        # Year
        if hasattr(n, 'sf_Year__c'):
            d['year'] = int(n.sf_Year__c.cdata)

        # Open Date
        if hasattr(n, 'sf_Open_Date__c'):
            d['open_date'] = n.sf_Open_Date__c.cdata

        # Close Date
        if hasattr(n, 'sf_Close_Date__c'):
            d['close_date'] = n.sf_Close_Date__c.cdata

        # Start Date
        if hasattr(n, 'sf_Start_Date__c'):
            d['start_date'] = n.sf_Start_Date__c.cdata

        # End Date
        if hasattr(n, 'sf_End_Date__c'):
            d['end_date'] = n.sf_End_Date__c.cdata

        # Venue
        if hasattr(n, 'sf_Venue__c'):
            d['venue_name'] = n.sf_Venue__c.cdata

        # Location
        if hasattr(n, 'sf_Location__c'):
            d['location'] = n.sf_Location__c.cdata

        # Time Zone
        if hasattr(n, 'sf_Time_Zone__c'):
            d['timezone'] = n.sf_Time_Zone__c.cdata

        # Description
        d['description'] = n.sf_Description__c.cdata if hasattr(n, 'sf_Description__c') else ""

        # Divisions
        if hasattr(n, 'sf_BS_Division__c'):
            d['divisions'] = n.sf_BS_Division__c.cdata

        # Kinds
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kinds'] = n.sf_BS_Kind__c.cdata

        # Return parsed dict
        return d

class SfAward:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Name
        if hasattr(n, 'sf_Name'):
            d['name'] = n.sf_Name.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Kind
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kind'] = int(float(n.sf_BS_Kind__c.cdata))

        # Gender
        d['gender'] = int(float(n.sf_BS_Classification__c.cdata)) if hasattr(n, 'sf_BS_Classification__c') else None

        # Level
        if hasattr(n, 'sf_BS_Level__c'):
            d['level'] = int(float(n.sf_BS_Level__c.cdata))

        # Season
        if hasattr(n, 'sf_BS_Season__c'):
            d['season'] = int(float(n.sf_BS_Season__c.cdata))

        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Divisions
        d['division'] = int(float(n.sf_BS_Division__c.cdata)) if hasattr(n, 'sf_BS_Division__c') else None

        # Is Single
        if hasattr(n, 'sf_is_single__c'):
            d['is_single'] = bool(strtobool(n.sf_is_single__c.cdata))

        # Threshold
        d['threshold'] = float(n.sf_Threshold__c.cdata) if hasattr(n, 'sf_Threshold__c') else None

        # Minimum
        d['minimum'] = float(n.sf_Minimum__c.cdata) if hasattr(n, 'sf_Minimum__c') else None

        # advance
        d['advance'] = float(n.sf_Advance__c.cdata) if hasattr(n, 'sf_Advance__c') else None

        # spots
        d['spots'] = int(float(n.sf_Spots__c.cdata)) if hasattr(n, 'sf_Spots__c') else None

        # Description
        d['description'] = n.sf_Description__c.cdata if hasattr(n, 'sf_Description__c') else ""

        # Notes
        d['notes'] = n.sf_Notes__c.cdata if hasattr(n, 'sf_Notes__c') else ""

        # Age
        d['age'] = int(float(n.sf_BS_Age__c.cdata)) if hasattr(n, 'sf_BS_Age__c') else None

        # Is Novice
        if hasattr(n, 'sf_is_novice__c'):
            d['is_novice'] = bool(strtobool(n.sf_is_novice__c.cdata))

        # Size
        d['size'] = int(float(n.sf_BS_Size__c.cdata)) if hasattr(n, 'sf_BS_Size__c') else None

        # Size Range
        d['size_range'] = n.sf_Size_Range__c.cdata if hasattr(n, 'sf_Size_Range__c') else None

        # Scope
        d['scope'] = int(float(n.sf_BS_Scope__c.cdata)) if hasattr(n, 'sf_BS_Scope__c') else None

        # Scope Range
        d['scope_range'] = n.sf_Scope_Range__c.cdata if hasattr(n, 'sf_Scope_Range__c') else None

        # Tree Sort
        d['tree_sort'] = int(float(n.sf_Tree_Sort__c.cdata)) if hasattr(n, 'sf_Tree_Sort__c') else None

        # Return parsed dict
        return d

class SfChart:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Name
        if hasattr(n, 'sf_Name'):
            d['title'] = n.sf_Name.cdata

        # Arrangers
        if hasattr(n, 'sf_Arrangers__c'):
            d['arrangers'] = n.sf_Arrangers__c.cdata

        # Composer
        d['composers'] = n.sf_Composers__c.cdata if hasattr(n, 'sf_Composers__c') else ""

        # Lyricist
        d['lyricists'] = n.sf_Lyricists__c.cdata if hasattr(n, 'sf_Lyricists__c') else ""

        # Holders
        d['holders'] = n.sf_Holders__c.cdata if hasattr(n, 'sf_Holders__c') else ""

        # Description
        d['description'] = n.sf_Description__c.cdata if hasattr(n, 'sf_Description__c') else ""

        # Notes
        d['notes'] = n.sf_Notes__c.cdata if hasattr(n, 'sf_Notes__c') else ""

        # Return parsed dict
        return d

class SfGroup:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Name
        if hasattr(n, 'sf_Name'):
            d['name'] = n.sf_Name.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Kind
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kind'] = int(float(n.sf_BS_Kind__c.cdata))

        # Gender
        if hasattr(n, 'sf_BS_Classification__c'):
            d['gender'] = int(float(n.sf_BS_Classification__c.cdata))

        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Divisions
        d['division'] = int(float(n.sf_BS_Division__c.cdata)) if hasattr(n, 'sf_BS_Division__c') else None

        # bhs_id
        d['bhs_id'] = int(n.sf_cfg_Member_Id__c.cdata) if hasattr(n, 'sf_cfg_Member_Id__c') else None

        # code
        d['code'] = n.sf_cfg_Code__c.cdata if hasattr(n, 'sf_cfg_Code__c') else ""

        # Return parsed dict
        return d

class SfPerson:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Name
        if hasattr(n, 'sf_FirstName') and hasattr(n, 'sf_LastName'):
            d['name'] = n.sf_FirstName.cdata + " " + n.sf_LastName.cdata

        # First Name
        d['first_name'] = n.sf_FirstName.cdata if hasattr(n, 'sf_FirstName') else ""

        # Last Name
        d['last_name'] = n.sf_LastName.cdata if hasattr(n, 'sf_LastName') else ""

        # part
        d['part'] = int(float(n.sf_BS_VoicePart__c.cdata)) if hasattr(n, 'sf_BS_VoicePart__c') else None

        # Gender
        d['gender'] = int(float(n.sf_BS_Gender__c.cdata)) if hasattr(n, 'sf_BS_Gender__c') else None

        # Email
        d['email'] = n.sf_npe01__HomeEmail__c.cdata if hasattr(n, 'sf_npe01__HomeEmail__c') else ""

        # Home Phone
        d['home_phone'] = n.sf_HomePhone.cdata if hasattr(n, 'sf_HomePhone') else ""

        # Cell Phone
        d['cell_phone'] = n.sf_MobilePhone.cdata if hasattr(n, 'sf_MobilePhone') else ""

        # BHS ID
        d['bhs_id'] = int(n.sf_cfg_Member_Number__c.cdata) if hasattr(n, 'sf_cfg_Member_Number__c') else None

        # Return parsed dict
        return d

class SfSession:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Kind
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kind'] = int(float(n.sf_BS_Kind__c.cdata))

        # Num Rounds
        if hasattr(n, 'sf_Num_rounds__c'):
            d['num_rounds'] = int(float(n.sf_Num_rounds__c.cdata))

        # Is Invitational
        if hasattr(n, 'sf_is_invitational__c'):
            d['is_invitational'] = bool(strtobool(n.sf_is_invitational__c.cdata))

        # Description
        d['description'] = n.sf_Description__c.cdata if hasattr(n, 'sf_Description__c') else ""

        # Notes
        d['notes'] = n.sf_Notes__c.cdata if hasattr(n, 'sf_Notes__c') else ""

        # Footnotes
        d['footnotes'] = n.sf_Footnotes__c.cdata if hasattr(n, 'sf_Footnotes__c') else ""

        if hasattr(n, 'sf_BS_Convention_UUID__c'):
            d['convention_id'] = n.sf_BS_Convention_UUID__c.cdata

        # Name
        if hasattr(n, 'sf_Name'):
            d['name'] = n.sf_Name.cdata

        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Season
        if hasattr(n, 'sf_BS_Season__c'):
            d['season'] = int(float(n.sf_BS_Season__c.cdata))

        # Panel
        if hasattr(n, 'sf_BS_Panel__c'):
            d['panel'] = int(float(n.sf_BS_Panel__c.cdata))

        # Year
        if hasattr(n, 'sf_Year__c'):
            d['year'] = int(n.sf_Year__c.cdata)

        # Open Date
        if hasattr(n, 'sf_Open_Date__c'):
            d['open_date'] = n.sf_Open_Date__c.cdata

        # Close Date
        if hasattr(n, 'sf_Close_Date__c'):
            d['close_date'] = n.sf_Close_Date__c.cdata

        # Start Date
        if hasattr(n, 'sf_Start_Date__c'):
            d['start_date'] = n.sf_Start_Date__c.cdata

        # End Date
        if hasattr(n, 'sf_End_Date__c'):
            d['end_date'] = n.sf_End_Date__c.cdata

        # Venue
        if hasattr(n, 'sf_Venue__c'):
            d['venue_name'] = n.sf_Venue__c.cdata

        # Location
        if hasattr(n, 'sf_Location__c'):
            d['location'] = n.sf_Location__c.cdata

        # Time Zone
        if hasattr(n, 'sf_Time_Zone__c'):
            d['timezone'] = n.sf_Time_Zone__c.cdata

        # Divisions
        if hasattr(n, 'sf_BS_Division__c'):
            d['divisions'] = n.sf_BS_Division__c.cdata

        # Return parsed dict
        return d

class SfContest:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Award ID
        if hasattr(n, 'BS_Award_UUID__c'):
            d['award_id'] = n.BS_Award_UUID__c.cdata

        # Name
        if hasattr(n, 'sf_Name'):
            d['name'] = n.sf_Name.cdata

        # Kind
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kind'] = int(float(n.sf_BS_Kind__c.cdata))

        # Gender
        d['gender'] = int(float(n.sf_BS_Classification__c.cdata)) if hasattr(n, 'sf_BS_Classification__c') else None

        # Level
        if hasattr(n, 'sf_BS_Level__c'):
            d['level'] = int(float(n.sf_BS_Level__c.cdata))

        # Season
        if hasattr(n, 'sf_BS_Season__c'):
            d['season'] = int(float(n.sf_BS_Season__c.cdata))

        # Description
        d['description'] = n.sf_Description__c.cdata if hasattr(n, 'sf_Description__c') else ""

        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Divisions
        d['division'] = int(float(n.sf_BS_Division__c.cdata)) if hasattr(n, 'sf_BS_Division__c') else None

        # Age
        d['age'] = int(float(n.sf_BS_Age__c.cdata)) if hasattr(n, 'sf_BS_Age__c') else None

        # Is Novice
        if hasattr(n, 'sf_is_novice__c'):
            d['is_novice'] = bool(strtobool(n.sf_is_novice__c.cdata))

        # Is Single
        if hasattr(n, 'sf_is_single__c'):
            d['is_single'] = bool(strtobool(n.sf_is_single__c.cdata))

        # Size
        d['size'] = int(float(n.sf_BS_Size__c.cdata)) if hasattr(n, 'sf_BS_Size__c') else None

        # Size Range
        d['size_range'] = n.sf_Size_Range__c.cdata if hasattr(n, 'sf_Size_Range__c') else None

        # Scope
        d['scope'] = int(float(n.sf_BS_Scope__c.cdata)) if hasattr(n, 'sf_BS_Scope__c') else None

        # Scope Range
        d['scope_range'] = n.sf_Scope_Range__c.cdata if hasattr(n, 'sf_Scope_Range__c') else None

        # Tree Sort
        d['tree_sort'] = int(float(n.sf_Tree_Sort__c.cdata)) if hasattr(n, 'sf_Tree_Sort__c') else None

        # Session ID
        if hasattr(n, 'sf_BS_Session_UUID__c'):
            d['session_id'] = n.sf_BS_Session_UUID__c.cdata

        # Return parsed dict
        return d

class SfAssignment:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Kind
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kind'] = int(float(n.sf_BS_Kind__c.cdata))

        # Category
        if hasattr(n, 'sf_BS_Category__c'):
            d['kind'] = int(float(n.sf_BS_Category__c.cdata))

        # Person ID
        if hasattr(n, 'sf_BS_Contact_UUID__c'):
            d['person_id'] = n.sf_BS_Contact_UUID__c.cdata

        # Name
        d['name'] = n.sf_Name__c.cdata if hasattr(n, 'sf_Name__c') else None

        # First Name
        d['first_name'] = n.sf_FirstName__c.cdata if hasattr(n, 'sf_FirstName__c') else None

        # Last Name
        d['last_name'] = n.sf_LastName__c.cdata if hasattr(n, 'sf_LastName__c') else None
        
        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Area
        if hasattr(n, 'sf_Area__c'):
            d['area'] = n.sf_Area__c.cdata

        # Email
        d['email'] = n.sf_HomeEmail__c.cdata if hasattr(n, 'sf_HomeEmail__c') else None

        # Cell Phone
        d['cell_phone'] = n.sf_MobilePhone__c.cdata if hasattr(n, 'sf_MobilePhone__c') else None

        # Airports
        d['airports'] = n.sf_Airports__c.cdata if hasattr(n, 'sf_Airports__c') else None

        # BHS ID
        d['bhs_id'] = int(n.sf_cfg_Member_Number__c.cdata) if hasattr(n, 'sf_cfg_Member_Number__c') else None

        # Session ID
        if hasattr(n, 'sf_BS_Session_UUID__c'):
            d['session_id'] = n.sf_BS_Session_UUID__c.cdata

        # Return parsed dict
        return d

class SfEntry:

    def parse_sf_notification(n):
        d = {}

        # Created
        if hasattr(n, 'sf_CreatedDate'):
            d['created'] = n.sf_CreatedDate.cdata

        # Modified
        if hasattr(n, 'sf_LastModifiedDate'):
            d['modified'] = n.sf_LastModifiedDate.cdata

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Status
        if hasattr(n, 'sf_BS_Status__c'):
            d['status'] = int(float(n.sf_BS_Status__c.cdata))

        # Is Evaluation
        if hasattr(n, 'sf_is_evaluation__c'):
            d['is_evaluation'] = bool(strtobool(n.sf_is_evaluation__c.cdata))

        # Is Private
        if hasattr(n, 'sf_is_private__c'):
            d['is_private'] = bool(strtobool(n.sf_is_private__c.cdata))

        # Is MT
        if hasattr(n, 'sf_is_mt__c'):
            d['is_mt'] = bool(strtobool(n.sf_is_mt__c.cdata))

        # Is Senior
        if hasattr(n, 'sf_is_senior__c'):
            d['is_senior'] = bool(strtobool(n.sf_is_senior__c.cdata))

        # Is Youth
        if hasattr(n, 'sf_is_youth__c'):
            d['is_youth'] = bool(strtobool(n.sf_is_youth__c.cdata))

        # Draw
        d['draw'] = int(float(n.sf_Draw_Order__c.cdata)) if hasattr(n, 'sf_Draw_Order__c') else None

        # Prelim
        d['prelim'] = float(n.sf_Prelim__c.cdata) if hasattr(n, 'sf_Prelim__c') else None

        # Base
        d['base'] = float(n.sf_Base__c.cdata) if hasattr(n, 'sf_Base__c') else None

        # Participants
        d['participants'] = n.sf_Participants__c.cdata if hasattr(n, 'sf_Participants__c') else ""

        # POS
        d['pos'] = int(float(n.sf_Persons_On_Stage__c.cdata)) if hasattr(n, 'sf_Persons_On_Stage__c') else None

        # Area
        if hasattr(n, 'sf_Organization__c'):
            d['area'] = n.sf_Organization__c.cdata

        # Chapters
        d['chapters'] = n.sf_Chapters__c.cdata if hasattr(n, 'sf_Chapters__c') else ""

        # Description
        d['description'] = n.sf_Description__c.cdata if hasattr(n, 'sf_Description__c') else ""

        # Notes
        d['notes'] = n.sf_Notes__c.cdata if hasattr(n, 'sf_Notes__c') else ""

        # Group ID
        if hasattr(n, 'sf_BS_Account_UUID__c'):
            d['group_id'] = n.sf_BS_Account_UUID__c.cdata

        # Name
        if hasattr(n, 'sf_Name'):
            d['name'] = n.sf_Name.cdata

        # Kind
        if hasattr(n, 'sf_BS_Kind__c'):
            d['kind'] = int(float(n.sf_BS_Kind__c.cdata))

        # Gender
        if hasattr(n, 'sf_BS_Classification__c'):
            d['gender'] = int(float(n.sf_BS_Classification__c.cdata))

        # District
        if hasattr(n, 'sf_BS_District__c'):
            d['district'] = int(float(n.sf_BS_District__c.cdata))

        # Divisions
        d['division'] = int(float(n.sf_BS_Division__c.cdata)) if hasattr(n, 'sf_BS_Division__c') else None

        if hasattr(n, 'sf_cfg_Member_Id__c'):
            if (n.sf_cfg_Member_Id__c.cdata.isdigit()):
                # BHS ID
                d['bhs_id'] = int(n.sf_cfg_Member_Id__c.cdata)
            else:
                # code
                d['code'] = n.sf_cfg_Member_Id__c.cdata

        # Session ID
        if hasattr(n, 'sf_BS_Session_UUID__c'):
            d['session_id'] = n.sf_BS_Session_UUID__c.cdata

        # Return parsed dict
        return d

class SfEntryContest:

    def parse_sf_notification(n):
        d = {}

        # Contest UUID
        if hasattr(n, 'sf_BS_Contest_UUID__c'):
            d['contest_id'] = n.sf_BS_Contest_UUID__c.cdata

        # Entry UUID
        if hasattr(n, 'sf_BS_Entry_UUID__c'):
            d['entry_id'] = n.sf_BS_Entry_UUID__c.cdata

        # Is Deleted
        if hasattr(n, 'sf_IsDeleted'):
            d['deleted'] = bool(strtobool(n.sf_IsDeleted.cdata))

        # Return parsed dict
        return d

class SfGroupChart:

    def parse_sf_notification(n):
        d = {}

        # Group UUID
        if hasattr(n, 'sf_BS_Account_UUID__c'):
            d['group_id'] = n.sf_BS_Account_UUID__c.cdata

        # Chart UUID
        if hasattr(n, 'sf_BS_Chart_UUID__c'):
            d['chart_id'] = n.sf_BS_Chart_UUID__c.cdata

        # Is Deleted
        if hasattr(n, 'sf_IsDeleted'):
            d['deleted'] = bool(strtobool(n.sf_IsDeleted.cdata))

        # Return parsed dict
        return d
