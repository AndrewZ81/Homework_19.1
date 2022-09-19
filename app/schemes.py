from marshmallow import Schema, fields


# Создаём класс сериализации сущностей "Режиссёр" базы данных
class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


# Создаём класс сериализации сущностей "Жанр" базы данных
class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


# Создаём класс сериализации сущностей "Фильм" базы данных
class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Nested(GenreSchema)
    director = fields.Nested(DirectorSchema)