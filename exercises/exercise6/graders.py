# -*- coding: utf-8 -*-

import re, sys, gnupg
from exercises.registry import register_grader

gpg = gnupg.GPG()

def print_info(decrypted):
    print('User name: %s' % decrypted.username)
    print('Key id: %s' % decrypted.key_id)
    print('Signature id: %s' % decrypted.signature_id)
    print('Signature timestamp: %s' % decrypted.sig_timestamp)
    print('Fingerprint: %s' % decrypted.fingerprint)

def hasStudentEmail(verified, student_email):
    emailList = re.findall(r"(?<=\<).+(?=\>)", str(verified.username))
    return student_email in emailList

# Assumes lookupMIT works, otherwise I can't fetch the pub key
def hasAtLeastOneSignature(verified):
    result = gpg.recv_keys('pgp.mit.edu', verified.key_id)
    return result.n_sigs > 0

# Assumes lookupMIT works, otherwise I can't fetch the pub key
def hasExpirationDate(verified):
    result = gpg.search_keys(verified.key_id, 'pgp.mit.edu')
    return len(result) > 0 and len(result[0]['expires']) > 0

# Assumes lookupMIT works, otherwise I can't fetch the pub key
def has4096Length(verified):
    result = gpg.search_keys(verified.key_id, 'pgp.mit.edu')
    return len(result) > 0 and result[0]['length'] == '4096'

# Looks up the key id in pgp.mit.edu
def lookupMIT(verified):
    result = gpg.search_keys(verified.key_id, 'pgp.mit.edu')
    return len(result) > 0

# Assumes lookupMIT works, otherwise I can't fetch the pub key
def importKeyFromData(signed_data):
    verified = gpg.verify(signed_data)
    result = gpg.recv_keys(verified.key_id, 'pgp.mit.edu')
    return

def validate(metadata, signed_data):
    #importKeyFromData(signed_data)
    verified = gpg.verify(signed_data)

    # Check is msg was signed. If not, there's no point to continue
    if not verified.key_id:
        return False, u'Το κείμενο δεν ειναι υπογεγραμμένο με έγκυρο GPG κλειδί.'

    lookedup = lookupMIT(verified)
    if not lookedup:
        return False, u'Το κλειδί σου δεν βρέθηκε στον MIT keyserver. Παρακαλούμε ανέβασε το κλειδί σου και ξαναπροσπάθησε.'

    hasEmail = hasStudentEmail(verified, metadata['user_email'])
    if not hasEmail:
        return False, u'Το κλειδί που βρέθηκε στον MIT keyserver (%s) δεν ειναι το ίδιο με το email σου (%s).' % (
                            verified.username,
                            metadata['user_email'],
                            )

    oneSignature = hasAtLeastOneSignature(verified)
    if not oneSignature:
        return False, u'Το κλειδί σου δεν έχει λάβει καμία υπογραφή. Λάβε μια υπογραφή, απο εναν συμφοιτητή σου, και ξαναπροσπάθησε.'

    hasExpiration = hasExpirationDate(verified)
    if not hasExpiration:
        return False, u'Στο κλειδί σου δεν έχει οριστεί ημερομηνία λήξης. Παρακαλούμε ξαναδημιούργησε το κλειδί σου και ξαναπροσπάθησε.'

    has4096 = has4096Length(verified)
    if not has4096:
        return False, u'Το κλειδί σου δεν έχει μήκος 4096 bits. Παρακαλούμε ξαναδημιούργησε το κλειδί σου και ξαναπροσπάθησε.'

    # Solution is correct!
    return True

register_grader('20.1', validate)