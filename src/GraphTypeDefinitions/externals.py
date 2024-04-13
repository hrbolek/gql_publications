import strawberry
import uuid
import typing
import asyncio

from ..Dataloaders import getLoadersFromInfo

PublicationAuthorGQLModel = typing.Annotated["PublicationAuthorGQLModel", strawberry.lazy(".Others")]
PublicationGQLModel = typing.Annotated["PublicationGQLModel", strawberry.lazy(".Others")]

# @classmethod
# async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
#     return cls(id=id)
@classmethod
async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID): return cls(id=id)


class BaseEternal:
    id: uuid.UUID = strawberry.federation.field(external=True)


@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference
    @strawberry.field(description="""List of authors""")
    async def author_publications(
        self, info: strawberry.types.Info
    ) -> typing.List["PublicationAuthorGQLModel"]:
        from .Others import PublicationAuthorGQLModel
        loader = PublicationAuthorGQLModel.getLoader(info)
        result = await loader.filter_by(user_id=self.id)
        return result

@strawberry.federation.type(extend=True, keys=["id"])
class RoleTypeGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class GroupGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference


@strawberry.federation.type(extend=True, keys=["id"])
class EventGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

@strawberry.federation.type(extend=True, keys=["id"])
class SubjectGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    @strawberry.field(description="""linked publications""")
    async def publication(self, info: strawberry.types.Info) -> typing.List["PublicationGQLModel"]:
        loader = getLoadersFromInfo(info).SubjectModel
        from .Others import PublicationGQLModel
        rows = await loader.filter_by(subject_id=self.id)
        awaitables = (PublicationGQLModel.resolve_reference(info, row.publication_id) for row in rows)
        return await asyncio.gather(*awaitables)

@strawberry.federation.type(extend=True, keys=["id"])
class RBACObjectGQLModel:
    id: uuid.UUID = strawberry.federation.field(external=True)
    resolve_reference = resolve_reference

    # @classmethod
    # async def resolve_roles(cls, info: strawberry.types.Info, id: uuid.UUID):
    #     loader = getLoadersFromInfo(info).authorizations
    #     authorizedroles = await loader.load(id)
    #     return authorizedroles