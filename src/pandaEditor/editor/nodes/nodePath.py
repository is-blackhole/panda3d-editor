import pandac.PandaModules as pm
from pandac.PandaModules import NodePath as NP
from direct.directtools.DirectSelection import DirectBoundingBox

from constants import *
from game.nodes.constants import *
from game.nodes.nodePath import NodePath as GameNodePath
from game.nodes.attributes import NodePathAttribute as Attr


class NodePath( GameNodePath ):
    
    geo = None
    pickable = True
    
    def __init__( self, *args, **kwargs ):
        GameNodePath.__init__( self, *args, **kwargs )
        
        # Add attributes for position, rotation and scale. These are
        # implemented editor side only as we only need a matrix to xform the
        # node. These are provided for the user's benefit only.
        pAttr = self.FindAttribute( 'nodePath' )
        attr = Attr( 'Position', pm.Vec3, NP.getPos, NP.setPos, w=False )
        attr.children.extend( 
            [
                Attr( 'X', float, NP.getX, NP.setX, w=False ),
                Attr( 'Y', float, NP.getY, NP.setY, w=False ),
                Attr( 'Z', float, NP.getZ, NP.setZ, w=False )
            ]
        )
        pAttr.children.append( attr )
        
        attr = Attr( 'Rotation', pm.Vec3, NP.getHpr, NP.setHpr, w=False )
        attr.children.extend( 
            [
                Attr( 'H', float, NP.getH, NP.setH, w=False ),
                Attr( 'P', float, NP.getP, NP.setP, w=False ),
                Attr( 'R', float, NP.getR, NP.setR, w=False )
            ]
        )
        pAttr.children.append( attr )
         
        attr = Attr( 'Scale', pm.Vec3, NP.getScale, NP.setScale, w=False )
        attr.children.extend( 
            [
                Attr( 'Sx', float, NP.getSx, NP.setSx, w=False ),
                Attr( 'Sy', float, NP.getSy, NP.setSy, w=False ),
                Attr( 'Sz', float, NP.getSz, NP.setSz, w=False )
            ]
        )
        pAttr.children.append( attr )
        
    @classmethod
    def SetPickable( cls, value=True ):
        cls.pickable = value
        
    @classmethod
    def SetEditorGeometry( cls, geo ):
        geo.setPythonTag( TAG_IGNORE, True )
        geo.setLightOff()
        geo.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        cls.geo = geo
        
    def SetupNodePath( self, np ):
        GameNodePath.SetupNodePath( self, np )
        
        if self.geo is not None:
            self.geo.copyTo( np )
            
        if self.pickable:
            np.setPythonTag( TAG_PICKABLE, self.pickable )
            
    def OnSelect( self, np ):
        """Add a bounding box to the indicated node."""
        bbox = DirectBoundingBox( np, (1, 1, 1, 1) )
        bbox.show()
        bbox.lines.setPythonTag( TAG_IGNORE, True )
        bbox.lines.node().adjustDrawMask( *base.GetEditorRenderMasks() )
        np.setPythonTag( TAG_BBOX, bbox )
        return bbox
    
    def OnDeselect( self, np ):
        """Remove the bounding box from the indicated node."""
        bbox = np.getPythonTag( TAG_BBOX )
        if bbox is not None:
            bbox.lines.removeNode()
        np.clearPythonTag( TAG_BBOX )
    
    def OnDelete( self, np ):
        pass
    
    def GetConnections( self ):
        data = {}
        lights = self.data.getAttrib( pm.LightAttrib )
        if lights is not None:
            onLights = lights.getOnLights()
            uuids = [lgt.getTag( TAG_NODE_UUID ) for lgt in onLights]
            data['onLight'] = uuids
        return data