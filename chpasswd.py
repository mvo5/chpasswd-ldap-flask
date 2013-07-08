#!/usr/bin/python

import getpass
import sys

import ldap
import ldap.modlist

if __name__ == "__main__":
    server = sys.argv[1]
    user = sys.argv[2]
    
    # or simply: 
    # res = subprocess.Popen(["smbpasswd", "-r", server, "-U", user],
    #                        stdin=subprocess.PIPE)

    l = ldap.initialize("ldaps://%s" % server)
    l.set_option(ldap.OPT_REFERRALS, 0)
    #l.start_tls_s()
    passw = getpass.getpass("Enter current password: ")
    res = l.simple_bind_s(user, passw)
    passwd_new1 = getpass.getpass("Enter new pw: ")
    passwd_new2 = getpass.getpass("Enter new pw (again): ")
    if passwd_new1 != passwd_new2:
        print "pw does not match"
        sys.exit(1)
    encoded_old = ('"%s"' % passw).encode("utf-16-le")
    encoded_new = ('"%s"' % passwd_new1).encode("utf-16-le")
    ldif = [
        (ldap.MOD_DELETE, 'unicodePwd', [encoded_old]),
        (ldap.MOD_ADD, 'unicodePwd', [encoded_new])]
    dn="CN=%s,cn=Users,dc=uni-trier,dc=de" % user.split("@")[0]
    res = l.modify_s(dn, ldif)

    # error
    if not res:
        sys.exit(1)

