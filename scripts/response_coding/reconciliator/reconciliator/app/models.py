from django.db import models


class Questions(models.Model):
    id = models.IntegerField(primary_key=True)
    qid = models.TextField()
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'questions'


class ResponseCodes(models.Model):
    id = models.IntegerField(primary_key=True)
    qid = models.TextField()
    pid = models.IntegerField()
    r0 = models.TextField(db_column='R0', blank=True, null=True)  # Field name made lowercase.
    r1 = models.TextField(db_column='R1', blank=True, null=True)  # Field name made lowercase.
    r2 = models.TextField(db_column='R2', blank=True, null=True)  # Field name made lowercase.
    r0r1 = models.TextField(db_column='R0R1', blank=True, null=True)  # Field name made lowercase.
    r0r2 = models.TextField(db_column='R0R2', blank=True, null=True)  # Field name made lowercase.
    r1r2 = models.TextField(db_column='R1R2', blank=True, null=True)  # Field name made lowercase.
    r0r1r2 = models.TextField(db_column='R0R1R2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'response_codes'


class Responses(models.Model):
    id = models.IntegerField(primary_key=True)
    pid = models.IntegerField()
    qid = models.TextField()
    response = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'responses'


class Terms(models.Model):
    #id = models.AutoField(unique=True)
    id = models.IntegerField(primary_key=True)
    term = models.TextField()
    definition = models.TextField()
    qid = models.TextField()

    class Meta:
        managed = False
        db_table = 'terms'