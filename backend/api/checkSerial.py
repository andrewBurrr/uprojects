from api.serializers import *
from api import serializers as ser


serials = [OwnerSerializer, TagSerializer,UserSerializer, AdminSerializer,
    OrganizationSerializer, BugReportSerializer, RespondSerializer, TeamSerializer, 
    TeamPermissionSerializer, MemberSerializer, ProjectSerializer, EventSerializer, 
    HostsSerializer, DropboxSubmissionSerializer, SubmissionFileSerializer,
    PartOfSerializer, RepositorySerializer, IssueSerializer, PullRequestSerializer,
    CommitSerializer, CodeReviewSerializer, UserFollowSerializer, OwnSerializer,
    ]


def serial_funky(func):
    """
    True or false function to help compile a list of troublesome Serializers.
    """
    serializer = func()
    try:
        print(repr(serializer) + "\n")
        return True

    except:
        return False


def test_func(func):
    """
    Test Function to inspect the serializers and print out their relations.
    """
    serializer = func()
    print(repr(serializer)+"\n")


def main():
    flags = []
    serial_list = []
    print("###########################################\n")
    for serializer in serials:
        serial_list.append( str(serializer.__name__))
        if(serial_funky(serializer)):
            print("===========================================\n")
        else:
            flags.append(serializer)
        

    print("*******************************************")
    print("Check the following serializers for issues:\n")
    flag_string =""
    for flag in flags:
        flag_string += "\t"+ str(flag.__name__) + "\n"
    print(flag_string)
    print("*******************************************\n")

    funcs = dir(ser)
    func2 = []
    for func in funcs:
        if (func.endswith("Serializer")):
            func2.append(func)

    for k in serial_list:
        func2.remove(k)

    print("missing in checkSerial **Please add to the serial_list**: \n")
    for serial in func2:
        print(serial + "\n")


def serializers_printout():
    """
    KW was trying to get this to automatically compile a list of functions in api.serializers
    that end with 'Serializer'. This prints off the list of functions but I don't
    know how to get this to call the functions... --\_(-_-)_/--
    """
    funcs = dir(ser)
    func2 = []
    for func in funcs:
        if (func.endswith("Serializer")):
            func2.append(func)

    for serial in func2:
        print(serial + "\n")