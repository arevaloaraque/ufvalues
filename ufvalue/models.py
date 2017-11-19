'''
    Models for information related to UF
'''


from django.db import models


class Ufvalue(models.Model):
    '''
        Historical UF values by date
    '''
    key   = models.CharField(unique = True, null=False, max_length=8)
    value = models.FloatField(null=True, blank=True)
    date  = models.DateField(null=False, blank=False)

    def __unicode__(self):
        return "%s, %s" % (self.key, self.value)
