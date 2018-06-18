from app import db
from marshmallow import Schema, fields


# # -- Models --
class UserVoice(db.Model):
    __tablename__ = 'user_voice'
    session_id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    location = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)


class VoiceProfile(db.Model):
    __tablename__ = 'voice_profile'
    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)
    model_location = db.Column(db.String, nullable=False)
    # shortcut for accessing on disk
    model_relative_path = db.Column(db.String, nullable=False)
    # add protected profiles like 'admin', 'system'
    user = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class ConvertedVoice(db.Model):
    __tablename__ = 'converted_voice'
    session_id = db.Column(db.String, nullable=False, primary_key=True)
    location = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)


# -- Schemas --
class UserVoiceSchema(Schema):
    session_id = fields.String()
    location = fields.String()
    user = fields.String()


class VoiceProfileSchema(Schema):
    name = fields.String()
    version = fields.String()
    model_location = fields.String()
    model_relative_path = fields.String()
    user = fields.String()


class ConvertedVoiceSchema(Schema):
    session_id = fields.String()
    location = fields.String()
    user = fields.String()


class InferenceSchema(Schema):
    session_id = fields.String()
    user_voice_location = fields.String()
    voice_profile_id = fields.Integer()


user_voice_schema = UserVoiceSchema()
voice_profile_schema = VoiceProfileSchema()
converted_voice_schema = ConvertedVoiceSchema()
inference_schema = InferenceSchema()
