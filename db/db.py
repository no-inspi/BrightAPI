from neomodel import StructuredNode, ArrayProperty, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom, config, StructuredRel, DateTimeProperty, Q, db
import datetime,json
import pytz

class MetricsRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )
class LikeRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )

class DisLikeRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )

class CommentRel(StructuredRel):
    since = DateTimeProperty(
        default=lambda: datetime.datetime.now(pytz.utc)+ datetime.timedelta(hours=2)
    )

class User(StructuredNode):
    username = StringProperty(unique_index=True)
    password = StringProperty()

class Comment(StructuredNode):
    content = StringProperty()
    users = RelationshipTo(User, 'POSTED_BY')

class Metrics(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    vues = IntegerProperty()
    post = RelationshipTo('Post', 'EVAL')
    liked_list_view = ArrayProperty(StringProperty(), default=[])

class Category(StructuredNode):
    name = StringProperty(unique_index=True)

class PathImg(StructuredNode):
    nomimg = StringProperty(unique_index=True)

class Post(StructuredNode):
    id_gun = StringProperty(unique_index=True)
    content = StringProperty()
    title = StringProperty()
    metrics = RelationshipFrom(Metrics, 'EVAL', model=MetricsRel)
    users = RelationshipTo(User, 'POSTED_BY')
    likes = RelationshipFrom(User, 'LIKED', model=LikeRel)
    dislikes = RelationshipFrom(User, 'DISLIKED', model=DisLikeRel)
    comments = RelationshipFrom(Comment, 'COMMENT', model=CommentRel)
    categories = RelationshipTo(Category, 'CATEGORISED BY')
    img = RelationshipTo(PathImg, 'Image Path')