PLATFORMS = ["netflix", "hotstar", "prime"]


def getOtherPlatforms(lis):
    return [i for i in PLATFORMS if i not in lis]