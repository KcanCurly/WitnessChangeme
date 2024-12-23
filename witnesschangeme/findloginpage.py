def find_login(response):
    if "SAS Web Application Server" in response:
        return "/SASLogon/login"
    if "URL='/ui'" in response:
        return "/ui/#/login"
    return None