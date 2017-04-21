def __unicode__(self):  return u'%s' % (self.name)

@property
def slicename(self):
    return "%s_%s" % (self.site.login_base, self.name)

def can_update(self, user):
    return user.can_update_slice(self)

@staticmethod
def select_by_user(user):
    if user.is_admin:
        qs = Slice.objects.all()
    else:
        from core.models.sliceprivilege import SlicePrivilege 
        # users can see slices they belong to 
        slice_ids = [sp.slice.id for sp in SlicePrivilege.objects.filter(user=user)]
        # pis and admins can see slices at their sites
        sites = [sp.site for sp in SitePrivilege.objects.filter(user=user)\
                    if (sp.role.role == 'pi') or (sp.role.role == 'admin')]
        slice_ids.extend([s.id for s in Slice.objects.filter(site__in=sites)])
        qs = Slice.objects.filter(id__in=slice_ids)
    return qs
