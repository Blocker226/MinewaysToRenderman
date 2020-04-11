#  Copyright (c) 2020 Blocker226. Released under GNU GPL 3.0

import maya.cmds as mc

fileNode = ""


def apply_pxr_material(node):
    global fileNode
    mc.undoInfo(openChunk=True)
    try:
        pxr_name = 'Pxr_' + node.split(":", 1)[1]
        if not mc.objExists(pxr_name):
            shd = mc.shadingNode('PxrSurface', name=pxr_name, asShader=True)
            shd_sg = mc.sets(name='{}SG'.format(shd), empty=True, renderable=True, noSurfaceShader=True)
            mc.connectAttr('{}.outColor'.format(shd), '{}.surfaceShader'.format(shd_sg))
            mc.sets(node, e=True, forceElement=shd_sg)
        else:
            print '{} material already created, skipping creation.'.format(pxr_name)
            shd = pxr_name
        # Find the associated texture file.
        # If there is a texture file already in use, delete this one and reuse that instead.
        filename = node + '2F'
        if mc.objExists(filename) and not fileNode:
            print 'Using {} for diffuse colour mapping.'.format(filename)
            fileNode = filename
        elif mc.objExists(filename) and filename != fileNode:
            # Disconnect everything before deleting the file node
            outgoing = mc.listConnections(filename, p=True, c=True, s=False) or []
            incoming = mc.listConnections(filename, p=True, c=True, d=False) or []
            out_pairs = zip(outgoing[::2], outgoing[1::2])
            in_pairs = zip(incoming[1::2], incoming[::2])
            for src, dest in out_pairs:
                mc.disconnectAttr(src, dest)
            for src, dest in in_pairs:
                mc.disconnectAttr(src, dest)
            mc.delete(filename)
        elif not fileNode:
            mc.warning('Unable to locate {}!, skipping!'.format(filename))
            return
        # Turn off filtering, and connect it to the diffuse color
        if not mc.connectionInfo('{}.diffuseColor'.format(shd), id=True):
            mc.connectAttr('{}.outColor'.format(fileNode), '{}.diffuseColor'.format(shd))
            print 'Connected {} to {}.'.format(fileNode, shd)
        elif mc.connectionInfo('{}.diffuseColor'.format(shd), sfd=True) == fileNode:
            print '{} already connected to {}, skipping.'.format(fileNode, shd)
        else:
            for attr in mc.listConnections('{}.diffuseColor'.format(shd), p=True):
                mc.disconnectAttr(attr, '{}.diffuseColor'.format(shd))
            mc.connectAttr('{}.outColor'.format(fileNode), '{}.diffuseColor'.format(shd))
            print 'Connected {} to {}.'.format(fileNode, shd)

        mc.setAttr('{}.rman__filter'.format(fileNode), 0)
        mc.setAttr('{}.filterType'.format(fileNode), 0)
        # Lastly, delete the old phong material and its shading group
        phong = node + '2'
        old_sg = node + '1'
        if mc.objExists(phong):
            mc.delete(phong)
            print 'Removed Phong {}'.format(phong)
        if mc.objExists(old_sg):
            mc.delete(old_sg)
            print 'Removed Shader Group {}'.format(old_sg)
    finally:
        mc.undoInfo(closeChunk=True)


def main():
    global fileNode
    fileNode = ""
    selected = mc.ls(sl=True)
    if len(selected) < 1:
        mc.error('No selection made.')
    else:
        for obj in selected:
            if mc.nodeType(obj) != 'transform':
                mc.error("Selected object {} is not a transform!".format(obj))
                break
            apply_pxr_material(obj)
        print 'PxrSurface conversion complete for {} items.'.format(len(selected)),


if __name__ == "__main__":
    main()
