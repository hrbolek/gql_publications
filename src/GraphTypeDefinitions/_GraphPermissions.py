import logging
from sqlalchemy.future import select
import strawberry
from typing import List, Any
from uuid import UUID
from functools import cached_property

import os

isDEMO = os.environ.get("DEMO", "True")

# def AsyncSessionFromInfo(info):
#     return info.context["session"]


# def UserFromInfo(info):
    # return info.context["user"]

"""
query ($id: ID!) {
  rolesOnUser(userId: $id) {
    ...role
  }
  rolesOnGroup(groupId: $id) {
    ...role
  }
}

fragment role on RoleGQLModel {
  valid
  roletype { id}
  user { id }
  group { id }
}
"""


class BasePermission(strawberry.permission.BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        raise NotImplemented()
        # print("BasePermission", source)
        # print("BasePermission", self)
        # print("BasePermission", kwargs)
        # return True





from functools import cache
import aiohttp


rolelist = [
        {
            "name": "já",
            "name_en": "myself",
            "id": "05a3e0f5-f71e-4caa-8012-229d868aa8ca",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "administrátor",
            "name_en": "administrator",
            "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
            "category_id": "774690a0-56b3-45d9-9887-0989ed3de4c0"
        },
        {
            "name": "zpracovatel gdpr",
            "name_en": "gdpr user",
            "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
            "category_id": "774690a0-56b3-45d9-9887-0989ed3de4c0"
        },
        {
            "name": "rektor",
            "name_en": "rector",
            "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "prorektor",
            "name_en": "vicerector",
            "id": "ae3f2886-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "děkan",
            "name_en": "dean",
            "id": "ae3f2912-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "proděkan",
            "name_en": "vicedean",
            "id": "ae3f2980-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "vedoucí katedry",
            "name_en": "head of department",
            "id": "ae3f29ee-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "vedoucí učitel",
            "name_en": "leading teacher",
            "id": "ae3f2a5c-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "garant",
            "name_en": "grant",
            "id": "5f0c247e-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "garant (zástupce)",
            "name_en": "grant (deputy)",
            "id": "5f0c2532-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "garant předmětu",
            "name_en": "subject's grant",
            "id": "5f0c255a-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "přednášející",
            "name_en": "lecturer",
            "id": "5f0c2578-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "cvičící",
            "name_en": "trainer",
            "id": "5f0c2596-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        }
    ]

# async def getRoles(userId="", roleUrlEndpoint="http://localhost:8088/gql/", isDEMO=True):
#     query = """query($userid: UUID!){
#             roles: roleByUser(userId: $userid) {
#                 id
#                 valid
#                 roletype { id }
#                 group { id }
#                 user { id }
#             }
#         }
# """
#     variables = {"userid": userId}
#     headers = {}
#     json = {
#         "query": query,
#         "variables": variables
#     }

#     print("roleUrlEndpoint", roleUrlEndpoint)
#     async with aiohttp.ClientSession() as session:
#         print(f"query {roleUrlEndpoint} for json={json}")
#         async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
#             print(resp.status)
#             if resp.status != 200:
#                 text = await resp.text()
#                 print(text)
#                 return []
#             else:
#                 respJson = await resp.json()

#     print(respJson)
    
#     assert respJson.get("errors", None) is None
#     respdata = respJson.get("data", None)
#     assert respdata is not None
#     roles = respdata.get("roles", None)
#     assert roles is not None
#     print("roles", roles)
#     return [*roles]

#     pass

import requests
# from src.utils.gql_ug_proxy import createProxy

def ReadAllRoles():
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    gqlproxy = createProxy(GQLUG_ENDPOINT_URL)

    query = """query {roleTypePage(limit: 1000) {id, name, nameEn}}"""
    variables = {}

    respJson = gqlproxy.post(query=query, variables=variables)
    assert respJson.get("errors", None) is None, respJson["errors"]
    respdata = respJson.get("data", None)
    assert respdata is not None, "during roles reading roles have not been readed"
    roles = respdata.get("roles", None)
    assert roles is not None, "during roles reading roles have not been readed"
    print("roles", roles)
    roles = list(map(lambda item: {**item, "nameEn": item["name_ne"]}, roles))
    return [*roles]

if not isDEMO:
    rolelist = ReadAllRoles()
    print("rolelist", rolelist)

roleIndex = { role["name_en"]: role["id"] for role in rolelist }

# async def ReadRoles(
#     userId="2d9dc5ca-a4a2-11ed-b9df-0242ac120003", 
#     roleUrlEndpoint="http://localhost:8088/gql/",
#     demo=True):
    
#     query = """query($userid: UUID!){
#             roles: roleByUser(userId: $userid) {
#                 id
#                 valid
#                 roletype { id }
#                 group { id }
#                 user { id }
#             }
#         }
# """
#     variables = {"userid": userId}
#     headers = {}
#     json = {
#         "query": query,
#         "variables": variables
#     }

#     print("roleUrlEndpoint", roleUrlEndpoint)
#     async with aiohttp.ClientSession() as session:
#         print(f"query {roleUrlEndpoint} for json={json}")
#         async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
#             print(resp.status)
#             if resp.status != 200:
#                 text = await resp.text()
#                 print(text)
#                 return []
#             else:
#                 respJson = await resp.json()

#     print(respJson)
    
#     assert respJson.get("errors", None) is None
#     respdata = respJson.get("data", None)
#     assert respdata is not None
#     roles = respdata.get("roles", None)
#     assert roles is not None
#     print("roles", roles)
#     return [*roles]

# def WhereAuthorized(userRoles, roleIdsNeeded=[]):
    
#     # 👇 filtrace roli, ktere maji pozadovanou uroven autorizace
#     roletypesFiltered = filter(lambda item: item["roletype"]["id"] in roleIdsNeeded, userRoles)
#     # 👇 odvozeni, pro ktere skupiny ma tazatel patricnou uroven autorizace
#     groupsAuthorizedIds = map(lambda item: item["group"]["id"], roletypesFiltered)
#     # 👇 konverze na list
#     groupsAuthorizedIds = list(groupsAuthorizedIds)
#     # cokoliv se tyka techto skupin, na to autor muze
#     print("groupsAuthorizedIds", groupsAuthorizedIds)
#     return groupsAuthorizedIds

@cache
def RolesToList(roles: str = ""):
    roleNames = roles.split(";")
    roleNames = list(map(lambda item: item.strip(), roleNames))
    roleIdsNeeded = list(map(lambda roleName: roleIndex[roleName], roleNames))
    return roleIdsNeeded

# from ._RBACObjectGQLModel import RBACObjectGQLModel

# async def resolveRoles(info, id):
#     return []


from src.Dataloaders import (
    getUserFromInfo
    )

from strawberry.type import StrawberryList
class OnlyForAuthentized(strawberry.permission.BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        if self.isDEMO:
            print("DEMO Enabled, not for production")
            return True
        
        self.defaultResult = [] if info._field.type.__class__ == StrawberryList else None
        user = getUserFromInfo(info)
        return (False if user is None else True)
    
    def on_unauthorized(self):
        return self.defaultResult
        
    @cached_property
    def isDEMO(self):
        DEMO = os.getenv("DEMO", None)
        return DEMO == "True"

# def createRoleGetter():
#     allroles = []
#     from src.Dataloaders import getLoadersFromInfo as getLoader
#     async def getter(info: strawberry.types.Info):
#         async def getAllRoles():
#             loader = getLoader(info).roletypes
#             rows = await loader.page(limit=1000)
#             scalars = rows.scalars()
#             return list(scalars)

#         if len(allroles) == 0:
#             allroles = await getAllRoles()

#         return allroles
#     return getter

# getAllRoles = createRoleGetter()    

class RBACPermission(BasePermission):
    _allRoles = None
    # @classmethod
    # def getAllRoles(cls):
    #     if cls._allRoles is not None:
    #         return cls._allRoles
    #     from ..DBDefinitions import RoleTypeModel, startSyncEngine
    #     statement = select(RoleTypeModel)
    #     sessionMaker = startSyncEngine()
    #     with sessionMaker() as session:
    #         rows = session.execute(statement)
    #         result = [{"id": r.id, "name": r.name, "name_en": r.name_en} for r in rows.scalars()]
    #         cls._allRoles = result
    #     return result

    @classmethod
    async def getAllRoles(cls, info: strawberry.types.Info):
        if cls._allRoles is not None:
            return cls._allRoles
        from ..DBDefinitions import RoleTypeModel, startEngine
        from ..Dataloaders import getLoadersFromInfo
        loader = getLoadersFromInfo(info).RoleTypeModel
        roles = await loader.page(limit=1000)
        
        result = [{"id": r.id, "name": r.name, "name_en": r.name_en} for r in roles]
        assert len(result) > 1, f"are roletypes initialized {result}?"
        cls._allRoles = result

        logging.info(f"loaded all roles {result}")
        return result

    async def getUserRoles(self, info: strawberry.types.Info):
        from .roleGQLModel import RoleGQLModel
        user = getUserFromInfo(info)
        userroles = user.get("roles")
        if userroles is None:
            loader = RoleGQLModel.getLoader(info)
            rolerows = await loader.filter_by(user_id=user["id"])
            rolerows = list(rolerows)

            ur = [
                {
                    "id": rolerow.id,
                    "group_id": rolerow.group_id,
                    "user_id": rolerow.user_id,
                    "roletype_id": rolerow.roletype_id
                } 
                for rolerow in rolerows
            ]
            logging.info(f"user {user['id']} has roles {ur}")
            allRoles = await RBACPermission.getAllRoles(info)
            indexedRoleTypes = {r["id"]: r for r in allRoles}

            userroles = [
                {
                    "id": rolerow.id,
                    "group_id": rolerow.group_id,
                    "user_id": rolerow.user_id,
                    "roletype_id": rolerow.roletype_id,
                    "type": indexedRoleTypes[rolerow.roletype_id]
                } 
                for rolerow in rolerows if indexedRoleTypes.get(rolerow.roletype_id, None) is not None]
            # write back to context and cache it for next use in current request
            logging.info(f"user {user['id']} has roles {userroles}")
            user["roles"] = userroles
        return userroles
        

    async def getRoles_(self, rbacobject: Any, info: strawberry.types.Info): 
        "returns roles related to source"
        from .RBACObjectGQLModel import RBACObjectGQLModel
        # assert hasattr(source, "rbacobject"), f"missing rbacobject on {source}"
        
        # rbacobject = source.rbacobject
        
        #rbacobject
        assert rbacobject is not None, f"RoleBasedPermission cannot be used, rbacobject has None value"
        # rbacobject = "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"

        ## zjistime, jake role jsou vztazeny k rbacobject 
        # print(response)

        authorizedroles = await RBACObjectGQLModel.resolve_roles(info=info, id=rbacobject)           
        return authorizedroles
    
    async def getActiveRoles(self, rbacobject: Any, info: strawberry.types.Info):
        "returns roles related to source which has logged user"
        from .RBACObjectGQLModel import RBACObjectGQLModel
        
        authorizedroles = await RBACObjectGQLModel.resolve_roles(info=info, id=rbacobject)           

        user = getUserFromInfo(info)
        # logging.info(f"RolebasedPermission.authorized user {user}")
        user_id = user["id"]
        usersrole = [r for r in authorizedroles if (r["user_id"] == user_id)]
        return usersrole
    
    async def testIsAdmin(self, info: strawberry.types.Info, adminRoleNames=["administrátor"]):
        assert len(adminRoleNames) > 0, "as adminRoleNames is empty, this always fails"
        userRoles = await self.getUserRoles(info)
        adminRoles = filter(lambda role: role["type"]["name"] in adminRoleNames, userRoles)
        # isAdmin = next(adminRoles, None) is not None
        return next(adminRoles, None)
    
    async def testIsAllowed(self, info: strawberry.types.Info, rbacobject, allowedRolesNames = []):
        assert len(allowedRolesNames) > 0, "as allowedRolesNames is empty, this always fails"
        relatedRoles = await self.getActiveRoles(rbacobject, info)
        allowedRoles = filter(lambda role: role["type"]["name"] in allowedRolesNames, relatedRoles)
        return next(allowedRoles, None)

    async def resolveUserRole(self, info: strawberry.types.Info, rbacobject, adminRoleNames=["administrátor"], allowedRoleNames = []):
        "test if logged user has appropriate global role (without relation to rbacobject) or appropriate role related to rbacobject"
        if len(adminRoleNames) > 0:
            adminRole = await self.testIsAdmin(info, adminRoleNames=adminRoleNames)
            if adminRole: return adminRole
            elif rbacobject is None:
                return None
        
        assert rbacobject is not None, "no admin role defined and rbacobject is None"

        if len(allowedRoleNames) > 0:
            return await self.testIsAllowed(info, rbacobject, allowedRoleNames)
        else:
            assert len(adminRoleNames) > 0, "no admin role defined nor allowedRolesNames defined"
        # self.__class__.__name__
        return None


class OnlyForAdmins(RBACPermission):
    message = "User is not allowed create new role category"
    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        adminRoleNames = ["administrátor"]
        adminrole = await self.testIsAdmin(info, adminRoleNames=adminRoleNames)
        
        if not adminrole: 
            logging.info(f"user has no admin role")
            return False
        return True



class AlwaysFailPermission(RBACPermission):

    async def has_permission(self, source, info: strawberry.types.Info, **kwargs) -> bool:
        self.defaultResult = [] if info._field.type.__class__ == StrawberryList else None
        return False
    
    def on_unauthorized(self) -> None:
        return self.defaultResult


def InsertRBACPermission(roles: str = "", get_rbacobject = None):
    assert get_rbacobject is not None, "missing get_rbacobject"
    roleIdsNeeded = RolesToList(roles)
    class InsertPermission(RBACPermission):
        message = "User has not appropriate roles"

        on_unauthorized = None
        
        async def has_permission(
                self, source: Any, info: strawberry.types.Info, **kwargs: Any
            # self, source, info: strawberry.types.Info, **kwargs
            # self, source, **kwargs
        ) -> bool:
            rbacobject = get_rbacobject(source, info, **kwargs)
            activeRoles = self.getActiveRoles(rbacobject, info)
            s = [r for r in activeRoles if (r["roletype"]["id"] in roleIdsNeeded)]           
            isAllowed = len(s) > 0
            return isAllowed
        
    return InsertPermission


class AnyRolePermission(RBACPermission):
    message = "User has not appropriate roles"

    def on_unauthorized(self) -> None:
        return self.defaultResult
    
    async def has_permission(
            self, source: Any, info: strawberry.types.Info, **kwargs: Any
        # self, source, info: strawberry.types.Info, **kwargs
        # self, source, **kwargs
    ) -> bool:
        self.defaultResult = [] if info._field.type.__class__ == StrawberryList else None
        activeRoles = self.getActiveRoles(source, info)
        isAllowed = len(activeRoles) > 0
        return isAllowed
    


@cache
def RoleBasedPermission(roles: str = ""):
    roleIdsNeeded = RolesToList(roles)

    class RolebasedPermission(RBACPermission):
        message = "User has not appropriate roles"

        def on_unauthorized(self) -> None:
            return self.defaultResult
        
        async def has_permission(
                self, source: Any, info: strawberry.types.Info, **kwargs: Any
            # self, source, info: strawberry.types.Info, **kwargs
            # self, source, **kwargs
        ) -> bool:
            self.defaultResult = [] if info._field.type.__class__ == StrawberryList else None
            # return False
            logging.info(f"has_permission {kwargs}")
            # assert False
            activeRoles = self.getActiveRoles(source, info)
            s = [r for r in activeRoles if (r["roletype"]["id"] in roleIdsNeeded)]           
            isAllowed = len(s) > 0
            return isAllowed
        
    return RolebasedPermission


# class UserGDPRPermission(BasePermission):
#     message = "User is not authenticated"

#     async def has_permission(
#         self, source, info: strawberry.types.Info, **kwargs
#     ) -> bool:
#         print("UserGDPRPermission", source)
#         print("UserGDPRPermission", self)
#         print("UserGDPRPermission", kwargs)
#         return True
