import peewee as pw

database = pw.SqliteDatabase('ca.db')

class BaseModel(pw.Model):
    class Meta:
        database = database

class Certificates(BaseModel):
    subject = pw.CharField(unique=True)
    serial = pw.IntegerField()
    keyhash = pw.CharField()

class RevokedCertificates(BaseModel):
    serial = pw.CharField(unique=True)

database.create_tables([Certificates, RevokedCertificates])