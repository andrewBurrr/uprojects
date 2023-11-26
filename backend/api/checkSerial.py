from api.serializers import *


serializers = [OwnerSerializer, TagSerializer,UserSerializer, AdminSerializer,
    OrganizationSerializer, BugReportSerializer, RespondSerializer, TeamSerializer, 
    TeamPermissionSerializer, MemberSerializer, ProjectSerializer, EventSerializer, 
    HostsSerializer, DropboxSubmissionSerializer, SubmissionFileSerializer,
    PartOfSerializer, RepositorySerializer, IssueSerializer, PullRequestSerializer,
    CommitSerializer, CodeReviewSerializer, UserFollowSerializer, OwnerSerializer,
    ]

def serial_funky(func):
    serializer = func()
    try:
        print(repr(serializer) + "\n")
        return True

    except:
        return False
    
def test_func(func):
    serializer = func()
    print(repr(serializer)+"\n")

def main():
    flags = []
    print("###########################################\n")
    for serializer in serializers:
        
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


main()


