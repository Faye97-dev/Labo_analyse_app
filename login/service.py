def check_user_group(request , all_grp):
    for name in all_grp:
        if request.user.groups.filter(name=name).exists() :
            return name
    return None

def first_link(role,pdf):
    if role == "Admin":
        if pdf:
            return 'analyse' 
        else :
            return 'dashboard'
    else:
        return 'analyse'
        
'''
def first_link(role,pdf,id=None):
    if role == "Admin":
        if pdf:
            return ['analyse' ,True]
        else :
            return ['dashboard',True]
    elif role == "Doctor" :
        return ['analyse/medecin/'+str(id),False]
    else:
        return ['analyse/patient/'+str(id),False]
'''