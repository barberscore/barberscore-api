
# Third-Party
from model_utils import Choices
from distutils.util import strtobool

# Local
from apps.registration.models import Contest, Session

class SfSession:

    # DIVISION = Choices(
    #     ('EVG', [
    #         (10, 'evgd1', 'EVG Division I'),
    #         (20, 'evgd2', 'EVG Division II'),
    #         (30, 'evgd3', 'EVG Division III'),
    #         (40, 'evgd4', 'EVG Division IV'),
    #         (50, 'evgd5', 'EVG Division V'),
    #     ]),
    #     ('FWD', [
    #         (60, 'fwdaz', 'FWD Arizona'),
    #         (70, 'fwdne', 'FWD Northeast'),
    #         (80, 'fwdnw', 'FWD Northwest'),
    #         (90, 'fwdse', 'FWD Southeast'),
    #         (100, 'fwdsw', 'FWD Southwest'),
    #     ]),
    #     ('LOL', [
    #         (110, 'lol10l', 'LOL 10000 Lakes'),
    #         (120, 'lolone', 'LOL Division One'),
    #         (130, 'lolnp', 'LOL Northern Plains'),
    #         (140, 'lolpkr', 'LOL Packerland'),
    #         (150, 'lolsw', 'LOL Southwest'),
    #     ]),
    #     ('MAD', [
    #         # (160, 'madatl', 'MAD Atlantic'),
    #         (170, 'madcen', 'MAD Central'),
    #         (180, 'madnth', 'MAD Northern'),
    #         (190, 'madsth', 'MAD Southern'),
    #         # (200, 'madwst', 'MAD Western'),
    #     ]),
    #     ('NED', [
    #         (210, 'nedgp', 'NED Granite and Pine'),
    #         (220, 'nedmtn', 'NED Mountain'),
    #         (230, 'nedpat', 'NED Patriot'),
    #         (240, 'nedsun', 'NED Sunrise'),
    #         (250, 'nedyke', 'NED Yankee'),
    #     ]),
    #     ('SWD', [
    #         (260, 'swdne', 'SWD Northeast'),
    #         (270, 'swdnw', 'SWD Northwest'),
    #         (280, 'swdse', 'SWD Southeast'),
    #         (290, 'swdsw', 'SWD Southwest'),
    #     ]),
    # )

    def parse_sf_notification(n):
        d = {}

        # UUID
        if hasattr(n, 'sf_BS_UUID__c'):
            d['id'] = n.sf_BS_UUID__c.cdata

        # Close Date
        if hasattr(n, 'sf_Close_Date__c'):
            d['close_date'] = n.sf_Close_Date__c.cdata

        # Convention ID -- Currently a Salesforce ID, could be a BS UUID?
        # if hasattr(n, 'sf_Convention__c'):
        #     d['convention_id'] = n.sf_Convention__c.cdata

        # District
        if hasattr(n, 'sf_District__c'):
            DISTRICT_D = dict((v,k) for k,v in Session.DISTRICT)
            d['district'] = DISTRICT_D[n.sf_District__c.cdata]

        # End Date
        if hasattr(n, 'sf_End_Date__c'):
            d['end_date'] = n.sf_End_Date__c.cdata

        # Kind
        if hasattr(n, 'sf_Kind__c'):
            KIND_D = dict((v,k) for k,v in Session.KIND)
            d['kind'] = KIND_D[n.sf_Kind__c.cdata]

        # Location
        if hasattr(n, 'sf_Location__c'):
            d['location'] = n.sf_Location__c.cdata

        # Num Rounds
        if hasattr(n, 'sf_Num_rounds__c'):
            d['num_rounds'] = int(float(n.sf_Num_rounds__c.cdata))

        # Open Date
        if hasattr(n, 'sf_Open_Date__c'):
            d['open_date'] = n.sf_Open_Date__c.cdata

        # Panel
        if hasattr(n, 'sf_Panel__c'):
            PANEL_D = dict((v,k) for k,v in Session.PANEL)
            d['panel'] = PANEL_D[n.sf_Panel__c.cdata]

        # Season
        if hasattr(n, 'sf_Season__c'):
            SEASON_D = dict((v,k) for k,v in Session.SEASON)
            d['season'] = SEASON_D[n.sf_Season__c.cdata]

        # Start Date
        if hasattr(n, 'sf_Start_Date__c'):
            d['start_date'] = n.sf_Start_Date__c.cdata

        # Status
        if hasattr(n, 'sf_Status__c'):
            STATUS_D = dict((v,k) for k,v in Session.STATUS)
            d['status'] = STATUS_D[n.sf_Status__c.cdata]

        # Time Zone
        if hasattr(n, 'sf_Time_Zone__c'):
            d['timezone'] = n.sf_Time_Zone__c.cdata

        # Venue
        if hasattr(n, 'sf_Venue__c'):
            d['venue_name'] = n.sf_Venue__c.cdata

        # Year
        if hasattr(n, 'sf_Year__c'):
            d['year'] = n.sf_Year__c.cdata

        # Is Invitational
        if hasattr(n, 'sf_is_invitational__c'):
            d['is_invitational'] = bool(strtobool(n.sf_is_invitational__c.cdata))

        # Description
        if hasattr(n, 'sf_Description__c'):
            d['description'] = n.sf_Description__c.cdata

        # Notes
        if hasattr(n, 'sf_Notes__c'):
            d['notes'] = n.sf_Notes__c.cdata

        # Footnotes
        if hasattr(n, 'sf_Footnotes__c'):
            d['footnotes'] = n.sf_Footnotes__c.cdata

        # Name
        if hasattr(n, 'sf_Name__c'):
            d['name'] = n.sf_Name__c.cdata

        # Divisions
        if hasattr(n, 'sf_Divisions__c'):
            d['divisions'] = n.sf_Divisions__c.cdata

        # Return parsed dict
        return d
