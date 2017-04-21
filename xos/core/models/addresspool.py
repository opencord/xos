
from header import *





from core.models.service import Service 






class AddressPool(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = CharField( blank = False, max_length = 32, null = False, db_index = False )
  addresses = TextField( blank = True, null = True, db_index = False )
  gateway_ip = CharField( blank = False, max_length = 32, null = True, db_index = False )
  gateway_mac = CharField( blank = False, max_length = 32, null = True, db_index = False )
  cidr = CharField( blank = False, max_length = 32, null = True, db_index = False )
  inuse = TextField( blank = True, null = True, db_index = False )
  

  # Relations
  
  service = ForeignKey(Service, db_index = True, related_name = 'addresspools', null = True, blank = True )

  def __unicode__(self): return u'%s' % (self.name)
  
  def get_address(self):
      with transaction.atomic():
          ap = AddressPool.objects.get(pk=self.pk)
          if ap.addresses:
              avail_ips = ap.addresses.split()
          else:
              avail_ips = []
  
          if ap.inuse:
              inuse_ips = ap.inuse.split()
          else:
              inuse_ips = []
  
          while avail_ips:
              addr = avail_ips.pop(0)
  
              if addr in inuse_ips:
                  # This may have happened if someone re-ran the tosca
                  # recipe and 'refilled' the AddressPool while some addresses
                  # were still in use.
                  continue
  
              inuse_ips.insert(0,addr)
  
              ap.inuse = " ".join(inuse_ips)
              ap.addresses = " ".join(avail_ips)
              ap.save()
              return addr
  
          addr = None
      return addr
  
  def put_address(self, addr):
      with transaction.atomic():
          ap = AddressPool.objects.get(pk=self.pk)
          addresses = ap.addresses or ""
          parts = addresses.split()
          if addr not in parts:
              parts.insert(0,addr)
              ap.addresses = " ".join(parts)
  
          inuse = ap.inuse or ""
          parts = inuse.split()
          if addr in parts:
              parts.remove(addr)
              ap.inuse = " ".join(parts)
  
          ap.save()
  
  
  pass

