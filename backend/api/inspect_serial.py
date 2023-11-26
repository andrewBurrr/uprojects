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
        # print(str(func.__name__) + " Flag raised\n")
        return False

def main():
    flags = []
    for serializer in serializers:
        if( not serial_funky(serializer)):
            flags.append(serializer)
            
    print("===========================================\n\n")
    print("Check the following serializers for issues:\n")
    flag_string =""
    for flag in flags:
        flag_string += "\t"+ str(flag.__name__) + "\n"
    print(flag_string)

    # serial_funky(OwnerSerializer)
    # serial_funky(TagSerializer)
    # serial_funky(UserSerializer)
    # serial_funky(AdminSerializer)
    # serial_funky(OrganizationSerializer)
    # serial_funky(BugReportSerializer)


    # serial_funky(RespondSerializer)
    # serial_funky(TeamSerializer)
    # serial_funky(TeamPermissionSerializer)
    # serial_funky(MemberSerializer)
    # serial_funky(ProjectSerializer)
    # serial_funky(EventSerializer)
    # serial_funky(HostsSerializer)
    # serial_funky(DropboxSubmissionSerializer)
    # serial_funky(SubmissionFileSerializer)
    # serial_funky(PartOfSerializer)
    # serial_funky(RepositorySerializer)
    # serial_funky(IssueSerializer)
    # serial_funky(PullRequestSerializer)
    # serial_funky(CommitSerializer)
    # serial_funky(CodeReviewSerializer)


    # serial_funky(UserFollowSerializer)
    # serial_funky(OwnerSerializer)


   


