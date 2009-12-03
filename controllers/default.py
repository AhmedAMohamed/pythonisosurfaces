p3d = local_import('p3d')
from math import *

response.title = "Marching Cubes"
response.subtitle = "Iso-surfaces with Python + processing.js + web2py"
session.forget()

def index():
    return dict()

def isosurface():   
    legend="""
    Sample iso-surface for topological charge density in 
    Quantum Chromo Dynamics
    """
    response.view='default/p3d.html'
    import os
    obj=p3d.P3D(300,onrotate=URL(r=request,f='onrotate'))
    field = p3d.read_vtk(os.path.join(request.folder,
                                      'private/topological_charge2.vtk'))
    obj.isosurface(field,0.3,0.0,red=255,green=0,blue=0)
    obj.isosurface(field,0.0,0.3,red=0,green=0,blue=255)
    return dict(obj=obj, legend=legend)

def func():    
    legend = """
    3D Plot of f(x,y,z) = sin(r)/r
    """
    response.view='default/p3d.html'
    def u(r): return sin(sqrt(r)+0.01)/(sqrt(r)+0.01)
    obj=p3d.P3D(onrotate=URL(r=request,f='onrotate'))
    field = p3d.make_points(lambda x,y,z: y + u(x**2+z**2),
                            (-10,10,1), (-2,2,0.5),(-10,10,1))
    obj.isosurface(field,0.0,0.0,red=0,green=255,blue=0)
    return dict(obj=obj, legend=legend)

def star():
    legend = """
    Iso-surface for f(x,y,z) = (x*y*z)**2
    """
    response.view='default/p3d.html'
    obj=p3d.P3D(onrotate=URL(r=request,f='onrotate'))
    field = p3d.make_points(lambda x,y,z: (x*y*z)**2,
                            (-2,2,0.5), (-2,2,0.5), (-2,2,0.5))
    obj.isosurface(field,0.01,0.0,red=250,green=250,blue=110)
    return dict(obj=obj, legend=legend)


def torus():   
    legend = """
    A simple torus
    """
    response.view='default/p3d.html'
    obj=p3d.P3D(onrotate=URL(r=request,f='onrotate'))
    field = p3d.make_points(lambda x,y,z: cos(x**2+y**2-2.6)-z**2,
                            (-2,2,0.2), (-2,2,0.2), (-3,3,0.5))
    obj.isosurface(field,0.5,0.0,red=255,green=0,blue=0)
    return dict(obj=obj, legend=legend)


def onrotate():
    """this callback funcion is called via ajax to report the current angles"""
    session.p3d_alpha = request.vars.alpha
    session.p3d_beta = request.vars.beta    
    return ''

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
