from typing import List, Union, Optional
import typing
import strawberry
import asyncio

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
#
# priklad rozsireni UserGQLModel
#

import datetime
import uuid
from .BaseGQLModel import BaseGQLModel

from ._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_valid,

    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    resolve_changedby
)

from src.Dataloaders import getLoadersFromInfo, getUserFromInfo

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]
SubjectGQLModel = typing.Annotated["SubjectGQLModel", strawberry.lazy(".externals")]

IDType = uuid.UUID

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a publication type"""
)
class PublicationTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info): 
        return getLoadersFromInfo(info).PublicationTypeModel
    
    id = resolve_id
    name = resolve_name

    created = resolve_created,
    lastchange = resolve_lastchange,
    created_by = resolve_createdby,
    changed_by = resolve_changedby,

    @strawberry.field(description="""List of publications with this type""")
    async def publications(
        self, info: strawberry.types.Info
    ) -> typing.List["PublicationGQLModel"]:
        loader = PublicationGQLModel.getLoader(info)
        result = await loader.filter_by()
        return result

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a publication"""
)
class PublicationGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info): 
        return getLoadersFromInfo(info).PublicationModel

    id = resolve_id
    name = resolve_name

    created = resolve_created,
    lastchange = resolve_lastchange,
    created_by = resolve_createdby,
    changed_by = resolve_changedby,

    @strawberry.field(description="""published year""")
    def published_date(self) -> datetime.date:
        return self.published_date

    @strawberry.field(description="""place""")
    def place(self) -> str:
        return self.place

    @strawberry.field(description="""reference""")
    def reference(self) -> str:
        return self.reference

    @strawberry.field(description="""If a publication is valid""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(
        description="""List of authors, where the author participated in publication"""
    )
    async def authors(
        self, info: strawberry.types.Info
    ) -> typing.List["PublicationAuthorGQLModel"]:
        loader = PublicationAuthorGQLModel.getLoader(info)
        result = await loader.filter_by(publication_id=self.id)
        return result

    @strawberry.field(description="""Publication type""")
    async def publicationtype(
        self, info: strawberry.types.Info
    ) -> PublicationTypeGQLModel:
        return await PublicationTypeGQLModel.resolve_reference(info, id=self.publication_type_id)

    @strawberry.field(description="""Subjects publication is linked to""")
    async def subjects(self, info: strawberry.types.Info) -> List["SubjectGQLModel"]:
        from .externals import SubjectGQLModel
        loader = getLoadersFromInfo(info).SubjectModel
        rows = await loader.filter_by(subject_id=self.id)
        awaitables = (SubjectGQLModel.resolve_reference(info, row.subject_id) for row in rows)
        return await asyncio.gather(*awaitables)



@strawberry.federation.type(
    keys=["id"],
    description="""Entity representing a relation between an user and a publication""",
)
class PublicationAuthorGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info): 
        return getLoadersFromInfo(info).AuthorModel

    id = resolve_id
    name = resolve_name

    created = resolve_created,
    lastchange = resolve_lastchange,
    created_by = resolve_createdby,
    changed_by = resolve_changedby,

    @strawberry.field(description="""order in author list""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="""share on publication""")
    def share(self) -> float:
        return self.share

    @strawberry.field(description="""user""")
    async def user(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        return await UserGQLModel.resolve_reference(info, self.user_id)

    @strawberry.field(description="""publication""")
    async def publication(self, info: strawberry.types.Info) -> "PublicationGQLModel":
        return await PublicationGQLModel.resolve_reference(info, self.publication_id)


    @strawberry.field(description="""If an author is valid""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


from dataclasses import dataclass
from uoishelpers.resolvers import createInputs
from typing import Optional
from ._GraphResolvers import encapsulateInsert, encapsulateDelete, encapsulateUpdate
@createInputs
@dataclass
class PublicationInputWhereFilter:
    name: str
    name_en: str

@strawberry.input(description="")
class PublicationUpdateGQLModel:
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[IDType] = None
    valid: Optional[bool] = None


@strawberry.input(description="")
class PublicationInsertGQLModel:
    id: Optional[IDType] = None
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[IDType] = None
    valid: Optional[bool] = None

@strawberry.type(description="Result of mutation")
class PublicationResultGQLModel:
    id: IDType = strawberry.field(description="The ID of the project", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the project")
    async def publication(self, info: strawberry.types.Info) -> Optional[PublicationGQLModel]:
        result = await PublicationGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.field(description="""Updates publication data""")
async def publication_update(
    self, info: strawberry.types.Info, publication: "PublicationUpdateGQLModel"
) -> "PublicationResultGQLModel":
    return await encapsulateUpdate(info, PublicationGQLModel.getLoader(info), publication, PublicationResultGQLModel(id=publication.id, msg="ok"))

@strawberry.field(description="""Inserts publication data""")
async def publication_insert(
    self, info: strawberry.types.Info, publication: "PublicationInsertGQLModel"
) -> "PublicationResultGQLModel":
    return await encapsulateInsert(info, PublicationGQLModel.getLoader(info), publication, PublicationResultGQLModel(id=publication.id, msg="ok"))

@strawberry.field(description="""Inserts publication data""")
async def publication_delete(
    self, info: strawberry.types.Info, publication_id: IDType
) -> "PublicationResultGQLModel":
    return await encapsulateDelete(info, PublicationGQLModel.getLoader(info), id, PublicationResultGQLModel(id=publication_id, msg="ok"))

@createInputs
@dataclass
class PublicationTypeInputWhereFilter:
    name: str
    name_en: str

@strawberry.input(description="")
class PublicationTypeUpdateGQLModel:
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[IDType] = None
    valid: Optional[bool] = None


@strawberry.input(description="")
class PublicationTypeInsertGQLModel:
    id: Optional[IDType] = None
    name: Optional[str] = None
    place: Optional[str] = None
    published_date: Optional[datetime.date] = None
    reference: Optional[str] = None
    publication_type_id: Optional[IDType] = None
    valid: Optional[bool] = None

@strawberry.type(description="Result of mutation")
class PublicationTypeResultGQLModel:
    id: IDType = strawberry.field(description="The ID of the type", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the project")
    async def publication_type(self, info: strawberry.types.Info) -> Optional[PublicationTypeGQLModel]:
        result = await PublicationTypeGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.field(description="""Updates publication data""")
async def publication_type_update(
    self, info: strawberry.types.Info, publication_type: "PublicationTypeUpdateGQLModel"
) -> "PublicationTypeResultGQLModel":
    return await encapsulateUpdate(info, PublicationTypeGQLModel.getLoader(info), publication_type, PublicationTypeResultGQLModel(id=publication_type.id, msg="ok"))

@strawberry.field(description="""Inserts PublicationType data""")
async def publication_type_insert(
    self, info: strawberry.types.Info, publication_type: "PublicationTypeInsertGQLModel"
) -> "PublicationTypeResultGQLModel":
    return await encapsulateInsert(info, PublicationTypeGQLModel.getLoader(info), publication_type, PublicationTypeResultGQLModel(id=publication_type.id, msg="ok"))

@strawberry.field(description="""Deletes PublicationType data""")
async def publication_type_delete(
    self, info: strawberry.types.Info, publication_type_id: IDType
) -> "PublicationTypeResultGQLModel":
    return await encapsulateDelete(info, PublicationTypeGQLModel.getLoader(info), id, PublicationTypeResultGQLModel(id=id, msg="ok"))

@createInputs
@dataclass
class PublicationAuthorInputWhereFilter:
    user_id: IDType
    publication_id: IDType

@strawberry.input(description="")
class PublicationAuthorUpdateGQLModel:
    id: IDType = strawberry.field(description="The ID of the Author data")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of last change")

    valid: Optional[bool] = strawberry.field(description="Indicates whether the data is valid or not (optional)", default=None)
    user_id: Optional[uuid.UUID] = strawberry.field(description="The ID of the data type",default=None)
    order: Optional[int] = strawberry.field(description="The order of the Author in the publication")
    share: Optional[float] = strawberry.field(description="The share of the Author in the publication",default=None)
    changedby: strawberry.Private[uuid.UUID] = None    

@strawberry.input(description="")
class PublicationAuthorInsertGQLModel:
    publication_id: uuid.UUID = strawberry.field(description="The ID of the associated publication")
    user_id: uuid.UUID = strawberry.field(description="The ID of the associated user")

    order: Optional[int] = strawberry.field(description="The order of the Author in the publication")
    share: Optional[float] = strawberry.field(description="The share of the Author in the publication",default=None)
    valid: Optional[bool] = strawberry.field(description="Indicates whether the data is valid or not (optional)", default=True)
    createdby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="Result of mutation")
class PublicationAuthorResultGQLModel:
    id: IDType = strawberry.field(description="The ID of the project", default=None)
    msg: str = strawberry.field(description="Result of the operation (OK/Fail)", default=None)

    @strawberry.field(description="Returns the project")
    async def author(self, info: strawberry.types.Info) -> Optional["PublicationAuthorGQLModel"]:
        result = await PublicationGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.field(description="""Updates an author""")
async def publication_author_update(
    self, info: strawberry.types.Info, author: PublicationAuthorUpdateGQLModel) -> "AuthorResultGQLModel":
    return await encapsulateUpdate(info, PublicationAuthorGQLModel.getLoader(info), author, PublicationAuthorResultGQLModel(id=author.id, msg="ok"))


@strawberry.field(description="""Adds the authorship to the publication, Currently it does not check if the authorship exists.""")
async def publication_author_insert(
    self, info: strawberry.types.Info, author: PublicationAuthorInsertGQLModel) -> "AuthorResultGQLModel":
    return await encapsulateInsert(info, PublicationAuthorGQLModel.getLoader(info), author, PublicationAuthorResultGQLModel(id=author.id, msg="ok"))


@strawberry.field(description="""Deletes the author""")
async def publication_author_delete(
    self, info: strawberry.types.Info, id: IDType) -> "AuthorResultGQLModel":
    return await encapsulateDelete(info, PublicationAuthorGQLModel.getLoader(info), id, PublicationAuthorResultGQLModel(id=id, msg="ok"))



###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################
from ..DBResolvers import DBResolvers
from ._GraphPermissions import OnlyForAuthentized

publication_by_id = strawberry.field(
    description="returns the publication",
    permission_classes=[
        OnlyForAuthentized
        ],
    resolver=DBResolvers.PublicationModel.resolve_by_id(PublicationGQLModel)
)

publication_page = strawberry.field(
    description="returns list of publications",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.PublicationModel.resolve_page(PublicationGQLModel, WhereFilterModel=PublicationInputWhereFilter)
    )

publication_type_by_id = strawberry.field(
    description="returns the publication",
    permission_classes=[
        OnlyForAuthentized
        ],
    resolver=DBResolvers.PublicationTypeModel.resolve_by_id(PublicationTypeGQLModel)
)

publication_type_page = strawberry.field(
    description="returns list of publications",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.PublicationTypeModel.resolve_page(PublicationTypeGQLModel, WhereFilterModel=PublicationInputWhereFilter)
    )


author_by_id = strawberry.field(
    description="returns the author",
    permission_classes=[
        OnlyForAuthentized
        ],
    resolver=DBResolvers.AuthorModel.resolve_by_id(PublicationAuthorGQLModel)
)

author_page = strawberry.field(
    description="returns list of authors",
    permission_classes=[
        OnlyForAuthentized
    ],
    resolver=DBResolvers.AuthorModel.resolve_page(PublicationAuthorGQLModel, WhereFilterModel=PublicationAuthorInputWhereFilter)
    )




###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

from typing import Optional
import datetime

@strawberry.input(description="")
class PublicationInsertGQLModel:
    name: str
    
    id: Optional[IDType] = None
    publication_type_id: Optional[IDType] = None
    place: Optional[str] = ""
    published_date: Optional[datetime.datetime] = datetime.datetime.now()
    reference: Optional[str] = ""
    valid: Optional[bool] = True

@strawberry.input(description="")
class PublicationUpdateGQLModel:
    lastchange: datetime.datetime
    id: IDType

    name: Optional[str] = None
    publication_type_id: Optional[IDType] = None
    place: Optional[str] = None
    published_date: Optional[datetime.datetime] = None
    reference: Optional[str] = None
    valid: Optional[bool] = None
    
    
@strawberry.type(description="")
class PublicationResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of publication operation""")
    async def publication(self, info: strawberry.types.Info) -> Union[PublicationGQLModel, None]:
        result = await PublicationGQLModel.resolve_reference(info, self.id)
        return result
   

@strawberry.input(description="")
class AuthorInsertGQLModel:
    user_id: IDType
    publication_id: IDType
    id: Optional[IDType] = None
    share: Optional[float] = 0.1
    order: Optional[int] = 1000

@strawberry.input(description="")
class AuthorUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    share: Optional[float] = None
    order: Optional[int] = None
    
@strawberry.type(description="")
class AuthorResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of publication operation""")
    async def author(self, info: strawberry.types.Info) -> Union[PublicationAuthorGQLModel, None]:
        result = await PublicationAuthorGQLModel.resolve_reference(info, self.id)
        return result

