from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
# import ssl, Tls
import re, io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User

from baseInfo.models import Employee
 


# Check user authentication in the LDAP and return his information
def get_LDAP_user(username, password):
    try:
        LDAP_URL = 'dc.asft.co:389'
        domain_user = 'asft\\' + username
        # tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1)
        # server = Server(LDAP_URL, use_ssl=True, tls=tls_configuration)
        server = Server(LDAP_URL, get_info=ALL)
        conn = Connection(server, user=domain_user, password=password, authentication=NTLM, auto_bind=True)

        base = '''dc=asft,dc=co'''
        criteria = '(&(objectCategory=user)(sAMAccountName='+ username+'))'
        attributes = ['sAMAccountName', 'givenName', 'sn', 'mail', 'userAccountControl', 'thumbnailPhoto']
        conn.search(base, criteria, attributes=attributes)
        # conn.search(search_base='dc=asft,dc=co', search_filter=f'(sAMAccountName={username})',search_scope=SUBTREE, attributes=['sAMAccountName'])

        username = ''
        if len(conn.response) != 0:
            sync_LDAP_user(conn.response[0])
            username = str(conn.response[0]['attributes']["sAMAccountName"])
        return username
    except:
        check_user_activity(username)
        return 'unauthenticated'


def check_user_activity(username):
    try:
        domain_user = 'asft\\portal'
        password = 'Ccontrol'
        LDAP_URL = 'dc.asft.co:389'
        # tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1)
        # server = Server(LDAP_URL, use_ssl=True, tls=tls_configuration)
        server = Server(LDAP_URL, get_info=ALL)
        conn = Connection(server, user=domain_user, password=password, authentication=NTLM, auto_bind=True)

        base = '''dc=asft,dc=co'''
        criteria = '(&(objectCategory=user)(sAMAccountName='+ username+'))'
        attributes = ['sAMAccountName', 'givenName', 'sn', 'mail', 'userAccountControl']
        conn.search(base, criteria, attributes=attributes)

        if len(conn.response) != 0:
            sync_LDAP_user(conn.response[0])
            return True
        else:
            return False     
    except:
        return False    


def sync_LDAP_user(entity):
    pattern = re.compile(r'^[a-z|A-Z]+\.[a-z|A-Z|\s]+$')
    # if(pattern.match(str(entity['sAMAccountName']))):
    #     username = entity['sAMAccountName'] # returns bytes by default so we need to decode to string. ou=All Clients,
    #     first_name = entity['givenName']
    #     last_name = entity['sn']
    #     email = entity['mail']
    #     thumbnailPhoto = entity['thumbnailPhoto']

    if('attributes' in entity and pattern.match(str(entity['attributes']['sAMAccountName']))):
        username = entity['attributes']['sAMAccountName']
        first_name = entity['attributes']['givenName']
        last_name = entity['attributes']['sn']
        email = entity['attributes']['mail']
        thumbnailPhoto = entity['attributes']['thumbnailPhoto']

        is_active = 0 if(entity['attributes']['userAccountControl'] == 66050 or entity['attributes']['userAccountControl'] == 514) else 1
        try:
            image_name = '/files/employee_pix/{0}.jpg'.format(username)
            # Update the user -- this allows for name changes etc, using username as the key.
            user, user_created = User.objects.update_or_create(username=username, 
                defaults={'email': email, 'first_name': first_name, 'last_name': last_name, 'is_active': is_active})

            if user_created:
                # Set an unusable password -- django-auth-ldap handles this, anyway.   'user_id':user.id, 
                user.set_unusable_password()
                user.save()
                # first_name__exact=first_name, last_name__exact=last_name      , picture=thumbnailPhoto
                
            employees = Employee.objects.filter(user_id__exact=user.id)
            if(len(employees) == 0):
                employee = Employee.objects.create(first_name=first_name, last_name=last_name, email=email, user_id=user.id, gender=False)     
                if(len(thumbnailPhoto)>0):
                    buffer = io.BytesIO()
                    buffer.write(thumbnailPhoto)
                    image_file = InMemoryUploadedFile(buffer, None, '{0}.jpg'.format(username), 'image/jpg', buffer.getbuffer().nbytes, None)
                    employee.picture.save(image_name, image_file)   
            else:
                if(len(employees) > 1):
                    employees[1].delete()
                if((employees[0].picture == None or employees[0].picture == []) and len(thumbnailPhoto)>0):
                    buffer = io.BytesIO()
                    buffer.write(thumbnailPhoto)
                    image_file = InMemoryUploadedFile(buffer, None, '{0}.jpg'.format(username), 'image/jpg', buffer.getbuffer().nbytes, None)
                    employees[0].picture.save(image_name, image_file)   

        except Exception as e:
            return 'sync exception'


def sync_LDAP_users(username, password):
    try:
        LDAP_URL = 'dc.asft.co:389'
        domain_user = 'asft\\' + username
        # tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1)
        # server = Server(LDAP_URL, use_ssl=True, tls=tls_configuration)
        server = Server(LDAP_URL, get_info=ALL)
        conn = Connection(server, user=domain_user, password=password, authentication=NTLM, auto_bind=True)

        base = '''dc=asft,dc=co'''
        criteria = '''(objectCategory=user)'''
        attributes = ['sAMAccountName', 'givenName', 'sn', 'mail', 'userAccountControl', 'thumbnailPhoto']

        conn.search(base, criteria, attributes=attributes)
        entries = conn.entries

        for e in entries:
            pattern = re.compile(r'^[a-z|A-Z]+\.[a-z|A-Z|\s]+$')
            if(pattern.match(str(e['sAMAccountName']))):
                username = e['sAMAccountName'] # returns bytes by default so we need to decode to string. ou=All Clients,
                first_name = e['givenName']
                last_name = e['sn']
                email = e['mail']
                thumbnailPhoto = e['thumbnailPhoto']
                is_active = 0 if(e['userAccountControl'] == 66050 or e['userAccountControl'] == 514) else 1
                try:
                    image_name = '/employee_pix/{0}.jpg'.format(username)
                    # Update the user -- this allows for name changes etc, using username as the key.
                    user, user_created = User.objects.update_or_create(username=username, defaults={'email': email, 'first_name': first_name, 'last_name': last_name, 'is_active': is_active})

                    if user_created:
                        # Set an unusable password -- django-auth-ldap handles this, anyway.   'user_id':user.id, 
                        user.set_unusable_password()
                        user.save()
                        # first_name__exact=first_name, last_name__exact=last_name
                    employees = Employee.objects.filter(user_id__exact=user.id)
                    if(len(employees) == 0):
                        employee = Employee.objects.create(first_name=first_name, last_name=last_name, email=email, user_id=user.id, gender=False)     
                        if(len(thumbnailPhoto)>0):
                            buffer = io.BytesIO()
                            buffer.write(thumbnailPhoto)
                            image_file = InMemoryUploadedFile(buffer, None, '{0}.jpg'.format(username), 'image/jpg', buffer.getbuffer().nbytes, None)
                            employee.picture.save(image_name, image_file)   
                   
                except Exception as e:
                    return 'sync exception'

        return 'done successfully'
    except:
        return 'unauthenticated'


def sync_LDAP_users_Ex(username, password):
    try:
        LDAP_URL = 'dc.asft.co:389'
        username = 'portal'
        password = 'Ccontrol'
        domain_user = 'asft\\' + username

        server = Server(LDAP_URL, get_info=ALL)
        conn = Connection(server, user=domain_user, password=password, authentication=NTLM, auto_bind=True)

        base = '''dc=asft,dc=co'''
        criteria = '''(objectCategory=user)'''
        attributes = ['sAMAccountName', 'givenName', 'sn', 'mail', 'userAccountControl', 'thumbnailPhoto']

        conn.search(base, criteria, attributes=attributes)
        results = conn.response

        for r in results:   
            pattern = re.compile(r'^[a-z|A-Z]+\.[a-z|A-Z|\s]+$')
            if('attributes' in r and pattern.match(str(r['attributes']['sAMAccountName']))):
                username = r['attributes']['sAMAccountName']
                first_name = r['attributes']['givenName']
                last_name = r['attributes']['sn']
                email = r['attributes']['mail']
                thumbnail = r['attributes']['thumbnailPhoto']

                is_active = 0 if(r['attributes']['userAccountControl'] == 66050 or r['attributes']['userAccountControl'] == 514) else 1
                try:                
                    image_name = '/employee_pix/{0}.jpg'.format(username)
                    
                    user, user_created = User.objects.update_or_create(username=username, defaults={'email': email, 'first_name': first_name, 'last_name': last_name, 'is_active': is_active})
                    if user_created:
                        # Set an unusable password -- django-auth-ldap handles this, anyway.  'user_id':user.id, 
                        user.set_unusable_password()
                        user.save()
                        # first_name__exact=first_name, last_name__exact=last_name
                    employees = Employee.objects.filter(user_id__exact=user.id)
                    if(len(employees) == 0):
                        employee = Employee.objects.create(first_name=first_name, last_name=last_name, picture=image_name, email=email, user_id=user.id, gender=False)
                        if(len(thumbnail)>0):
                            buffer = io.BytesIO()
                            buffer.write(thumbnail)
                            image_file = InMemoryUploadedFile(buffer, None, '{0}.jpg'.format(username), 'image/jpg', buffer.getbuffer().nbytes, None)
                            employee.picture.save(image_name, image_file)   
                except Exception as e:
                    return 'sync exception'                                
        return 'done successfully'
    except:
        return 'unauthenticated'                                    