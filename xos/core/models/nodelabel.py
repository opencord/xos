
from header import *





from core.models.node import Node 






class NodeLabel(PlCoreBase):
  # Primitive Fields (Not Relations)
  name = StrippedCharField( help_text = "label name", max_length = 200, null = False, db_index = False, blank = False )
  

  # Relations
  
  node = ManyToManyField(Node, db_index = False, related_name = 'nodelabels', null = False, through = 'NodeLabel_node', blank = True )

  def __unicode__(self): return u'%s' % (self.name)
  pass

