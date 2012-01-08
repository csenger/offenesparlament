#coding: utf-8
from lxml import etree

import sqlaload as sl

from offenesparlament.core import etl_engine
from offenesparlament.core import master_data
from offenesparlament.transform.namematch import match_speaker, make_prints

FEED_URL = "http://www.abgeordnetenwatch.de/koop/feeds/index.php?account=60e4a1f4fac1801c6486e85f8ed78a06&feed=3f39181c64fa435556f3ce86c24cd118"

PARTEI_MAPPING = {
    'CDU': 'CDU/CSU',
    'CSU': 'CDU/CSU',
    u'GRÜNE': u'B90/DIE GRÜNEN',
    'DIE LINKE': 'DIE LINKE.'
    }

def load_profiles(engine, master):
    prints = make_prints(engine)
    doc = etree.parse(FEED_URL)
    Person = sl.get_table(engine, 'person')
    for profile in doc.findall('//PROFIL'):
        name = profile.findtext('.//VORNAME')
        name += ' ' + profile.findtext('.//NACHNAME')
        partei = profile.findtext('.//PARTEI')
        name += ' ' + PARTEI_MAPPING.get(partei, partei)
        print profile.get('url')
        try:
            fp = match_speaker(master, name, prints)
            if fp:
                sl.upsert(engine, Person, 
                          {'awatch_url': profile.get('url'),
                           'fingerprint': fp}, 
                        unique=['fingerprint'])
        except ValueError:
            pass

if __name__ == '__main__':
    engine = etl_engine()
    print "DESTINATION", engine
    load_profiles(engine, master_data())


