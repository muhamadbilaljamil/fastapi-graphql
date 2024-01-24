# import graphene
# from fastapi import FastAPI
# from starlette.graphql import GraphQLApp

# from .schema import Mutation, Query

import asyncio
import graphene
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route
from graphene_file_upload.scalars import Upload
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()


class Query(graphene.ObjectType):
    me = graphene.Field(User)

    def resolve_me(root, info):
        return {"id": "john", "name": "John"}


class FileUploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        return FileUploadMutation(ok=True)


class Mutation(graphene.ObjectType):
    upload_file = FileUploadMutation.Field()


class Subscription(graphene.ObjectType):
    count = graphene.Int(upto=graphene.Int())

    async def subscribe_count(root, info, upto=3):
        for i in range(upto):
            yield i
            await asyncio.sleep(1)

schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)

class Homepage(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse(f"Hello, world!")


class User(HTTPEndpoint):
    async def get(self, request):
        username = request.path_params['username']
        return PlainTextResponse(f"Hello, {username}")

routes = [
    Route("/", Homepage),
    Route("/{username}", User)
]

app = Starlette(routes=routes)

app.add_route("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler() ))